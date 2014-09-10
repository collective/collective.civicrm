# -*- coding: utf-8 -*-
from collective.civicrm.config import PROJECTNAME
from collective.civicrm.interfaces import ICiviCRMSettings
from collective.civicrm.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_has_view(self):
        request = self.layer['request']
        view = api.content.get_view(u'civicrm-settings', self.portal, request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@civicrm-settings')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('civicrm', actions)

    def test_controlpanel_permissions(self):
        roles = ['Manager', 'Site Administrator']
        for r in roles:
            with api.env.adopt_roles([r]):
                configlets = self.controlpanel.enumConfiglets(group='Products')
                configlets = [a['id'] for a in configlets]
                self.assertIn(
                    'civicrm', configlets, 'configlet not listed for ' + r)

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertNotIn('civicrm', actions)


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ICiviCRMSettings)

    def test_url_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'url'))

    def test_civicrm_site_key_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'civicrm_site_key'))

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        BASE_REGISTRY = 'collective.civicrm.controlpanel.ICiviCRMSettings.'
        records = [
            BASE_REGISTRY + 'url',
            BASE_REGISTRY + 'civicrm_site_key',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
