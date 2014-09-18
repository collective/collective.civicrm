******************************
Plone integration with CiviCRM
******************************

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

.. image:: https://raw.github.com/collective/collective.civicrm/master/civicrm-logo.png
    :alt: CiviCRM
    :target: https://civicrm.org/

`CiviCRM`_ is a web-based, open source, Constituent Relationship Management (CRM) software geared toward meeting the needs of non-profit and other civic-sector organizations.

``collective.civicrm`` is a package aimed to provide basic integration between Plone and CiviCRM.

.. _`CiviCRM`: https://civicrm.org/

Mostly Harmless
===============

.. image:: https://secure.travis-ci.org/collective/collective.civicrm.png?branch=master
    :alt: Travis CI badge
    :target: http://travis-ci.org/collective/collective.civicrm

.. image:: https://coveralls.io/repos/collective/collective.civicrm/badge.png?branch=master
    :alt: Coveralls badge
    :target: https://coveralls.io/r/collective/collective.civicrm

.. image:: https://pypip.in/d/collective.civicrm/badge.png
    :alt: Downloads
    :target: https://pypi.python.org/pypi/collective.civicrm/

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it::

    [buildout]
    ...
    eggs =
        collective.civicrm

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.civicrm`` and click the 'Activate' button.

.. Note::

    You may have to empty your browser cache and save your resource registries in order to see the effects of the product installation.

Before you begin
----------------

To use the CiviCRM integration you need the following information:

- REST interface URL
- Site key
- Every user that will interact with CiviCRM needs an API key

See `CiviCRM REST interface documentation`_ for more information on this.

.. _`CiviCRM REST interface documentation`: http://wiki.civicrm.org/confluence/display/CRMDOC/REST+interface

Usage
-----

After installing CiviCRM integration, go to the control panel configlet and set up the REST interface URL and site key.

.. figure:: https://raw.github.com/collective/collective.civicrm/master/configlet.png
    :align: center
    :height: 640px
    :width: 640px

Set up the API key for all users that will use the CiviCRM integration.

.. figure:: https://raw.github.com/collective/collective.civicrm/master/user.png
    :align: center
    :height: 640px
    :width: 640px

Go to the @@civicrm-find-contacts view at the site root and start making searches.
You can search for contacts by name or email, and you can filter the results by contact type, group and tag.

.. figure:: https://raw.github.com/collective/collective.civicrm/master/search.png
    :align: center
    :height: 700px
    :width: 640px
