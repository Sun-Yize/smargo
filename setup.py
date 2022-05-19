#! /usr/bin/env python3

from setuptools import setup, find_packages


setup(
    name="smargo",
    version="0.1.0",
    description="Python Smart Tsumego Solver",
    author="sunyize",
    author_email="sunyize@163.com",
    url="https://github.com/Sun-Yize-SDUWH/smargo",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "tqdm",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6",
)
