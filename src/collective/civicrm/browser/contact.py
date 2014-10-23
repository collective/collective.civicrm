# -*- coding: utf-8 -*-
from collective.civicrm.browser.base import CiviCRMBaseView
from collective.civicrm.config import INMEDIATE_TIMING
from collective.civicrm.config import TTL
from plone.memoize import ram
from plone.memoize import view
from profilehooks import timecall
from time import time


class ContactView(CiviCRMBaseView):

    """A page displaying information of a contact on a CiviCRM server."""

    def render(self):
        """Render the page."""
        return self.index()

    def __call__(self):
        """Open the connection to the CiviCRM server and initialize
        internal variables.

        :returns: the page to be rendered
        """
        if not self._validate_contact_id:
            return

        self.contact_id = int(self.request.form.get('contact_id'))
        # open connection to CiviCRM server
        super(ContactView, self).__call__()
        return self.render()

    @property
    @view.memoize
    def contact(self):
        """Return the information of the current contact."""
        return self.get_contact(self.contact_id)

    @timecall(immediate=INMEDIATE_TIMING)
    def _get_groups_by_contact(self, contact_id):
        """Return the list of groups of a contact.

        :param contact_id: [required] the id of the contact to search for
        :type contact_ids: int
        :returns: list of group names
        """
        query = dict(contact_id=contact_id, limit=999)
        groups = self.civicrm.get('GroupContact', **query)
        return [g['title'] for g in groups]

    @property
    @ram.cache(lambda method, self: (time() // TTL, self.contact_id))
    def groups(self):
        """Return a comma separated list of groups the contact belongs to."""
        return ', '.join(self._get_groups_by_contact(self.contact_id))
