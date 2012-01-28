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


def test_383():
    """Tests that comments aren't getting wrapped"""
    rs = RedmineScraper("")
    data = open(os.path.join(get_testdata(), "383.html")).read()
    issue = rs.parse_issue(data)

    # extracted
    eq_(issue["id"], "383")

    # history
    eq_(len(issue["history"]), 1)
    hist1 = issue["history"][0]
    eq_(hist1["date"], "06/17/2011 05:46 pm")
    eq_(hist1["author"], "Jef van Schendel")
    eq_(hist1["comment"], 
        u"Hi there!\n\nAs pointed out on IRC, instead of copying the rest of the website, a black-on-white color scheme will be a better choice due to the large amounts of text in the docs.\n\nI've made a quick mockup using the colors we have right now, but with the background and text colors switched:\n\n[http://schendje.fedorapeople.org/goblin/docsTest.png][1]  \n[http://schendje.fedorapeople.org/goblin/docsTest.svg][2]\n\nI think that's a good start. As soon as I decide on the final color scheme for the website, I'll use it to make a matching one for the docs. But it'll probably look similar to this. :)\n\nJef\n\n   [1]: http://schendje.fedorapeople.org/goblin/docsTest.png\n   [2]: http://schendje.fedorapeople.org/goblin/docsTest.svg\n\n")
    props = hist1["properties"]
    eq_(len(props), 0)
