from operator import itemgetter
from itertools import product
import numpy as np


def find_borders(img_arr):
    idx_list = [idx for idx, _ in np.ndenumerate(img_arr)]
    directions = product((0, 1), repeat=2)
    for axis, reverse in directions:
        for idx in sorted(idx_list, key=itemgetter(axis), reverse=reverse):
            if img_arr[idx] == 255:
                yield idx[axis]
                break


def cut_borders(img_arr, borders=None):
    if borders is None:
        new_arr = np.copy(img_arr)
    else:
        n, s, e, w = borders
        new_arr = np.copy(img_arr[n:s, e:w])
    return new_arr


def restore_ratio(img_arr, screen_ratio=1, margin=10):
    h, w = img_arr.shape
    ratio = h / w
    coef = (1, ratio / screen_ratio) if ratio > screen_ratio else (screen_ratio / ratio, 1)
    new_arr = np.zeros(tuple(int(i * c + 2 * margin) + 1 for i, c in zip((h, w), coef)))
    for idx, val in np.ndenumerate(img_arr):
        if val == 255:
            new_idx = tuple(int((k - j) / 2 + i) for i, j, k in zip(idx, img_arr.shape, new_arr.shape))
            new_arr[new_idx] = val
    return new_arr
