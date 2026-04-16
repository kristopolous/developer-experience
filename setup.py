#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

readme = open('README.md').read()
with open('requirements-dev.txt') as f:
    required_dev = f.read().splitlines()
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='hackernews-cli',
    version='1.0.0',
    description='Read HackerNews like a hacker',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Kamil Chmielewski',
    author_email='kamil.chm@gmail.com',
    url='https://github.com/kamilchm/developer-experience',
    license="Apache License (2.0)",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=required,
    entry_points={
        'console_scripts': [
            'hn = hncli.cli:cli',
        ],
    },
)
