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


def test_733():
    rs = RedmineScraper("")
    data = open(os.path.join(get_testdata(), "733.html")).read()
    issue = rs.parse_issue(data)

    # extracted
    eq_(issue["id"], "733")
    eq_(issue["title"], u'Comment-field-opening \u201cAdd one\u201d button is useless/broken/confusing when JavaScript is disabled')
    eq_(issue["author"], u'Aleksej Serdjukov')
    eq_(issue["creation-date"], u'01/08/2012 10:24 am')
    eq_(issue["last-updated-date"], u'01/10/2012 09:41 am')

    eq_(issue["description"], u'The button (right above the comment field) is intended for users who will have\nto log in to comment. (\n\n')

    # details table
    eq_(issue["priority"], "Normal")
    eq_(issue["status"], "New")
    eq_(issue["start-date"], "01/08/2012")
    eq_(issue["due-date"], "")
    eq_(issue["assigned-to"], "Jef van Schendel")
    eq_(issue["progress"], "0%")
    eq_(issue["category"], "Programming")
    eq_(issue["fixed-version"], "-")

    # history
    eq_(len(issue["history"]), 6)

    hist1 = issue["history"][0]
    eq_(hist1["date"], "01/08/2012 10:41 am")
    eq_(hist1["author"], "Jef van Schendel")
    props = hist1["properties"]
    eq_(len(props), 0)

    hist2 = issue["history"][1]
    eq_(hist2["date"], "01/08/2012 11:00 am")
    eq_(hist2["author"], "Aleksej Serdjukov")
    props = hist2["properties"]
    eq_(len(props), 0)

    # Skip the other history items--they're like other tests.
