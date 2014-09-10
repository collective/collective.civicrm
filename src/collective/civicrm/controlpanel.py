# -*- coding: utf-8 -*-
from collective.civicrm import _
from collective.civicrm.interfaces import ICiviCRMSettings
from plone.app.registry.browser import controlpanel


class CiviCRMSettingsEditForm(controlpanel.RegistryEditForm):
    schema = ICiviCRMSettings
    label = _(u'CiviCRM')
    description = _(u'Configurations for the integration of Plone with CiviCRM.')


class CiviCRMSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = CiviCRMSettingsEditForm
