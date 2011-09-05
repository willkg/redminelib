#######################################################################
# This file is part of redminelib.
#
# Copyright (C) 2011 Will Kahn-Greene
#
# redminelib is distributed under the MIT license.  See the file
# COPYING for distribution details.
#######################################################################


import httplib
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


    def http_get(self, host, path, port=80, querystring=""):
        """Takes a host, path, port, and querystring and returns
        the HTTP response.

        :param host: host string.  ex. bugs.foocorp.net
        :param path: path of the request.  ex. /projects/mediagoblin/issues
        :param port: the port.  defaults to 80.
        :param querystring: the querystring (don't include the ?).
            defaults to the empty string

        :returns: http response object

        :raises ValueError: on a non-200 response
        """
        conn = httplib.HTTPConnection(host, port)
        if querystring:
            conn.request("GET", "?".join(path, querystring))
        else:
            conn.request("GET", path)
        resp = conn.getresponse()

        if resp.status != 200:
            # FIXME - this is bad--should do something more
            # intelligent
            raise ValueError("Bad url?: Error: status: %s reason: %s",
                             resp.status, resp.reason)

        return resp


    def extract_bugid(self, root):
        bug_id = root.cssselect("h2")[0].text

        # this peels off the "Bug #" part.
        return bug_id.split("#")[1]


    def extract_title(self, root):
        details = root.cssselect("div.details")[0]
        title = details.cssselect("h3")[0]
        return title.text


    def extract_author(self, root):
        details = root.cssselect("div.details")[0]
        author_and_date = details.cssselect("p.author a")
        return author_and_date[0].text


    def extract_creation_date(self, root):
        details = root.cssselect("div.details")[0]
        author_and_date = details.cssselect("p.author a")
        return author_and_date[1].attrib["title"]


    def extract_last_updated_date(self, root):
        details = root.cssselect("div.details")[0]
        author_and_date = details.cssselect("p.author a")
        return author_and_date[2].attrib["title"]


    def extract_description(self, root):
        details = root.cssselect("div.details")[0]
        desc = details.cssselect("div.wiki")[0]
        # FIXME - should convert this to something useful somehow
        return textify(desc)


    def extract_attributes(self, root):
        details = root.cssselect("div.details")[0]
        attributes = {}

        # the attributes table in redmine has td elements that have
        # semantic class names.  for example, one td has a class name
        # of "status".
        #
        # i abuse that fact to just grab all the data in key/value pairs.
        attributes_table = details.cssselect("table.attributes")[0]
        for elem in attributes_table.cssselect("td"):
            key = elem.attrib["class"]
            if elem.text:
                attributes[key] = elem.text
            else:
                attributes[key] = "".join(elem.itertext())

        return attributes


    def extract_relation(self, elem_tr):
        relation = {}

        td = elem_tr.cssselect("td")[0]
        issue_id = td.cssselect("a")[0]
        relation["id"] = issue_id.text.split("#")[1]
        relation["relation"] = td.text.split(" ")[0]

        return relation


    def extract_relations(self, root):
        relations = root.cssselect("div#relations")
        if len(relations) > 0:
            return  [
                self.extract_relation(rel)
                for rel in relations[0].cssselect("tr")]
        else:
            return []


    def extract_watcher(self, elem_span):
        return elem_span.cssselect("a")[0].text


    def extract_watchers(self, root):
        """
        .. Note::

           Watchers only show up on the page if you're logged in.

        :param root: the document

        :returns: list of watchers (each a string)
        """
        watchers = root.cssselect("div#watchers")
        if len(watchers) > 0:
            return [
                self.extract_watcher(wat)
                for wat in watchers[0].cssselect("span.user")]
        else:
            return []


    def extract_attachments(self, root):
        attachments = root.cssselect("div.attachments")
        if len(attachments) > 0:
            return  [
                self.extract_attachment(att)
                for att in attachments[0].cssselect("p")]
        else:
            return []


    def extract_attachment(self, elem_p):
        """Takes an attachments p and parses out the attachment
        information.

        :param doc: doc Element holding a single attachment

        :returns: dict representing the attachment
        """
        att = {}
        ahref = elem_p.cssselect("a")[0]
        att["url"] = urljoin(self.base_url, ahref.attrib["href"])
        att["name"] = ahref.text

        author = elem_p.cssselect("span.author")[0].text
        att["author"] = author[:author.rfind(",")].strip()
        att["date"] = author[author.rfind(",")+1:].strip()

        return att


    def extract_history(self, root):
        history = root.cssselect("div#history")
        if len(history) > 0:
            return [
                self.extract_history_item(hist_item)
                for hist_item in history[0].cssselect("div.journal")]
        else:
            return []


    def extract_history_item(self, elem_div):
        """Takes a journal div and extracts the history item
        information from it.

        :param doc: doc Element holding a single history item

        :returns: dict representing the history item
        """
        history_item = {}

        # this is fragile.  the first <a ..> is the author.  the
        # second has a title that's the date we want.
        hrefs = elem_div.cssselect("a")
        history_item["author"] = hrefs[2].text
        history_item["date"] = hrefs[3].attrib["title"]

        # extracts individual change_property items for this history
        # item.  the user can change multiple properties all at once.
        change_properties = []
        for change in elem_div.cssselect("ul li"):
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

        comment = elem_div.cssselect("div.wiki")
        if len(comment) > 0:
            # if you're logged in, you get this additional contextual
            # bit that has ajaxy stuff for commenting, editing, etc.
            # so we remove it if it's there so we're only getting the
            # comment.
            contextual = comment[0].cssselect("div.contextual")
            if len(contextual) > 0:
                contextual[0].clear()
            history_item["comment"] = textify(comment[0])
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

        issue["id"] = self.extract_bugid(root)
        issue["title"] = self.extract_title(root)
        issue["author"] = self.extract_author(root)
        issue["creation-date"] = self.extract_creation_date(root)
        issue["last-updated-date"] = self.extract_last_updated_date(root)
        issue.update(self.extract_attributes(root))
        issue["description"] = self.extract_description(root)
        issue["relations"] = self.extract_relations(root)
        issue["watchers"] = self.extract_watchers(root)
        issue["attachments"] = self.extract_attachments(root)
        issue["history"] = self.extract_history(root)

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
