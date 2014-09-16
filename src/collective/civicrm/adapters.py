# -*- coding: utf-8 -*-
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):

    def get_api_key(self):
        return self.context.getProperty('api_key', '')

    def set_api_key(self, value):
        return self.context.setMemberProperties({'api_key': value})

    api_key = property(get_api_key, set_api_key)
