from PIL import Image
import numpy as np


def load_image(name):
    img = Image.open(name).convert('L')
    arr = np.array(img)
    return arr


def save_image(arr, name):
    img = Image.fromarray(arr).convert('L')
    img.save(name)
