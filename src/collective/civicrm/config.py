# -*- coding: utf-8 -*-
PROJECTNAME = 'collective.civicrm'

DEBUG = False
TIMEOUT = 5  # connection to CiviCRM server timeout in seconds
TTL = 60 * 5  # number of seconds to cache some expensive API calls

REGISTRY_PREFIX = 'collective.civicrm.interfaces.ICiviCRMSettings.'
URL_RECORD = REGISTRY_PREFIX + 'url'
SITE_KEY_RECORD = REGISTRY_PREFIX + 'civicrm_site_key'
