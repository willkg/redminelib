========
 README
========

This is a library of stuff that I threw together to scrape a Redmine
instance to migrate my bug data to another issue tracking system.


Note about usefulness
=====================

While I tried to design this with utility in mind, it's only really
been used for my stuff and it targets the Redmine instance I needed
to migrate stuff from.  It's not clear at the time of this writing
as to whether this will be useful for other people.


Install
=======

**Installing it system wide**

Install redminelib system-wide by getting the source and then doing::

    python setup.py install


**Installing it just for you or to try out**

If you want to use it in-place without installing it system-wide, create a
virtual environment, enter it, then run::

    python setup.py develop

You need to do some kind of install because that sets up the
``redminelib-cmd`` script.


.. Note::

   If you have problems installing ``lxml``, you can install a system
   package.  On Debian-derived systems, you can do::

       apt-get install python-lxml

   If you don't have a Debian-derived system, then visit the
   `lxml website <http://lxml.de/>`_.


How to use
==========

redminelib is a library for scraping Redmine sites.  You can use it in
your programs by first importing it::

    import redminelib

creating a ``RedmineScraper`` instance::

    rs = redminelib.RedmineScraper()

and then using that.

For details on what it does and how, check the code.  If you're
interested in helping writing documentation, let me know.  I'm punting
on this for now since things are still in flux and I'm the only user.

redminelib also comes with a command-line script that you can use
called ``redminelib-cmd``.  Run::

    redminelib-cmd --help

for details.


How to run tests
================

redminelib uses `nose <http://code.google.com/p/python-nose/>`_ for
tests.

To run the tests, you must first install nose.

After you install nose, you can do::

    nosetests


Feedback, bug reports, etc
==========================

I plan to work on this project for as long as I have a need for this
code.  Beyond that, it'll hang out until someone else takes it over.

:project site: http://github.com/willkg/redminelib
:bugs:         http://github.com/willkg/redminelib/issues .
:feedback:     email: willg at bluesock dot org
