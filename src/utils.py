"""random convenience utilities"""
from os import path


def get_root_dir():
    """returns the root directory of the project"""
    return path.dirname(path.abspath(__file__))
