from numba import njit, uint8

from converter.image import MyImage
from .base import BaseAlgorithm


@njit
def invert(img: MyImage):
    return MyImage(uint8(255) - img.array)


class SimpleAlgorithm(BaseAlgorithm):
    def process(self, img: MyImage):
        return invert(img)
