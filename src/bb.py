"""Interacts with BB web reporting"""

from enum import Enum
import subprocess


# class syntax
class Color(Enum):
    """available BB colors"""

    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"


def _date():
    return subprocess.check_output(["date"], shell=True).decode().strip()


def post(color: Color, message: str):
    """post status to BB"""
    command = f'$BB $BBDISP "status SPOT.STATUS {color} {_date()} {message}"'
    subprocess.Popen(command, shell=True)
