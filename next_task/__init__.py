"""Instansiate the package."""

from os import path

from .services.logging import logger, logging

logging()

__version__ = open(path.join(path.dirname(__file__), "VERSION"), "rt").read()
