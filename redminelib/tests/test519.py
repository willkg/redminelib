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
    eq_(issue["id"], "519")
    eq_(issue["title"], u"CloudFilesStorage.get_file() performance issue.")
    eq_(issue["author"], u"Joar Wandborg")
    eq_(issue["creation-date"], "08/24/2011 06:08 pm")
    eq_(issue["last-updated-date"], "08/27/2011 10:07 pm")

    # details table
    eq_(issue["priority"], "Normal")
    eq_(issue["status"], "Closed")
    eq_(issue["start-date"], "08/24/2011")
    eq_(issue["due-date"], "")
    eq_(issue["assigned-to"], "Christopher Webber")
    eq_(issue["progress"], "50%")
    eq_(issue["category"], "Programming")
    eq_(issue["fixed-version"], "0.0.5")

    # history
    # there are two changes
    eq_(len(issue["history"]), 2)
    hist1 = issue["history"][0]
    eq_(hist1["date"], "08/24/2011 07:14 pm")
    eq_(hist1["author"], "Joar Wandborg")
    props = hist1["properties"]
    eq_(props[0], {
            "property": "Status",
            "oldvalue": "New",
            "newvalue": "Feedback"
            })
    eq_(props[1], {
            "property": "Assigned to",
            "oldvalue": "Joar Wandborg",
            "newvalue": "Christopher Webber"
            })
    eq_(props[2], {
            "property": "% Done",
            "oldvalue": "0",
            "newvalue": "50"
            })
    eq_(hist1["comment"], '<div class="wiki" id="journal-1352-notes"><p>Hi Christopher, merge request filed at <a class="external" href="https://gitorious.org/mediagoblin/mediagoblin/merge_requests/19">https://gitorious.org/mediagoblin/mediagoblin/merge_requests/19</a></p>\n\n\n\t<p>Feedback if any much appreciated.</p>\n\n\n\t<p>Cheers,</p></div>\n  ')

    hist2 = issue["history"][1]
