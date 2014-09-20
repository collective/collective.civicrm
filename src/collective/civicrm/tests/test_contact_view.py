# -*- coding: utf-8 -*-
from collective.civicrm.interfaces import IAddOnInstalled
from collective.civicrm.testing import INTEGRATION_TESTING
from httmock import all_requests
from httmock import HTTMock
from plone import api
from urlparse import parse_qs
from zope.interface import alsoProvides

import os
import unittest


@all_requests
def civicrm_server(url, request):
    path = os.path.abspath(os.path.dirname(__file__)) + '/json/'
    query = parse_qs(url.query)
    if query['action'] == ['getsingle'] and query['entity'] == ['Contact']:
        json = 'getsingle_contact_9.json'
    elif query['action'] == ['get'] and query['entity'] == ['GroupContact']:
        json = 'get_groupcontact_9.json'
    else:
        return

    with open(path + json, 'r') as f:
        content = f.read()
    return {'status_code': 200, 'content': content}


class ContactViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def _configure_rest_api(self):
        from collective.civicrm.config import SITE_KEY_RECORD
        from collective.civicrm.config import URL_RECORD
        from plone import api
        api.portal.set_registry_record(URL_RECORD, u'localhost')
        api.portal.set_registry_record(SITE_KEY_RECORD, u'secret')
        user = api.user.get_current()
        user.setMemberProperties(mapping={'api_key': '123456'})

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IAddOnInstalled)
        self._configure_rest_api()

    @unittest.expectedFailure
    def test_view(self):
        self.request.form['contact_id'] = '9'
        view = api.content.get_view(
            u'civicrm-contact', self.portal, self.request)
        with HTTMock(civicrm_server):
            view()
