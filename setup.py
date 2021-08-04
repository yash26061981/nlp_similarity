"""
 *************************************************************************
 *
 * AUDIO FIRST COMMERCE PRIVATE LIMITED Confidential
 * Copyright (c) 2020 AUDIO FIRST COMMERCE PRIVATE LIMITED.
 * All Rights Reserved.
 *
 * NOTICE:  All information contained herein is, and remains the property of
 * AUDIO FIRST COMMERCE PRIVATE LIMITED and its suppliers, if any. The intellectual
 * and technical concepts contained herein are proprietary to AUDIO FIRST COMMERCE
 * PRIVATE LIMITED and its suppliers and may be covered by Indian and Foreign Patents,
 * patents in process, and are protected by trade secret or copyright law. Dissemination
 * of this information or reproduction of this material is strictly forbidden unless
 * prior written permission is obtained from AUDIO FIRST COMMERCE PRIVATE LIMITED.
 *
 *************************************************************************
"""

from setuptools import setup, find_packages
import pathlib, os
from src.nlpsim.get_updated_version import VersionManager
from pip._internal.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session='hack')

# reqs is a list of requirement
reqs = [str(ir.requirement) for ir in install_reqs]

root = pathlib.Path(__file__).parent
os.chdir(str(root))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = VersionManager().get_version()

setup(
    name='nlpsim',
    version=version,
    description='NLP Based Similarity',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='HiVOCO',
    author_email='n/a',
    url="https://github.com/yash26061981/nlp_similarity",
    project_urls={
        "Bug Tracker": "https://github.com/yash26061981/nlp_similarity/issues",
    },
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=True,
    packages=find_packages(where='src'),
    include_package_data=True,
    python_requires='>=3.6, <4',
    install_requires=reqs,
)
