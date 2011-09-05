#######################################################################
# This file is part of redminelib.
#
# Copyright (C) 2011 Will Kahn-Greene
#
# redminelib is distributed under the MIT license.  See the file
# COPYING for distribution details.
#######################################################################

# this has blockers and related bugs

from redminelib.redmine import RedmineScraper
from redminelib.tests import utils


import os

from nose.tools import eq_


def test_491():
    rs = RedmineScraper("")
    data = open(os.path.join(utils.get_testdata(), "491.html")).read()
    issue = rs.parse_issue(data)

    # extracted
    eq_(issue["id"], "491")
    eq_(issue["title"], "Contributors to the code may be surprised to learn of PEP-8")
    eq_(issue["author"], "Caleb Davis")
    eq_(issue["creation-date"], "08/10/2011 02:32 pm")
    eq_(issue["last-updated-date"], "09/04/2011 09:44 am")

    eq_(issue["description"], "I know I was...There are places in redmine mentioning PEP-8 style guidelines\n([http://www.python.org/dev/peps/pep-0008/][1]), but there is no prominent\nmention in the contributor docs. This suggestion just came up again in IRC.\nThis issue needs:\n\n  * decide where to mention and link to PEP-8\n  * add it to the contributor documentation\n\n   [1]: http://www.python.org/dev/peps/pep-0008/\n\n")

    # details table
    eq_(issue["priority"], "Normal")
    eq_(issue["status"], "New")
    eq_(issue["start-date"], "08/10/2011")
    eq_(issue["due-date"], "")
    eq_(issue["assigned-to"], "Will Kahn-Greene")
    eq_(issue["progress"], "0%")
    eq_(issue["category"], "Documentation")
    eq_(issue["fixed-version"], "0.1.0")

    # relations
    eq_(len(issue["relations"]), 0)

    # watchers
    eq_(len(issue["watchers"]), 2)
    eq_(issue["watchers"], ["Jim Campbell", "Will Kahn-Greene"])

    # history
    eq_(len(issue["history"]), 3)
    hist1 = issue["history"][0]
    eq_(hist1["date"], "08/11/2011 10:29 pm")
    eq_(hist1["author"], "Christopher Webber")
    props = hist1["properties"]
    eq_(len(props), 0)
    eq_(hist1["comment"], "[+ Jim Campbell, Will Kahn-Greene]\n\nI think we need a style guide page on the wiki altogether.\n\nMaybe that belongs on [http://wiki.mediagoblin.org/Code_style_guide][1] ?\n\n   [1]: http://wiki.mediagoblin.org/Code_style_guide\n\n")

    hist2 = issue["history"][1]
    eq_(hist2["date"], "09/04/2011 09:44 am")
    eq_(hist2["author"], "Will Kahn-Greene")
    props = hist2["properties"]
    eq_(len(props), 1)
    eq_(hist2["comment"], "Chris and I bandied about what should be in a code style guide for a bit now.\nI'll grab this bug and throw one together soon.\n\n")

    hist3 = issue["history"][2]
    eq_(hist3["date"], "09/04/2011 09:44 am")
    eq_(hist3["author"], "Will Kahn-Greene")
    props = hist3["properties"]
    eq_(len(props), 1)
    eq_(props[0], {
            "property": "Target version",
            "newvalue": "0.1.0",
            "oldvalue": "0.0.5"
            })

    eq_(hist3["comment"], "Bumping this to 0.1.0 since 0.0.5 is out now.\n\n")
