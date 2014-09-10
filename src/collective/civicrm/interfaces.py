# -*- coding: utf-8 -*-
from collective.civicrm import _
from plone.directives import form
from zope import schema
from zope.interface import Interface


class IAddOnInstalled(Interface):

    """A layer specific for this add-on product."""


class ICiviCRMSettings(form.Schema):

    """Control panel form."""

    url = schema.TextLine(
        title=_(u'URL'),
        description=_(u'URL used for API calls using the REST interface.'),
        required=True,
    )

    civicrm_site_key = schema.TextLine(
        title=_(u'Site key'),
        description=_(u'The value of CIVICRM_SITE_KEY from your settings file (civicrm.settings.php).'),
        required=True,
    )
