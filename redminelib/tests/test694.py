#######################################################################
# This file is part of redminelib.
#
# Copyright (C) 2011 Will Kahn-Greene
#
# redminelib is distributed under the MIT license.  See the file
# COPYING for distribution details.
#######################################################################

from redminelib.redmine import RedmineScraper
from redminelib.tests import get_testdata

import os

from nose.tools import eq_


def test_694():
    rs = RedmineScraper("")
    data = open(os.path.join(get_testdata(), "694.html")).read()
    issue = rs.parse_issue(data)

    # extracted
    eq_(issue["id"], "694")
    eq_(issue["title"], u"On submit page, show the site's filesize limit")
    eq_(issue["author"], u"Greg Grossmeier")
    eq_(issue["creation-date"], "12/04/2011 02:02 pm")
    eq_(issue["last-updated-date"], "12/04/2011 02:02 pm")

    eq_(issue["description"], u'It is convenient for the user to know how big of a file they can upload before they try.\n')

    # details table
    eq_(issue["priority"], "Normal")
    eq_(issue["status"], "New")
    eq_(issue["start-date"], "12/04/2011")
    eq_(issue["due-date"], "")
    eq_(issue["assigned-to"], "-")
    eq_(issue["progress"], "0%")
    eq_(issue["category"], "Graphic Design / UI")
    eq_(issue["fixed-version"], "-")

    # history
    eq_(len(issue["history"]), 0)
