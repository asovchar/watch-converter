import os
import datetime
from glob import glob
from typing import Generator
from itertools import product
from operator import itemgetter
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
from PIL import Image
import numpy as np


BLACK = 0
WHITE = 255
BLACK_THRESHOLD = 75


class Converter:
    _supported_formats = ['.jpg', '.png']

    _log = '{:5s}  {:50s} {:50s} {:50s}'

    def __init__(self, width: int, height: int, raw_path: str, processed_path: str) -> None:
        self._width = width
        self._height = height
        self._screen_ratio = height / width

        self._thread_count = cpu_count()

        self._raw_photos_path = raw_path if raw_path[-1] == '/' else raw_path + '/'
        self._processed_photos_path = processed_path if processed_path[-1] == '/' else processed_path + '/'
        self._processed_name_template = self._processed_photos_path + 'watch_img_{:03d}.jpg'

        self._raw_images = []
        self._processed_images = []

    @staticmethod
    def _open_image(name: str) -> np.ndarray:
        img = Image.open(name).convert('L')
        return np.array(img)

    @staticmethod
    def _save_image(arr: np.ndarray, name: str) -> None:
        img = Image.fromarray(arr).convert('L')
        img.save(name)

    @staticmethod
    def _fix(img_arr, ind=1, num=3):
        fix_arr = np.copy(img_arr)
        h, w = img_arr.shape
        for i in range(ind, h - ind):
            for j in range(ind, w - ind):
                arr = np.array([img_arr[i + m, j + n] for m, n in product(range(-ind, ind + 1), repeat=2)])
                if len(arr[arr < BLACK_THRESHOLD]) > num:
                    fix_arr[i, j] = 0
        return fix_arr

    @staticmethod
    def _invert(img_arr):
        new_arr = np.copy(img_arr)
        for idx, val in np.ndenumerate(img_arr):
            if val < BLACK_THRESHOLD:
                new_arr[idx] = WHITE
            else:
                new_arr[idx] = BLACK
        return new_arr

    @staticmethod
    def _find_borders(img_arr: np.ndarray) -> Generator[int, None, None]:
        idx_list = [idx for idx, _ in np.ndenumerate(img_arr)]
        directions = product((0, 1), repeat=2)
        for axis, reverse in directions:
            for idx in sorted(idx_list, key=itemgetter(axis), reverse=reverse):
                if img_arr[idx] == WHITE:
                    yield idx[axis]
                    break

    @staticmethod
    def _cut_borders(img_arr: np.ndarray, borders: Generator[int, None, None] = None) -> np.ndarray:
        if borders is None:
            return np.copy(img_arr)
        else:
            n, s, e, w = borders
            return np.copy(img_arr[n:s, e:w])

    @staticmethod
    def _restore_ratio(img_arr: np.ndarray, screen_ratio: float = 1., margin: int = 20):
        h, w = img_arr.shape
        ratio = h / w
        coef = (1, ratio / screen_ratio) if ratio > screen_ratio else (screen_ratio / ratio, 1)
        new_arr = np.zeros(tuple(int(i * c + 2 * margin) + 1 for i, c in zip((h, w), coef)))
        for idx, val in np.ndenumerate(img_arr):
            if val == WHITE:
                new_idx = tuple(int((k - j) / 2 + i) for i, j, k in zip(idx, img_arr.shape, new_arr.shape))
                new_arr[new_idx] = val
        return new_arr

    def _process_one(self, name: str, new_name: str, idx: int) -> None:
        start = datetime.datetime.utcnow()
        img_arr = self._open_image(name)
        fixed = self._fix(img_arr)
        colored = self._invert(fixed)

        borders = self._find_borders(colored)
        cut = self._cut_borders(colored, borders)
        restored = self._restore_ratio(cut, self._screen_ratio)

        self._save_image(restored, new_name)

        print(self._log.format(str(idx), name, new_name, str(datetime.datetime.utcnow() - start)))

    def find(self) -> None:
        for format_ in self._supported_formats:
            self._raw_images.extend(sorted(glob('{}/*{}'.format(self._raw_photos_path, format_))))

    def process(self) -> None:
        print(self._log.format('Index', 'Source', 'Result', 'Duration'))

        self._processed_images = [self._processed_name_template.format(idx) for idx in range(len(self._raw_images))]
        indexes = [idx for idx in range(len(self._raw_images))]

        with ProcessPoolExecutor(max_workers=self._thread_count) as executor:
            executor.map(self._process_one, self._raw_images, self._processed_images, indexes)

    def order_timestamps(self, seconds_delta: int = 10) -> None:
        now = datetime.datetime.utcnow()
        for name in self._processed_images:
            stamp = (now + datetime.timedelta(seconds=seconds_delta)).strftime('%m/%d/%Y %H:%M:%S')
            os.system('SetFile -d "{0}" -m "{0}" {1}'.format(stamp, name))
