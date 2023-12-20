# pylint: disable=all
from src.main import add_two


def test_add_two():
    expected = 8
    actual = add_two(6)
    assert expected == actual


def test_add_two_to_ten():
    expected = 12
    actual = add_two(10)
    assert expected == actual
