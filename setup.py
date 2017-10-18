#!/usr/bin/env python3

from setuptools import setup, find_packages
from os         import path
import sys

if sys.version_info < (3, 2):
    print('whale-linter requires at least Python 3.2 to run.')
    sys.exit(1)

here = path.abspath(path.dirname(__file__))

version = '0.0.7'

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='whale-linter',
    version=version,
    packages=find_packages(),
    install_requires=requirements,
    scripts=['bin/whale-linter'],
    author="Jerome Pin",
    author_email="jerome@jeromepin.fr",
    maintainer="Jerome Pin",
    maintainer_email="jerome@jeromepin.fr",
    description="A simple non professional Dockerfile linter",
    long_description='',
    include_package_data=True,
    zip_safe = False,
    license='MIT',
    url='https://github.com/jeromepin/whale-linter',
    download_url='https://github.com/jeromepin/whale-linter/tarball/' + version,
    keywords=['docker', 'linter'],
    platforms='Linux',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "Intended Audience :: System Administrators"
    ]
)
