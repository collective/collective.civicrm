# -*- coding: utf-8 -*-
from collective.civicrm.config import API_KEY
from collective.civicrm.config import SITE_KEY_RECORD
from collective.civicrm.config import TIMEOUT
from collective.civicrm.config import URL_RECORD
from collective.civicrm.pythoncivicrm import CiviCRM
from plone import api
from plone.memoize import view
from Products.Five.browser import BrowserView


class FindContactsView(BrowserView):

    """A page displaying a form to search for contacts on a CiviCRM server."""

    def render(self):
        """Render the page."""
        return self.index()

    def __call__(self):
        """Initialize internal variables and open the connection to the
        CiviCRM server."""
        self.sort_name = self.request.form.get('sort_name', None)
        self.contact_type = self.request.form.get('contact_type', None)
        self.group = self.request.form.get('group', None)
        self.tag = self.request.form.get('tag', None)
        url = api.portal.get_registry_record(URL_RECORD)
        site_key = api.portal.get_registry_record(SITE_KEY_RECORD)
        api_key = API_KEY
        self.civicrm = CiviCRM(
            url, site_key, api_key, use_ssl=False, timeout=TIMEOUT)
        return self.render()

    @property
    def show_results(self):
        """Return True if we will show the results."""
        return self.sort_name is not None

    @property
    def has_results(self):
        """Return True if we have results to show."""
        return len(self.results()) > 0

    @view.memoize
    def results(self, limit=-1):
        """Return the contacts that fullfil the query specified.
        We just define a timeout for all operations and we do not
        handle any exception.

        :param limit: Number of results to return; by default we return all
        :type limit: int
        :returns: list of dictionaries with contact information
        :raises: ConnectionError
        """
        results = self.civicrm.get(
            'Contact',
            sort_name=self.sort_name,
            contact_type=self.contact_type,
            limit=limit,
        )
        # the API does not support filtering by group, nor by tag;
        # we have to deal with that here
        if self.group:
            results = [i for i in results if self.filter_by_group(i, self.group)]
        if self.tag:
            results = [i for i in results if self.filter_by_tag(i, self.tag)]
        return results

    @view.memoize
    def get_contact_types(self):
        """Return the contact types available.

        :returns: list of dictionaries with contact type information
        :raises: ConnectionError
        """
        contact_types = [dict(value=u'', selected=u'', title=u'- any contact types -')]
        results = self.civicrm.get('ContactType', limit=999)
        for ct in results:
            selected = self.contact_type == ct['name']
            contact_types.append(dict(
                value=ct['name'],
                selected=u'selected' if selected else u'',
                title=ct['label'],
            ))
        return contact_types

    @view.memoize
    def get_groups(self):
        """Return the groups available.

        :returns: list of dictionaries with group information
        :raises: ConnectionError
        """
        groups = [dict(value=u'', selected=u'', title=u'- any group -')]
        results = self.civicrm.get('Group', limit=999)
        for group in results:
            selected = self.group == group['id']
            groups.append(dict(
                value=group['id'],
                selected=u'selected' if selected else u'',
                title=group['title'],
            ))
        return groups

    @view.memoize
    def get_tags(self):
        """Return the tags available.

        :returns: list of dictionaries with tags
        :raises: ConnectionError
        """
        tags = [dict(value=u'', selected=u'', title=u'- any tag -')]
        results = self.civicrm.get('Tag', limit=999)
        for tag in results:
            selected = self.tag == tag['name']
            tags.append(dict(
                value=tag['name'],
                selected=u'selected' if selected else u'',
                title=tag['name'],
            ))
        return tags

    @view.memoize
    def get_contacts_by_group(self, group):
        """Return the list of contacts on a group."""
        group = int(group)
        contacts = self.civicrm.get('GroupContact', group_id=group, limit=999)
        return [c['id'] for c in contacts]

    def filter_by_group(self, contact, group):
        """Return True if the contact is in the group."""
        return contact['id'] in self.get_contacts_by_group(group)

    def filter_by_tag(self, contact, tag):
        """Return True if the contact is tagged."""
        return True  # not yet implemented
