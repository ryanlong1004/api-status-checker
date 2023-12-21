import httpx
from loguru import logger

ENDPOINT = 'https://cat-fact.herokuapp.com/facts'

def main():
    """main execution"""
    logger.info("starting...")
    r = httpx.get(ENDPOINT)
    logger.info("complete...")
    print(r.status_code)


if __name__ == "__main__":
    main()
