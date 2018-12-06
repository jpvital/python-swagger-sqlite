# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "src"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="Factory product management",
    author_email="joao.campos18@gmail.com",
    url="",
    keywords=["Swagger", "Factory product management"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['src=src.__main__:main']},
    long_description="""\
    This is a sample factory inventory product management server.
    """
)

