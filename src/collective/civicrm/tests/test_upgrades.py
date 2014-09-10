# -*- coding: utf-8 -*-
from collective.civicrm.config import PROJECTNAME
from collective.civicrm.testing import INTEGRATION_TESTING
from Products.GenericSetup.upgrade import listUpgradeSteps

import unittest


class TestUpgrade(unittest.TestCase):

    """Ensure product upgrades work."""

    layer = INTEGRATION_TESTING

    profile = '{0}:default'.format(PROJECTNAME)

    def setUp(self):
        self.portal = self.layer['portal']
        self.st = self.portal['portal_setup']

    def test_version(self):
        self.assertEqual(
            self.st.getLastVersionForProfile(self.profile), (u'1000',))

    @unittest.expectedFailure  # no upgrade steps defined yet
    def test_to1010_available(self):
        upgradeSteps = listUpgradeSteps(self.st, self.profile, '1000')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('1010',))
                and (step[0]['source'] == ('1000',))]
        self.assertEqual(len(step), 1)
