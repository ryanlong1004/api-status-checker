#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=missing-module-docstring

import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

required = ["click", "loguru==0.7.2"]

required_extras = {  # Optional
    "dev": [
        "check-manifest",
        "black",
        "pylint",
        "pytest",
        "pytest-cov",
        "pytest-xdist",
        "tox",
        "icecream",
    ],
    "test": ["pytest", "pytest-cov", "pytest-forked", "pytest-xdist", "tox"],
}

setup(
    name="<[Project Name]>",
    version="0.0.1",
    description="<[Project Name]> description",
    # long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Ryan Long",
    author_email="ryan.long@noaa.gov",
    url="",
    py_modules=["<[Project Name]>"],
    install_requires=required,
    tests_require=["pytest"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    extras_require=required_extras,
    packages=find_packages(),
)
