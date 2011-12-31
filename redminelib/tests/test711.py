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


def test_711():
    rs = RedmineScraper("")
    data = open(os.path.join(get_testdata(), "711.html")).read()
    issue = rs.parse_issue(data)

    # extracted
    eq_(issue["id"], "711")
    eq_(issue["title"], u'New feed library that uses lxml')
    eq_(issue["author"], u"Christopher Webber")
    eq_(issue["creation-date"], "12/14/2011 07:04 pm")
    eq_(issue["last-updated-date"], "12/14/2011 07:30 pm")

    eq_(issue["description"], u"We're finding that our present feeds aren't extensible enough and... well, we\nneed to extend them! Inconexo is already working on this in a branch:\n\n[https://gitorious.org/~inconexo/mediagoblin/inconexos-\nmediagoblin/commits/feed_library][1]\n\nI'll leave comments on that as I read through here.\n\n   [1]: https://gitorious.org/~inconexo/mediagoblin/inconexos-mediagoblin/commits/feed_library\n\n")

    # details table
    eq_(issue["priority"], "Normal")
    eq_(issue["status"], "New")
    eq_(issue["start-date"], "12/14/2011")
    eq_(issue["due-date"], "")
    eq_(issue["assigned-to"], u"Inconexo \xf8")
    eq_(issue["progress"], "0%")
    eq_(issue["category"], "Programming")
    eq_(issue["fixed-version"], "0.2.1")

    # history
    eq_(len(issue["history"]), 2)
    hist1 = issue["history"][0]
    eq_(hist1["date"], "12/14/2011 07:15 pm")
    eq_(hist1["author"], "Christopher Webber")
    props = hist1["properties"]
    eq_(len(props), 0)
