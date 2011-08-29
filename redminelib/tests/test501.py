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

    # extracted
    eq_(issue["title"], "Inconsistent font size specifications in css")
    eq_(issue["author"], "Jef van Schendel")
    eq_(issue["creation_date"], "08/16/2011 05:20 pm")

    # details table
    eq_(issue["priority"], "Normal")
    eq_(issue["status"], "Closed")
    eq_(issue["start-date"], "08/16/2011")
    eq_(issue["due-date"], "")
    eq_(issue["assigned-to"], "Jef van Schendel")
    eq_(issue["progress"], "0%")
    eq_(issue["category"], "Graphic Design / UI")
    eq_(issue["fixed-version"], "0.0.5")
