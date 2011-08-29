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


def test_519():
    rs = RedmineScraper()
    data = open(os.path.join(utils.get_testdata(), "519.html")).read()
    issue = rs.parse_issue(data)

    # extracted
    eq_(issue["title"], u"CloudFilesStorage.get_file() performance issue.")
    eq_(issue["author"], u"Joar Wandborg")
    eq_(issue["priority"], u"Normal")

    # details table
    eq_(issue["priority"], "Normal")
    eq_(issue["status"], "Closed")
    eq_(issue["start-date"], "08/24/2011")
    eq_(issue["due-date"], "")
    eq_(issue["assigned-to"], "Christopher Webber")
    eq_(issue["progress"], "50%")
    eq_(issue["category"], "Programming")
    eq_(issue["fixed-version"], "0.0.5")

