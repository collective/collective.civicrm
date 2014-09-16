# -*- coding: utf-8 -*-
"""Test if the API key field was added to member data and user registration.
"""
from collective.civicrm.testing import INTEGRATION_TESTING

import unittest


class MembershipPropertiesTestCase(unittest.TestCase):

    """Ensure membership properties overrides are properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_memberdata_has_api_key_property(self):
        memberdata = self.portal['portal_memberdata']
        self.assertTrue(memberdata.hasProperty('api_key'))

    def test_user_registration_has_api_key_field(self):
        site_properties = self.portal['portal_properties'].site_properties
        self.assertIn('api_key', site_properties.user_registration_fields)
