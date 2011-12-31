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


def test_716():
    rs = RedmineScraper("")
    data = open(os.path.join(get_testdata(), "716.html")).read()
    issue = rs.parse_issue(data)

    # extracted
    eq_(issue["id"], "716")
    eq_(issue["title"], u'Apache FCGI documentation In Manual')
    eq_(issue["author"], u"Sam Kleinman")
    eq_(issue["creation-date"], "12/20/2011 10:23 am")
    eq_(issue["last-updated-date"], "12/22/2011 06:29 pm")

    eq_(issue["description"], u'')

    # details table
    eq_(issue["priority"], "Normal")
    eq_(issue["status"], "New")
    eq_(issue["start-date"], "12/20/2011")
    eq_(issue["due-date"], "")
    eq_(issue["assigned-to"], "Sam Kleinman")
    eq_(issue["progress"], "0%")
    eq_(issue["category"], "Documentation")
    eq_(issue["fixed-version"], "-")

    # history
    eq_(len(issue["history"]), 1)
    hist1 = issue["history"][0]
    eq_(hist1["date"], "12/22/2011 06:29 pm")
    eq_(hist1["author"], "Blaise Alleyne")
    props = hist1["properties"]
    eq_(len(props), 0)
