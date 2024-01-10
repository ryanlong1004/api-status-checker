import asyncio
import os
import socket
from typing import Any, List
import json
import httpx
from loguru import logger
from mail import email
import datetime
from dotenv import load_dotenv

load_dotenv()

EMAIL_TO = os.getenv("STATUS_CHECKER_EMAIL")

logger.add(
    "/usr1/rlong/api-status-checker/LOG",
    level="DEBUG",
    colorize=False,
    backtrace=True,
    diagnose=True,
)

HEADERS = {
    "accept": "application/ld+json",
    "Authorization": "spotp_fd14ed9b418c8d9d10eceafab8048135021e5d188cb59e12ba03a3eff02c5bbf",
}


async def to_job(fx, *params):
    """enables regular functions to run async"""
    return await asyncio.to_thread(fx, *params)


class CheckResult:
    """represents the results of a url check"""

    def __init__(self, name, url, status_code, content):
        self.name = name
        self.url = url
        self.status_code = status_code
        self.content = content

    @property
    def result(self):
        """returns the result as eith 'PASS' or 'FAIL'"""
        return "PASS" if self.status_code == 200 else "FAIL"

    def __str__(self):
        return f"{self.result}: {self.name} {self.content if self.content else ''}"


def check_endpoint(
    name: str, url: str, headers: dict[str, Any], client
) -> "CheckResult":
    """hits the url with a get request and returns the results as a CheckResult"""
    try:
        response = client.get(url, headers=headers, timeout=10)
        return CheckResult(
            name,
            url,
            response.status_code,
            response.content if response.status_code != 200 else None,
        )

    except (socket.timeout, httpx.ReadTimeout) as e:
        return CheckResult(name, url, 408, str(e))


def handle_check_results(results: List[CheckResult]):
    """logs the results and sends an email of all failed results"""
    errors = []
    for result in results:
        message = f"{result.status_code}:{result}"
        if result.status_code != 200:
            logger.error(message)
            errors.append(message)
            continue
        logger.info(message)
    email(
        EMAIL_TO,
        f"API Failure {datetime.datetime.now().isoformat()}",
        "\n".join(errors),
    )


async def main():
    """main execution"""
    logger.info("starting...")
    with open(
        "/usr1/rlong/api-status-checker/queue.json", "r", encoding="utf-8"
    ) as _input:
        endpoints = json.load(_input)
        results = []
        with httpx.Client() as client:
            results = await asyncio.gather(
                *[
                    to_job(check_endpoint, name, endpoint, HEADERS, client)
                    for name, endpoint in endpoints.items()
                ]
            )
        handle_check_results(results)
        logger.info("finished")


if __name__ == "__main__":
    asyncio.run(main())
