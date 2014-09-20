# -*- coding: utf-8 -*-
from collective.civicrm.config import SITE_KEY_RECORD
from collective.civicrm.config import TIMEOUT
from collective.civicrm.config import URL_RECORD
from collective.civicrm.pythoncivicrm import CiviCRM
from plone import api
from Products.Five.browser import BrowserView
from urlparse import urlparse
from zExceptions import Forbidden


class CiviCRMBaseView(BrowserView):

    """A base browser view for getting information from a CiviCRM
    server using its REST API interface.
    """

    def __call__(self):
        """Open a connection to the CiviCRM server using the
        configuration information stored on the registry and the
        current user account.

        :raises: Forbidden
        """
        url = api.portal.get_registry_record(URL_RECORD)
        site_key = api.portal.get_registry_record(SITE_KEY_RECORD)
        api_key = api.user.get_current().getProperty('api_key', None)

        # can not open connection to server if no api_key is provided
        if not api_key:
            raise Forbidden(
                'No API key defined. You can not access CiviCRM server.')

        # for now, we can use any kind of connection
        # in the future, we must enforce use_ssl=True
        # as CiviCRM stores personal information of users
        use_ssl = urlparse(url).scheme == 'https'
        self.civicrm = CiviCRM(
            url, site_key, api_key, use_ssl=use_ssl, timeout=TIMEOUT)
