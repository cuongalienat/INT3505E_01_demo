# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion",
    "swagger-ui-bundle>=0.0.2"
]

setup(
    name=NAME,
    version=VERSION,
    description="Library Management API (v1)",
    author_email="",
    url="",
    keywords=["Swagger", "Library Management API (v1)"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    REST API cho hệ thống quản lý thư viện — phiên bản v1   Bao gồm quản lý người dùng, sách, mượn/trả sách, xác thực JWT, và khởi tạo database. 
    """
)
