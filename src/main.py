import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    handlers=[logging.FileHandler("archive_results.log"), logging.StreamHandler()],
)


def add_two(value: int) -> int:
    """adds 2 to value and returns"""
    return value + 2


def main():
    """main execution"""


if __name__ == "__main__":
    pass
