import asyncio
import socket
from typing import Any
import json
import httpx
from loguru import logger
from mail import email
import datetime

logger.add(
    "/usr1/rlong/api-status-checker/LOG",
    level="DEBUG",
    colorize=False,
    backtrace=True,
    diagnose=True,
)

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
        response = httpx.get(url, headers=headers, timeout=10)
        result = CheckResult(
            name,
            url,
            response.status_code,
            response.content if response.status_code != 200 else None,
        )
        if result.status_code != 200:
            logger.error(result)
            email(
                "ryan.long@noaa.gov",
                f"API Failure {datetime.datetime.now().isoformat()}",
                str(result),
            )
            # email("kyle.nevins@noaa.gov", f"API Failure {datetime.datetime.now().isoformat()}", str(result))
        logger.info(result)

    except (socket.timeout, httpx.ReadTimeout) as e:
        result = CheckResult(name, url, 1, str(e))
        logger.error(CheckResult(name, url, 1, str(e)))
        email("ryan.long@noaa.gov", "API Failure", str(result))


async def main():
    """main execution"""
    logger.info("starting...")
    with open(
        "/usr1/rlong/api-status-checker/queue.json", "r", encoding="utf-8"
    ) as _input:
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
