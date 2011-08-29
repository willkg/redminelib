#######################################################################
# This file is part of redminelib.
#
# Copyright (C) 2011 Will Kahn-Greene
#
# redminelib is distributed under the MIT license.  See the file
# COPYING for distribution details.
#######################################################################


import sys
import httplib
import urllib
import csv
from urlparse import urlparse, urljoin
from StringIO import StringIO
import lxml.etree
import lxml.html


class RedmineScraper:
    """
    RedmineScraper class that allows you to navigate and parse issues
    for a project in Redmine.
    """

    def parse_issue(self, data):
        """Takes in a string of an issue page in html, parses it, and
        returns a dict containing all the useful stuff.
        """
        issue = {}

        tree = lxml.html.parse(StringIO(data))
        root = tree.getroot()

        topdivs = root.findall(".//div")
        history = None
        details = None
        for mem in topdivs:
            if "details" in mem.attrib.get("class", ""):
                details = mem
            elif mem.attrib.get("id", "") == "history":
                history = mem

        if details is None:
            raise ValueError("No details section in this bug?")

        title = details.find(".//h3")
        issue["title"] = title.text

        author_and_date = details.findall(".//p[@class='author']//a")
        issue["author"] = author_and_date[0].text
        issue["creation_date"] = author_and_date[1].attrib["title"]

        # the attributes table in redmine has td elements that have
        # semantic class names.  for example, one td has a class name
        # of "status".
        #
        # i abuse that fact to just grab all the data in key/value pairs.
        attributes = details.find(".//table[@class='attributes']")
        tds = attributes.findall(".//td")
        for mem in tds:
            issue[mem.attrib["class"]] = mem.text

        desc = details.find(".//div[@class='wiki']")
        # FIXME - should convert this to something useful somehow
        issue["description"] = lxml.etree.tostring(desc, pretty_print=True).strip()

        if history is not None:
            changes = history.findall(".//div[@class='journal']")
            for change in changes:
                print change

        print issue


    def get_issue(self, url):
        parsedurl = urlparse(url)
        path = parsedurl.path

        conn = httplib.HTTPConnection(parsedurl.hostname, parsedurl.port)
        conn.request("GET", path)
        resp = conn.getresponse()

        if resp.status != 200:
            raise ValueError("Bad url?: Error: status: %s reason: %s",
                             resp.status, resp.reason)

        return self.parse_issue(resp.read())


    def parse_issues(self, data):
        """Takes in a string of the list of issues as a csv file and
        returns a list of issue dicts.

        The string should be a csv file of issues where the first line
        is the headers and columns are delimited by commas and quoted
        by double-quotes.

        :param data: csv file data as a big string

        :returns: list of dicts each representing an issue
        """
        reader = csv.DictReader(StringIO(data), delimiter=",", quotechar='"')
        return [row for row in reader]


    def get_open_issues(self, url):
        """Fetches the issues.csv file, parses it, and returns the
        list of open issues.

        :returns: list of dicts each representing an issue
        """
        parsedurl = urlparse(url)
        path = parsedurl.path

        conn = httplib.HTTPConnection(parsedurl.hostname, parsedurl.port)
        conn.request("GET", path)
        resp = conn.getresponse()

        if resp.status != 200:
            raise ValueError("Bad url?: Error: status: %s reason: %s",
                             resp.status, resp.reason)

        return self.parse_issues(resp.read())
