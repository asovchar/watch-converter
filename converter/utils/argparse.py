import os
from argparse import ArgumentTypeError
from functools import partial
from typing import Callable


def validate(type: Callable, constrain: Callable):
    def wrapper(value):
        value = type(value)
        if not constrain(value):
            raise ArgumentTypeError
        return value

    return wrapper


valid_path = validate(str, constrain=os.path.exists)
