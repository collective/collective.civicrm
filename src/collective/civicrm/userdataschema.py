# -*- coding: utf-8 -*-
from collective.civicrm import _
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope import schema
from zope.interface import implements


class UserDataSchemaProvider(object):

    implements(IUserDataSchemaProvider)

    def getSchema(self):
        return IEnhancedUserDataSchema


class IEnhancedUserDataSchema(IUserDataSchema):

    """Use all fields from default user data schema and add an extra fields."""

    api_key = schema.ASCIILine(
        title=_(u'label_api_key', default=u'CiviCRM API key'),
        description=_(
            u'help_api_key',
            default=u'Only if you are allowed to use CiviCRM REST interface.'
        ),
        required=False,
    )
