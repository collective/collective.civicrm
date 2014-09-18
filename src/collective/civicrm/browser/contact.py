# -*- coding: utf-8 -*-
from collective.civicrm.config import SITE_KEY_RECORD
from collective.civicrm.config import TIMEOUT
from collective.civicrm.config import TTL
from collective.civicrm.config import URL_RECORD
from collective.civicrm.logger import logger
from collective.civicrm.pythoncivicrm import CiviCRM
from collective.civicrm.timer import Timer
from plone import api
from plone.memoize import ram
from plone.memoize import view
from Products.Five.browser import BrowserView
from time import time
from urlparse import urlparse


class ContactView(BrowserView):

    """A page displaying information of a contact on a CiviCRM server."""

    def render(self):
        """Render the page."""
        return self.index()

    def __call__(self):
        """Initialize internal variables and open the connection to the
        CiviCRM server."""
        self.contact_id = self.request.form.get('contact_id', None)
        url = api.portal.get_registry_record(URL_RECORD)
        site_key = api.portal.get_registry_record(SITE_KEY_RECORD)
        api_key = api.user.get_current().getProperty('api_key')
        use_ssl = urlparse(url).scheme == 'https'
        self.civicrm = CiviCRM(
            url, site_key, api_key, use_ssl=use_ssl, timeout=TIMEOUT)
        return self.render()

    @view.memoize
    def _get_contact(self):
        """Return a contact from the CiviCRM server.

        :returns: dictionary with contact information
        :raises: ConnectionError
        """
        with Timer() as t:
            contact = self.civicrm.getsingle(
                'Contact', contact_id=self.contact_id)
        logger.info(
            u'getsingle Contact API call took {0:.2n}s'.format(t.elapsed_secs))
        return contact

    @property
    def get_contact(self):
        """Return True if we will show the results."""
        return self._get_contact()

    @ram.cache(lambda *args: time() // (60 * TTL))
    def _get_groups_by_contact(self):
        """Return the list of groups of a contact."""
        count = self.civicrm.getcount('GroupContact')
        logger.info(u'{0} GroupContact records in server'.format(count))
        with Timer() as t:
            groups = self.civicrm.get(
                'GroupContact', contact_id=int(self.contact_id), limit=999)
        logger.info(
            u'get GroupContact API call took {0:.2n}s'.format(t.elapsed_secs))
        return [g['title'] for g in groups]

    @property
    def get_contact_groups(self):
        """Return a comma separated list of groups the contact belongs to."""
        return ', '.join(self._get_groups_by_contact())
