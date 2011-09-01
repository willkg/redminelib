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


def test_476():
    rs = RedmineScraper()
    data = open(os.path.join(utils.get_testdata(), "476.html")).read()
    issue = rs.parse_issue(data)

    # extracted
    eq_(issue["id"], "476")
    eq_(issue["title"], "tag clouds")
    eq_(issue["author"], "Caleb Davis")
    eq_(issue["creation-date"], "08/03/2011 12:33 pm")
    eq_(issue["last-updated-date"], "08/03/2011 12:37 pm")

    eq_(issue["description"], u"This is another rollover from [#360][1], but it got left behind somehow. A tag\ncloud is a dict-like object containing {'tag-name':frequency-of-use,...}. It's\nfun to have them to see all the tags that people are using publicly on an\ninstance.\n\nWhere would we display these?\n\n  * instance home page - all users, processed media\n  * user's profile - user's processed media\n  * [BONUS] - arbitrary collection (/tags/bunnies)\n\nOpen questions:\n\n  * Should we use MapReduce? [http://cookbook.mongodb.org/patterns/count_tags/][2] The alternative would be to write tags to a text file and do \n    \n    sort tags_text_file | uniq -c\n\nor do it completely within python\n\n  * Should we use celery? Generating tag clouds shouldn't slow page renders. Thoughts:\n\n> do it with python if you're using MapReduce since, if MapReduce gets too\nslow, you just add more processors!\n\n> if it 'takes too long', then use celery\n\n  * How often do we update the clouds? Thoughts included:\n\n> not during a bulk upload\n\n  * How do we store these tag cloud objects? If we're not rendering them on the fly, then they should be in some kind of cache. Thoughts:\n\n> user['tag_cloud'] = dict\n\n> associate the cloud with the route. something like - {'/':'instance_cloud.tx\nt','/u/user1':'user1_cloud.txt','/tags/bunnies':'tags_bunnies.txt'}\n\n   [1]: /issues/360 (tagging (Closed))\n   [2]: http://cookbook.mongodb.org/patterns/count_tags/\n\n")

    # details table
    eq_(issue["priority"], "Normal")
    eq_(issue["status"], "New")
    eq_(issue["start-date"], "08/03/2011")
    eq_(issue["due-date"], "")
    eq_(issue["assigned-to"], "-")
    eq_(issue["progress"], "0%")
    eq_(issue["category"], "Programming")
    eq_(issue["fixed-version"], "0.0.5")

    # FIXME - add tests for blockers and related bugs

    # history
    # there's one change
    eq_(len(issue["history"]), 1)
    hist1 = issue["history"][0]
    eq_(hist1["date"], "08/03/2011 12:37 pm")
    eq_(hist1["author"], "Caleb Davis")
    props = hist1["properties"]
    eq_(len(props), 0)
    eq_(hist1["comment"],  u"I haven't gone through the code in this one yet, but the feature set is\ninteresting: [http://pypi.python.org/pypi/cs.tags][1]\n\n   [1]: http://pypi.python.org/pypi/cs.tags\n\n")