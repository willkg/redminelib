#######################################################################
# This file is part of redminelib.
#
# Copyright (C) 2011 Will Kahn-Greene
#
# redminelib is distributed under the MIT license.  See the file
# COPYING for distribution details.
#######################################################################

# tests attachments
# tests a history entry that has no comment


from redminelib.redmine import RedmineScraper
from redminelib.tests import get_testdata

import os

from nose.tools import eq_


def test_503():
    rs = RedmineScraper("http://bugs.foocorp.net/")
    data = open(os.path.join(get_testdata(), "503.html")).read()
    issue = rs.parse_issue(data)

    # extracted
    eq_(issue["id"], "503")
    eq_(issue["title"], 'If there are no next and previous media, the navigation buttons should not appear')
    eq_(issue["author"], "Jef van Schendel")
    eq_(issue["creation-date"], "08/20/2011 05:32 pm")
    eq_(issue["last-updated-date"], "08/22/2011 09:29 am")

    eq_(issue["description"], u'Speaks for itself. If you only have one piece of media for whatever reason,\nthe navigation still shows up. But both of the buttons are disabled, so they\nmay just as well be gone completely.\n\nI have no idea how hard this is to do though.\n\nAttached is a screenshot.\n\n')

    # details table
    eq_(issue["priority"], "Normal")
    eq_(issue["status"], "Feedback")
    eq_(issue["start-date"], "08/20/2011")
    eq_(issue["due-date"], "")
    eq_(issue["assigned-to"], "Caleb Davis")
    eq_(issue["progress"], "90%")
    eq_(issue["category"], "Programming")
    eq_(issue["fixed-version"], "-")

    # attachments
    eq_(len(issue["attachments"]), 1)
    att1 = issue["attachments"][0]

    eq_(att1["author"], "Jef van Schendel")
    eq_(att1["date"], "08/20/2011 05:32 pm")
    eq_(att1["url"], "http://bugs.foocorp.net/attachments/73/Screenshot-16.png")
    eq_(att1["name"], "Screenshot-16.png")

    # history
    eq_(len(issue["history"]), 5)

    hist1 = issue["history"][0]
    eq_(hist1["date"], "08/20/2011 05:33 pm")
    eq_(hist1["author"], "Jef van Schendel")
    props = hist1["properties"]
    eq_(len(props), 0)
    eq_(hist1["comment"], u'Typo in the ticket title: "not disappear" should of course be "not appear".\n\n')

    hist2 = issue["history"][1]
    eq_(hist2["date"], "08/20/2011 10:37 pm")
    eq_(hist2["author"], "Caleb Davis")
    props = hist2["properties"]
    eq_(props[0], {
            "property": "Subject",
            "oldvalue": "If there are no next and previous media, the navigation buttons should not disappear",
            "newvalue": "If there are no next and previous media, the navigation buttons should not appear"
            })
    eq_(hist2["comment"], "")

    hist3 = issue["history"][2]
    eq_(hist3["date"], "08/21/2011 01:18 am")
    eq_(hist3["author"], "Caleb Davis")
    props = hist3["properties"]
    eq_(len(props), 3)
    eq_(props[0], {
            "property": "Status",
            "oldvalue": "New",
            "newvalue": "Feedback",
            })
    eq_(props[1], {
            "property": "Assigned to",
            "oldvalue": "",
            "newvalue": "Caleb Davis",
            })
    eq_(props[2], {
            "property": "% Done",
            "oldvalue": "0",
            "newvalue": "50",
            })
    eq_(hist3["comment"], u"Jef, like this?\n\n[https://gitorious.org/~cfdv/mediagoblin/cfdvs-\nmediagoblin/commit/e3df834a8a22a45ba77940efbd083c7d5a23764e][1]\n\nEDIT: Chris pointed out you didn't want the Xs to go away completely, just in\nthe case where the user had one media item only. Oops! How about this one?\n\n[https://gitorious.org/~cfdv/mediagoblin/cfdvs-\nmediagoblin/commit/0a100476b24d81355342cae5320e1a5a6c83014d][2]\n\n   [1]: https://gitorious.org/~cfdv/mediagoblin/cfdvs-mediagoblin/commit/e3df834a8a22a45ba77940efbd083c7d5a23764e\n   [2]: https://gitorious.org/~cfdv/mediagoblin/cfdvs-mediagoblin/commit/0a100476b24d81355342cae5320e1a5a6c83014d\n\n")
