#!/usr/bin/env python
""" 
This Python script is a convenience executor using the click library, which allows running various commands related to Python project development, testing, packaging, and publishing.

This script defines several commands (test, format, serve, publish, packaging) using the click library to perform different tasks related to Python project management. These tasks include running tests, formatting code, starting a development server, publishing the project to PyPI, and opening documentation in the web browser. The cli() function acts as the entry point and runs the specified command based on user input from the command line.
"""

import subprocess
import webbrowser
import click
import sys


def run(cmd):
    return subprocess.run(cmd.split(), shell=True, check=True)


@click.command
def test():
    """run testing suites"""
    return run("pytest")


@click.command
def format():
    """run black"""
    return run(f"black --line-length 100 .")


@click.command
@click.option("--port", default=8000, help="specify a port number")
def serve(port=8000):
    """spins up a development server"""
    return run(f"{sys.executable} -m http.server {port}")


@click.command
def publish():
    """publish the project to Pypi"""
    return run(f"{sys.executable} setup.py sdist bdist_wheel upload")


@click.command
def packaging():
    """open packaging documentation in the browser"""
    webbrowser.open("https://packaging.python.org/en/latest/")


@click.group()
def cli():
    pass


cli.add_command(packaging)
cli.add_command(test)
cli.add_command(serve)
cli.add_command(publish)
cli.add_command(format)

if __name__ == "__main__":
    cli()
