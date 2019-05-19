import numpy as np
from itertools import product


def fix(img_arr, ind=1, num=3):
    fix_arr = np.copy(img_arr)
    h, w = img_arr.shape
    for i in range(ind, h-ind):
        for j in range(ind, w-ind):
            arr = np.array([img_arr[i+m, j+n] for m, n in product(range(-ind, ind+1), repeat=2)])
            if len(arr[arr < 75]) > num:
                fix_arr[i, j] = 0
    return fix_arr


def invert(img_arr):
    new_arr = np.copy(img_arr)
    for idx, val in np.ndenumerate(img_arr):
        if val < 50:
            new_arr[idx] = 255
        else:
            new_arr[idx] = 0
    return new_arr
