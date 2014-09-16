# -*- coding: utf-8 -*-
from collective.civicrm import _
from collective.civicrm.interfaces import ICiviCRMSettings
from plone.app.registry.browser import controlpanel


class CiviCRMSettingsEditForm(controlpanel.RegistryEditForm):
    schema = ICiviCRMSettings
    label = _(u'CiviCRM settings')
    description = _(u'CiviCRM REST interface parameters for integration with Plone.')


class CiviCRMSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = CiviCRMSettingsEditForm
