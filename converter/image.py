import numpy as np
from numba import uint8
from numba.experimental import jitclass
from PIL import Image


@jitclass([("_array", uint8[:, :])])
class MyImage:
    def __init__(self, array: np.ndarray):
        self._array = array

    @property
    def array(self):
        return self._array

    @property
    def height(self):
        return self._array.shape[0]

    @property
    def width(self):
        return self._array.shape[1]


def load(filename: str) -> MyImage:
    img = Image.open(filename).convert("L")
    return MyImage(np.array(img))


def dump(image: MyImage, filename: str):
    img = Image.fromarray(image.array)
    img.save(filename)


__all__ = ("MyImage", "load", "dump")
