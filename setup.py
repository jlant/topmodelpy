#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.rst") as changelog_file:
    changelog = changelog_file.read()

with open("LICENSE") as license_file:
    license = license_file.read()


requirements = [
    "click",
    "numpy",
    "pandas",
]

test_requirements = [
    "pytest",
]


setup(
    name="topmodelpy",
    version="0.1",
    description=("A rainfall-runoff model that predicts the amount "
                 "of water flow in rivers."),
    long_description=readme + "\n\n" + changelog,
    author="Jeremiah Lant",
    author_email="jlant@usgs.gov",
    url="",
    packages=[
        "topmodelpy",
    ],
    package_dir={"topmodelpy": "topmodelpy"},
    entry_points={"console_scripts": ["topmodelpy = topmodelpy.cli:main"]},
    include_package_data=True,
    install_requires=requirements,
    license=license,
    zip_safe=False,
    keywords="topmodelpy",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    test_suite="tests",
    tests_require=test_requirements
)
