# -*- coding: utf-8 -*-
from collective.civicrm.interfaces import IAddOnInstalled
from collective.civicrm.testing import INTEGRATION_TESTING
from plone import api
from zope.interface import alsoProvides

import unittest


class FindContactsViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IAddOnInstalled)

    @unittest.expectedFailure  # we need to mock the access to the server
    def test_view_available(self):
        view = api.content.get_view(
            u'find-contacts', self.portal, self.request)
        view = view.__of__(self.portal)
        self.assertTrue(view())
