# -*- coding: utf-8 -*-
from collective.civicrm.config import PROJECTNAME
from collective.civicrm.interfaces import IAddOnInstalled
from collective.civicrm.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers

import unittest


class BaseTestCase(unittest.TestCase):

    """Base test case to be used by other tests."""

    layer = INTEGRATION_TESTING

    profile = 'collective.civicrm:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.wt = self.portal['portal_workflow']


class TestInstall(BaseTestCase):

    """Ensure product is properly installed."""

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME),
                        '%s not installed' % PROJECTNAME)

    def test_browser_layer_installed(self):
        self.assertIn(IAddOnInstalled, registered_layers())


class TestUninstall(BaseTestCase):

    """Ensure product is properly uninstalled."""

    def setUp(self):
        BaseTestCase.setUp(self)
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_removed_uninstalled(self):
        self.assertNotIn(IAddOnInstalled, registered_layers())
