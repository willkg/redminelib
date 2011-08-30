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

    eq_(issue["description"], u'For the thumb listings such as the index page, gallery page a call to\ncloudfiles is made for every thumbnail on the page.\n\nCloudFilesStorage should be changed to save container_url on _init_, and then\nuse self._resolve_filepath() to generate the filepath without verifying that\nthe file exists, just like BasicFileStorage does.\n\n')

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
    eq_(hist1["comment"], u'Hi Christopher, merge request filed at\n[https://gitorious.org/mediagoblin/mediagoblin/merge_requests/19][1]\n\nFeedback if any much appreciated.\n\nCheers,\n\n   [1]: https://gitorious.org/mediagoblin/mediagoblin/merge_requests/19\n\n')

    hist2 = issue["history"][1]
    eq_(hist2["date"], "08/27/2011 10:07 pm")
    eq_(hist2["author"], "Christopher Webber")
    props = hist2["properties"]
    eq_(props[0], {
            "property": "Status",
            "oldvalue": "Feedback",
            "newvalue": "Closed"
            })
    eq_(hist2["comment"], "Merged!\n\n")
