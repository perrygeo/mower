import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

setup(
    name="mower",
    version="0.1",
    author="Matthew Perry",
    author_email="perrygeo@gmail.com",
    description=("Tames GRASS GIS and makes working with pygrass fun again"),
    license="MIT",
    keywords="grass gis",
    url="https://github.com/perrygeo/mower",
    packages=["mower"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
