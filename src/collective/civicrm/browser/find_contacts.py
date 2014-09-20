# -*- coding: utf-8 -*-
from collective.civicrm.browser.base import CiviCRMBaseView
from collective.civicrm.config import DEBUG
from collective.civicrm.config import TTL
from collective.civicrm.logger import logger
from collective.civicrm.timer import Timer
from plone.memoize import ram
from plone.memoize import view
from time import time


class FindContactsView(CiviCRMBaseView):

    """A page displaying a form to search for contacts on a CiviCRM server."""

    def render(self):
        """Render the page."""
        return self.index()

    def __call__(self):
        """Open the connection to the CiviCRM server and initialize
        internal variables.

        :returns: the page to be rendered
        """
        # open connection to CiviCRM server
        super(FindContactsView, self).__call__()
        # get variables used to display results
        self.sort_name = self.request.form.get('sort_name', None)
        self.contact_type = self.request.form.get('contact_type', None)
        self.group = self.request.form.get('group', None)
        self.tag = self.request.form.get('tag', None)
        return self.render()

    @property
    def show_results(self):
        """Return True if we will show the results."""
        return self.sort_name is not None

    @property
    def has_results(self):
        """Return True if we have results to show."""
        return len(self.results) > 0

    @property
    @view.memoize
    def results(self):
        """Return the contacts that fullfil the query specified.

        :returns: list of dictionaries with contact information
        """
        results = self.search_contacts
        # the API does not support filtering by group, nor by tag;
        # we have to deal with that here
        if self.group:
            results = [i for i in results if self.filter_by_group(i, self.group)]
        if self.tag:
            results = [i for i in results if self.filter_by_tag(i, self.tag)]
        return results

    @property
    def _search_contacts(self):
        """Search for contacts that fullfil the query specified on the
        CiviCRM server. The search is limited to 9999 records and return
        fields are limited to sort_name, city, email and phone.

        :returns: list of dictionaries with contact information
        """
        query = {
            'sort_name': self.sort_name,
            'contact_type': self.contact_type,
            'return': 'sort_name,city,email,phone',
            'limit': 9999,
        }
        if DEBUG:
            count = self.civicrm.getcount('Contact')
            logger.info(u'{0} Contact records in server'.format(count))
        with Timer() as t:
            contacts = self.civicrm.get('Contact', **query)
        logger.info(
            u'get Contact API call took {0:.2n}s'.format(t.elapsed_secs))
        return contacts

    @property
    @ram.cache(
        lambda method, self: (time() // TTL, self.sort_name, self.contact_type))
    def search_contacts(self):
        """Cached version of the _search_contacts() function."""
        return self._search_contacts

    @property
    def _get_contact_types(self):
        """Return contact types available on a CiviCRM server.

        :returns: list of dictionaries with contact type information
        """
        if DEBUG:
            count = self.civicrm.getcount('ContactType')
            logger.info(u'{0} ContactType records in server'.format(count))
        with Timer() as t:
            results = self.civicrm.get('ContactType', limit=999)
        logger.info(
            u'get ContactType API call took {0:.2n}s'.format(t.elapsed_secs))
        return results

    @property
    @ram.cache(lambda *args: time() // TTL)
    def get_contact_types(self):
        """Cached version of _get_contact_types() function."""
        return self._get_contact_types

    @property
    def contact_type_options(self):
        """Return contact type options to be used on the view template."""
        contact_types_options = [
            dict(value=u'', selected=u'', title=u'- any contact types -')]
        for ct in self.get_contact_types:
            selected = self.contact_type == ct['name']
            contact_types_options.append(dict(
                value=ct['name'],
                selected=u'selected' if selected else u'',
                title=ct['label'],
            ))
        return contact_types_options

    @property
    def _get_groups(self):
        """Return groups available on a CiviCRM server.

        :returns: list of dictionaries with group information
        """
        if DEBUG:
            count = self.civicrm.getcount('Group')
            logger.info(u'{0} Group records in server'.format(count))
        with Timer() as t:
            results = self.civicrm.get('Group', limit=999)
        logger.info(
            u'get Group API call took {0:.2n}s'.format(t.elapsed_secs))
        return results

    @property
    @ram.cache(lambda *args: time() // TTL)
    def get_groups(self):
        """Cached version of _get_groups() function."""
        return self._get_groups

    @property
    def group_options(self):
        """Return group options to be used on the view template."""
        groups = [dict(value=u'', selected=u'', title=u'- any group -')]
        for group in self.get_groups:
            selected = self.group == group['id']
            groups.append(dict(
                value=group['id'],
                selected=u'selected' if selected else u'',
                title=group['title'],
            ))
        return groups

    @property
    def _get_tags(self):
        """Return tags available on the CiviCRM server.

        :returns: list of dictionaries with tags
        """
        if DEBUG:
            count = self.civicrm.getcount('Tag')
            logger.info(u'{0} Tag records in server'.format(count))
        with Timer() as t:
            results = self.civicrm.get('Tag', limit=999)
        logger.info(u'get Tag API call took {0:.2n}s'.format(t.elapsed_secs))
        return results

    @property
    @ram.cache(lambda *args: time() // TTL)
    def get_tags(self):
        """Cached version of _get_tags() function."""
        return self._get_tags

    @property
    def tag_options(self):
        """Return tag options to be used on the view template."""
        tags = [dict(value=u'', selected=u'', title=u'- any tag -')]
        for tag in self.get_tags:
            selected = self.tag == tag['id']
            tags.append(dict(
                value=tag['id'],
                selected=u'selected' if selected else u'',
                title=tag['name'],
            ))
        return tags

    @ram.cache(lambda method, self, group: (time() // TTL, group))
    def get_contacts_by_group(self, group):
        """Return the list of contacts on a group."""
        if DEBUG:
            count = self.civicrm.getcount('GroupContact')
            logger.info(u'{0} GroupContact records in server'.format(count))
        with Timer() as t:
            contacts = self.civicrm.get(
                'GroupContact', group_id=int(group), limit=999)
        logger.info(
            u'get GroupContact API call took {0:.2n}s'.format(t.elapsed_secs))
        return [c['contact_id'] for c in contacts]

    @ram.cache(lambda method, self, tag: (time() // TTL, tag))
    def get_contacts_with_tag(self, tag):
        """Return the list of contacts with the tag."""
        with Timer() as t:
            contacts = self.civicrm.get(
                'EntityTag', tag_id=int(tag), limit=999)
        logger.info(
            u'get EntityTag API call took {0:.2n}s'.format(t.elapsed_secs))
        return [c['entity_id'] for c in contacts]

    def filter_by_group(self, contact, group):
        """Return True if the contact is in the group."""
        return contact['id'] in self.get_contacts_by_group(group)

    def filter_by_tag(self, contact, tag):
        """Return True if the contact has the tag."""
        return contact['id'] in self.get_contacts_with_tag(tag)
