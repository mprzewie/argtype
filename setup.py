from distutils.core import setup

from setuptools import find_packages

setup(
    name="argtype",
    version="0.0",
    packages=find_packages(exclude=["test"]),
    url="",
    license="",
    author="Marcin Przewięźlikowski",
    author_email="",
    description="Converting NamedTuples to ArgParser",
)
