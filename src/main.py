import asyncio
import socket
from typing import Any
import json
import httpx
from loguru import logger

HEADERS = {
    "accept": "application/ld+json",
    "Authorization": "spotp_10499d9479d32dc3530161b9fc569297f32cdc287c7ba33ebdc45a99aab6aff5",
}


async def to_job(fx, *params):
    return await asyncio.to_thread(fx, *params)


class CheckResult:
    def __init__(self, name, url, status_code, content):
        self.name = name
        self.url = url
        self.status_code = status_code
        self.content = content

    @property
    def result(self):
        return "PASS" if self.status_code == 200 else "FAIL"

    def __str__(self):
        return f"{self.result}: {self.name} {self.content if self.content else ''}"


def check_endpoint(name: str, url: str, headers: dict[str, Any]):
    try:
        r = httpx.get(url, headers=headers, timeout=10)
        result = CheckResult(name, url, r.status_code, r.content if r.status_code != 200 else None)
        if result.status_code != 200:
            logger.error(result)
        logger.info(result)

    except (socket.timeout, httpx.ReadTimeout) as e:
        logger.error(CheckResult(name, url, 1, str(e)))


async def main():
    """main execution"""
    logger.info("starting...")
    with open("./queue.json", "r", encoding="utf-8") as _input:
        endpoints = json.load(_input)
        await asyncio.gather(
            *[
                to_job(check_endpoint, name, endpoint, HEADERS)
                for name, endpoint in endpoints.items()
            ]
        )
        logger.info("finished")


if __name__ == "__main__":
    asyncio.run(main())
