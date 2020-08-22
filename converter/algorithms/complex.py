import numpy as np
from numba import njit, uint8

from converter.image import MyImage
from .base import BaseAlgorithm

BLACK = 0
WHITE = 255


@njit
def saturate(img: MyImage, sw_size=1, min_black_cnt=3, black_threshold=75) -> MyImage:
    new = MyImage(np.copy(img.array))
    for (x, y), color in np.ndenumerate(img.array):
        window = img.array[x-sw_size:x+sw_size+1, y-sw_size:y+sw_size+1]
        if np.sum(window < black_threshold) > min_black_cnt:
            new.array[x, y] = BLACK
        else:
            new.array[x, y] = WHITE
    return new


@njit
def invert(img: MyImage):
    return MyImage(uint8(255) - img.array)


@njit
def crop(img: MyImage) -> MyImage:
    upper, lower, left, right = 0, img.height, 0, img.width
    for i, row in enumerate(img.array):
        if np.sum(row == WHITE) > 0:
            upper = i
            break
    for i, row in enumerate(img.array[::-1]):
        if np.sum(row == WHITE) > 0:
            lower = img.height - i
            break
    for i, row in enumerate(img.array.T):
        if np.sum(row == WHITE) > 0:
            left = i
            break
    for i, row in enumerate(img.array.T[::-1]):
        if np.sum(row == WHITE) > 0:
            right = img.width - i
            break
    return MyImage(img.array[upper:lower, left:right])


@njit
def fit_screen(img: MyImage, screen_shape=(448, 368), frame=20) -> MyImage:
    screen_ratio = screen_shape[0] / screen_shape[1]
    img_ratio = img.height / img.width

    filler_width = np.int(img.width * (img_ratio / screen_ratio - 1) / 2) * (img_ratio > screen_ratio)
    filler = np.zeros((img.height, frame + filler_width), dtype=uint8)
    new = MyImage(np.concatenate((filler, img.array, filler), axis=1))

    filler_height = np.int(new.height * (screen_ratio / img_ratio - 1) / 2) * (img_ratio < screen_ratio)
    filler = np.zeros((frame + filler_height, new.width), dtype=uint8)
    new = MyImage(np.concatenate((filler, new.array, filler), axis=0))

    return new


class ComplexAlgorithm(BaseAlgorithm):
    def process(self, img: MyImage):
        saturated = saturate(img)
        inverted = invert(saturated)
        cropped = crop(inverted)
        return fit_screen(cropped)
