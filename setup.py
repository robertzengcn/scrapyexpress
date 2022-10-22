#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from setuptools import setup
from setuptools import find_packages



version = re.search(
    "^__version__\s*=\s*'(.*)'",
    open('version.py').read(),
    re.M).group(1)

requirements = [r for r in open('requirements.txt', 'r').read().split('\n') if r]
# with open('requirements.txt') as f:
#     required = f.read().splitlines()
# https://dustingram.com/articles/2018/03/16/markdown-descriptions-on-pypi

setup(name='scrapyexpress',
      version=version,
      description='A module to scrape product from aliexpress site',
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      include_package_data=True,
      author='Robert Zeng',
      author_email='zengjianze@gmail.com',
      packages=find_packages(),
      entry_points={'console_scripts': ['scrapyexpress = core:main']},
      install_requires=requirements,
      python_requires='>=3.9',
)
