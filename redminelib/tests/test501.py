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
    eq_(issue["id"], "501")
    eq_(issue["title"], "Inconsistent font size specifications in css")
    eq_(issue["author"], "Jef van Schendel")
    eq_(issue["creation-date"], "08/16/2011 05:20 pm")

    # details table
    eq_(issue["priority"], "Normal")
    eq_(issue["status"], "Closed")
    eq_(issue["start-date"], "08/16/2011")
    eq_(issue["due-date"], "")
    eq_(issue["assigned-to"], "Jef van Schendel")
    eq_(issue["progress"], "0%")
    eq_(issue["category"], "Graphic Design / UI")
    eq_(issue["fixed-version"], "0.0.5")

    # history

    # there's only one history item and it's a status change from New
    # to Closed with a comment.
    eq_(len(issue["history"]), 1)
    hist1 = issue["history"][0]
    eq_(hist1["date"], "08/18/2011 11:30 am")
    eq_(hist1["author"], "Jef van Schendel")
    prop = hist1["properties"][0]
    eq_(prop["property"], "Status")
    eq_(prop["oldvalue"], "New")
    eq_(prop["newvalue"], "Closed")
    eq_(hist1["comment"], '''<div class="wiki" id="journal-1292-notes"><p>This has been fixed. We now use relative sizes (em) everywhere.</p>\n\n\n\t<p>I\'ve also cleaned up a few things: removed some unnecssary text size values and added some spacing.</p></div>\n  ''')
