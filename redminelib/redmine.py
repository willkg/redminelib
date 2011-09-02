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
from html2text import html2text

def textify(doc):
    """Takes a doc Element and returns it stringified, stripped, and
    then converted to Markdown.

    :param doc: doc Element

    :returns: the data formated in Markdown as a string
    """
    return html2text(lxml.html.tostring(doc).strip())


class RedmineScraper:
    """
    RedmineScraper class that allows you to navigate and parse issues
    for a project in Redmine.
    """

    def __init__(self, base_url=""):
        """
        :param base_url: base url to use for issue urls.  Defaults to
            the empty string.
        """
        self.base_url = base_url


    def extract_attachment(self, doc):
        """Takes an attachments p and parses out the attachment
        information.

        :param doc: doc Element holding a single attachment

        :returns: dict representing the attachment
        """
        att = {}
        ahref = doc.cssselect("a")[0]
        att["url"] = urljoin(self.base_url, ahref.attrib["href"])
        att["name"] = ahref.text

        author = doc.cssselect("span.author")[0].text
        att["author"] = author[:author.rfind(",")].strip()
        att["date"] = author[author.rfind(",")+1:].strip()

        return att


    def extract_history_item(self, doc):
        """Takes a journal div and extracts the history item
        information from it.

        :param doc: doc Element holding a single history item

        :returns: dict representing the history item
        """
        history_item = {}

        # this is fragile.  the first <a ..> is the author.  the
        # second has a title that's the date we want.
        hrefs = doc.cssselect("a")
        history_item["author"] = hrefs[2].text
        history_item["date"] = hrefs[3].attrib["title"]

        # extracts individual change_property items for this history
        # item.  the user can change multiple properties all at once.
        change_properties = []
        for change in doc.cssselect("ul li"):
            prop_name = change.cssselect("strong")[0]
            values = change.cssselect("i")
            if len(values) == 1:
                change_properties.append({
                        "property": prop_name.text,
                        "oldvalue": "",
                        "newvalue": values[0].text
                        })
            else:
                change_properties.append({
                        "property": prop_name.text,
                        "oldvalue": values[0].text,
                        "newvalue": values[1].text
                        })

        history_item["properties"] = change_properties

        comment = doc.cssselect("div.wiki")
        if len(comment) > 0:
            history_item["comment"] = textify(doc.cssselect("div.wiki")[0])
        else:
            history_item["comment"] = ""

        return history_item


    def parse_issue(self, data):
        """Takes in a string of an issue page in html, parses it, and
        returns a dict containing all the useful stuff.

        :param data: html document as a string

        :returns: dict representing the issue
        """
        issue = {}

        tree = lxml.html.parse(StringIO(data))
        root = tree.getroot()

        bug_id = root.cssselect("h2")[0].text
        issue["id"] = bug_id.split("#")[1]

        details = root.cssselect("div.details")[0]

        if details is None:
            raise ValueError("No details section in this bug?")

        title = details.cssselect("h3")[0]
        issue["title"] = title.text

        author_and_date = details.cssselect("p.author a")
        issue["author"] = author_and_date[0].text
        issue["creation-date"] = author_and_date[1].attrib["title"]
        issue["last-updated-date"] = author_and_date[2].attrib["title"]

        # the attributes table in redmine has td elements that have
        # semantic class names.  for example, one td has a class name
        # of "status".
        #
        # i abuse that fact to just grab all the data in key/value pairs.
        attributes = details.cssselect("table.attributes")[0]
        tds = attributes.cssselect("td")
        for mem in tds:
            key = mem.attrib["class"]
            if mem.text:
                issue[key] = mem.text
            else:
                issue[key] = "".join(mem.itertext())

        desc = details.cssselect("div.wiki")[0]
        # FIXME - should convert this to something useful somehow
        issue["description"] = textify(desc)

        attachments = root.cssselect("div.attachments")
        if len(attachments) > 0:
            issue["attachments"] = [
                self.extract_attachment(att)
                for att in attachments[0].cssselect("p")]
        else:
            issue["attachments"] = []

        history = root.cssselect("div#history")
        if len(history) > 0:
            issue["history"] = [
                self.extract_history_item(hist_item)
                for hist_item in history[0].cssselect("div.journal")]
        else:
            issue["history"] = []

        print issue

        return issue


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
