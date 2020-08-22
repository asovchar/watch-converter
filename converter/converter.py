import glob
import os

from converter.algorithms import ComplexAlgorithm
from converter.image import load, dump


class Converter:
    def __init__(self, algorithm=ComplexAlgorithm):
        self.algo = algorithm()

    @staticmethod
    def find_images(path):
        if os.path.isfile(path):
            yield load(path)
        else:
            filenames = glob.glob(os.path.join(path, f"*.jpg"))
            yield from map(load, sorted(filenames))

    def run(self, input_dir, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        for idx, img in enumerate(self.find_images(input_dir)):
            res = self.algo.process(img)
            dump(res, os.path.join(output_dir, f"watch_img_{idx}.jpg"))
