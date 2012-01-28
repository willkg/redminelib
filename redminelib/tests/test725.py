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


def test_725():
    rs = RedmineScraper("")
    data = open(os.path.join(get_testdata(), "725.html")).read()
    issue = rs.parse_issue(data)

    # extracted
    eq_(issue["id"], "725")
    eq_(issue["title"], u"atom feed shows a wrong URL when using apache with mod_proxy")
    eq_(issue["author"], u"Michele Azzolari")
    eq_(issue["creation-date"], "12/28/2011 06:44 pm")
    eq_(issue["last-updated-date"], "12/29/2011 09:45 am")

    eq_(issue["description"], u'Setup: I have a virtual host for media.macno.org and I use mod_proxy to access my mediagoblin server (which listen on 127.0.0.1:6543)\n\nIssue: atom feed self link uses a wrong url\n\nFor example requesting [http://media.macno.org/u/macno/atom/][1] returns <link href="http://127.0.0.1:6543/u/macno/atom/" rel="self" />\n\n   [1]: http://media.macno.org/u/macno/atom/\n\n')

    # details table
    eq_(issue["priority"], "Normal")
    eq_(issue["status"], "New")
    eq_(issue["start-date"], "12/28/2011")
    eq_(issue["due-date"], "")
    eq_(issue["assigned-to"], "-")
    eq_(issue["progress"], "0%")
    eq_(issue["category"], "-")
    eq_(issue["fixed-version"], "-")

    # history
    eq_(len(issue["history"]), 1)
    hist1 = issue["history"][0]
    eq_(hist1["date"], "12/29/2011 09:45 am")
    eq_(hist1["author"], "Michele Azzolari")
    props = hist1["properties"]
    eq_(len(props), 0)
