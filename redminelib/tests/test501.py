#######################################################################
# This file is part of redminelib.
#
# Copyright (C) 2011 Will Kahn-Greene
#
# redminelib is distributed under the MIT license.  See the file
# COPYING for distribution details.
#######################################################################

from redminelib.redmine import RedmineScraper
from redminelib.tests import utils

import os

from nose.tools import eq_

def test_501():
    rs = RedmineScraper()
    data = open(os.path.join(utils.get_testdata(), "501.html")).read()
    issue = rs.parse_issue(data)

    eq_(issue["title"], "Inconsistent font size specifications in css")
    eq_(issue["author"], "Jef van Schendel")

    # eq_(issue["title"], u"CloudFilesStorage.get_file() performance issue.")
    # eq_(issue["author"], u"Joar Wandborg")
    eq_(issue["priority"], u"Normal")

