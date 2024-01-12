"""main execution"""
import asyncio
import datetime
import os
import socket
from typing import Any, List
import json
import httpx

from loguru import logger
from dotenv import load_dotenv

from mail import email
import bb

load_dotenv()

logger.add(
    "/usr1/rlong/api-status-checker/LOG",
    rotation="7 days",
    compression="zip",
    retention="30 days",
    colorize=False,
    backtrace=True,
    diagnose=False,
    enqueue=True,
    level="INFO",
)

HEADERS = {
    "accept": "application/ld+json",
    "Authorization": os.getenv("STATUS_CHECKER_KEY"),
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
    logger.debug(f"testing {name}@{url}")
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
    """logs the results and return failed result messages"""
    errors = []
    for result in results:
        message = f"{result.status_code}:{result}"
        if result.status_code != 200:
            logger.error(message)
            errors.append(message)
            continue
        logger.info(message)
    return errors


def handle_email(email_to: str, errors: List[str]) -> None:
    """emails failures to receipient"""
    email(
        email_to,
        f"API Failure {datetime.datetime.now().isoformat()}",
        "\n".join(errors),
    )


def handle_big_brother(errors):
    """report number of issues to BB"""
    if errors:
        bb.post(bb.Color.RED, f"{len(errors)} issues reported")
    else:
        bb.post(bb.Color.GREEN, "no current issues")


async def run_checks(endpoints):
    """runs checks async and returns total results"""
    with httpx.Client() as client:
        return await asyncio.gather(
            *[
                to_job(check_endpoint, name, endpoint, HEADERS, client)
                for name, endpoint in endpoints.items()
            ]
        )


EMAIL_TO = os.getenv("STATUS_CHECKER_EMAIL")


async def main():
    """main execution"""

    logger.info("starting...")
    with open(
        "/usr1/rlong/api-status-checker/queue.json", "r", encoding="utf-8"
    ) as _input:
        endpoints = json.load(_input)
        results = await run_checks(endpoints)

        errors = handle_check_results(results)
        # handle_big_brother(errors)

        email_to = os.getenv("STATUS_CHECKER_EMAIL")
        if not email_to:
            raise ValueError(f"invalid email address {email_to}")

        handle_email(email_to, errors)

        logger.info("finished")


if __name__ == "__main__":
    asyncio.run(main())
