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
    """Simulate certain responses from a CiviCRM server."""

    # helper function
    is_rest_call = lambda action, entity: (
        query['action'] == [action] and query['entity'] == [entity])

    path = os.path.abspath(os.path.dirname(__file__)) + '/json/'
    query = parse_qs(url.query)
    if is_rest_call('getsingle', 'Contact'):
        json = 'getsingle_contact_9.json'
    elif is_rest_call('get', 'ContactType'):
        json = 'get_contacttype.json'
    elif is_rest_call('get', 'GroupContact'):
        json = 'get_groupcontact_9.json'
    elif is_rest_call('get', 'Relationship'):
        if 'contact_id_a' in query:
            json = 'get_relationship_a_200.json'
        elif 'contact_id_b' in query:
            json = 'get_relationship_b_200.json'
        else:
            return
    elif is_rest_call('get', 'RelationshipType'):
        json = 'get_relationshiptype.json'
    else:
        return  # this will make python-civicrm fail

    # return the proper content
    with open(path + json, 'r') as f:
        content = f.read()
    return {'status_code': 200, 'content': content}


def configure_rest_api():
    """Set the parameters to access the CiviCRM REST API."""
    from collective.civicrm.config import SITE_KEY_RECORD
    from collective.civicrm.config import URL_RECORD
    api.portal.set_registry_record(URL_RECORD, u'localhost')
    api.portal.set_registry_record(SITE_KEY_RECORD, u'secret')
    user = api.user.get_current()
    user.setMemberProperties(mapping={'api_key': '123456'})


class BaseViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IAddOnInstalled)
        configure_rest_api()


class FindContactsViewTestCase(BaseViewTestCase):

    @unittest.expectedFailure
    def test_find_contacts_view(self):
        view = api.content.get_view(
            u'civicrm-find-contacts', self.portal, self.request)
        with HTTMock(civicrm_server):
            view()


class ContactViewTestCase(BaseViewTestCase):

    def test_contact_view(self):
        self.request.form['contact_id'] = '9'
        view = api.content.get_view(
            u'civicrm-contact', self.portal, self.request)
        with HTTMock(civicrm_server):
            view()


class RelationshipsViewTestCase(BaseViewTestCase):

    @unittest.expectedFailure
    def test_relationships_view(self):
        self.request.form['contact_id'] = '200'
        view = api.content.get_view(
            u'civicrm-relationships', self.portal, self.request)
        with HTTMock(civicrm_server):
            view()
