# -*- coding: utf-8 -*-
from collective.civicrm.browser.base import CiviCRMBaseView
from collective.civicrm.interfaces import IAddOnInstalled
from collective.civicrm.testing import INTEGRATION_TESTING
from httmock import all_requests
from httmock import HTTMock
from plone import api
from urlparse import parse_qs
from zExceptions import Forbidden
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
        json = 'getsingle_contact_{0}.json'.format(query['contact_id'][0])
    elif is_rest_call('get', 'Contact'):
        if query.get('sort_name', False):
            json = 'get_contact_sort_name.json'
        elif query.get('contact_type', False):
            json = 'get_contact_contact_type.json'
        else:
            json = 'get_contact.json'
    elif is_rest_call('get', 'ContactType'):
        json = 'get_contacttype.json'
    elif is_rest_call('get', 'Group'):
        json = 'get_group.json'
    elif is_rest_call('get', 'EntityTag'):
        json = 'get_entitytag.json'
    elif is_rest_call('get', 'GroupContact'):
        if query.get('group_id', False):
            json = 'get_groupcontact_group_4.json'
        elif query.get('contact_id', False):
            json = 'get_groupcontact_contact_9.json'
        else:
            return  # this will make python-civicrm fail
    elif is_rest_call('get', 'Relationship'):
        if 'contact_id_a' in query:
            json = 'get_relationship_a_200.json'
        elif 'contact_id_b' in query:
            json = 'get_relationship_b_200.json'
        else:
            return  # this will make python-civicrm fail
    elif is_rest_call('get', 'RelationshipType'):
        json = 'get_relationshiptype.json'
    elif is_rest_call('get', 'Tag'):
        json = 'get_tag.json'
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


class ViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IAddOnInstalled)
        configure_rest_api()


class BaseViewTestCase(ViewTestCase):

    def setUp(self):
        super(BaseViewTestCase, self).setUp()
        self.view = CiviCRMBaseView(None, self.request)

    def test_view_no_api_key(self):
        user = api.user.get_current()
        user.setMemberProperties(mapping={'api_key': ''})
        with self.assertRaises(Forbidden):
            self.view()

    def test_view_no_id(self):
        with self.assertRaises(Forbidden):
            self.view._validate_contact_id()

    def test_view_invalid_id(self):
        self.request.form['contact_id'] = 'foo'
        with self.assertRaises(Forbidden):
            self.view._validate_contact_id()


class FindContactsViewTestCase(ViewTestCase):

    def setUp(self):
        super(FindContactsViewTestCase, self).setUp()
        self.view = api.content.get_view(
            u'civicrm-find-contacts', self.portal, self.request)

    def test_find_contacts_view(self):
        with HTTMock(civicrm_server):
            self.view()

    def test_find_contacts_view_sort_name(self):
        self.request.form['sort_name'] = 'jinajameson10@example.org'
        with HTTMock(civicrm_server):
            self.view()
            self.assertEqual(len(self.view.results), 1)

    def test_find_contacts_view_contact_type(self):
        self.request.form['contact_type'] = 'Organization'
        with HTTMock(civicrm_server):
            self.view()
            self.assertEqual(len(self.view.results), 21)

    def test_find_contacts_view_group(self):
        self.request.form['group'] = '4'
        with HTTMock(civicrm_server):
            self.view()
            self.assertEqual(len(self.view.results), 8)

    def test_find_contacts_view_tag(self):
        self.request.form['tag'] = '2'
        with HTTMock(civicrm_server):
            self.view()
            self.assertEqual(len(self.view.results), 4)


class ContactViewTestCase(ViewTestCase):

    def test_contact_view(self):
        self.request.form['contact_id'] = '9'
        view = api.content.get_view(
            u'civicrm-contact', self.portal, self.request)
        with HTTMock(civicrm_server):
            view()


class RelationshipsViewTestCase(ViewTestCase):

    def test_relationships_view(self):
        self.request.form['contact_id'] = '200'
        view = api.content.get_view(
            u'civicrm-relationships', self.portal, self.request)
        with HTTMock(civicrm_server):
            view()
