"""Instansiate the package."""

from os import path

__version__ = open(path.join(path.dirname(__file__), "VERSION"), "rt").read()
