#######################################################################
# This file is part of redminelib.
#
# Copyright (C) 2011 Will Kahn-Greene
#
# redminelib is distributed under the MIT license.  See the file
# COPYING for distribution details.
#######################################################################

from setuptools import setup, find_packages
import re
import os


READMEFILE = "README"
VERSIONFILE = os.path.join("redminelib", "_version.py")
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"


def get_version():
    verstrline = open(VERSIONFILE, "rt").read()
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % VERSIONFILE)


setup(
    name="redminelib",
    version=get_version(),
    description="Redmine scraping library",
    long_description=open(READMEFILE).read(),
    license="MIT",
    author="Will Kahn-Greene",
    author_email="willg@bluesock.org",
    keywords="redmine scraper",
    zip_safe=True,
    packages=find_packages(),
    test_suite="nose.collector",
    install_requires=[
        "html2text",
        "nose",
        "lxml",
        ]
    )
