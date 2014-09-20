# -*- coding: utf-8 -*-
from collective.civicrm.browser.base import CiviCRMBaseView
from collective.civicrm.config import DEBUG
from collective.civicrm.config import TTL
from collective.civicrm.logger import logger
from collective.civicrm.timer import Timer
from plone.memoize import ram
from plone.memoize import view
from time import time


class RelationshipsView(CiviCRMBaseView):

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
        super(RelationshipsView, self).__call__()
        return self.render()

    @property
    def has_relationships(self):
        """Return True if the contact has relationships."""
        return len(self.relationships) > 0

    @property
    @view.memoize
    def relationships(self):
        """Return a list of relations of a contact with its dependencies
        solved.
        """
        relationships = self.get_relationships_by_contact(self.contact_id)
        types = self.get_relationship_types
        results = []
        # TODO: refactor this uggly code
        for r in relationships['as_a']:
            type_id = int(r['relationship_type_id']) - 1
            r['relationship_type'] = types[type_id]['label_a_b']
            related = self.get_contact(r['contact_id_b'])
            r['id'] = related['contact_id']
            r['sort_name'] = related['sort_name']
            r['city'] = related['city']
            r['email'] = related['email']
            r['phone'] = related['phone']
            results.append(r)
        for r in relationships['as_b']:
            type_id = int(r['relationship_type_id']) - 1
            r['relationship_type'] = types[type_id]['label_b_a']
            related = self.get_contact(r['contact_id_a'])
            r['id'] = related['contact_id']
            r['sort_name'] = related['sort_name']
            r['city'] = related['city']
            r['email'] = related['email']
            r['phone'] = related['phone']
            results.append(r)
        return results

    def _get_relationships_by_contact(self, contact_id):
        """Return a dictionary with 2 lists of active relationships of
        a contact on a CiviCRM server. Note that a contact can have
        relationships in different directions, so it can be marked as
        contact_a or contact_b. That's why we need to make 2 separated
        calls to the CiviCRM API.

        :param contact_id: [required] the id of the contact to search for
        :type contact_ids: int
        :returns: list of dictionaries with relationship information
        """
        if DEBUG:
            count = self.civicrm.getcount('Relationship')
            logger.info(u'{0} Relationship records in server'.format(count))
        relationships = {}
        with Timer() as t:
            relationships['as_a'] = self.civicrm.get(
                'Relationship', contact_id_a=contact_id, is_active=1, limit=999)
            relationships['as_b'] = (self.civicrm.get(
                'Relationship', contact_id_b=contact_id, is_active=1, limit=999))
        logger.info(
            u'2 get Relationship API calls took {0:.2n}s'.format(t.elapsed_secs))
        return relationships

    @ram.cache(lambda method, self, contact_id: (time() // TTL, contact_id))
    def get_relationships_by_contact(self, contact_id):
        """Cached version of _get_relationships_by_contact() function."""
        return self._get_relationships_by_contact(contact_id)

    @property
    def _get_relationship_types(self):
        """Return the relationship types on a CiviCRM server.

        :returns: list of dictionaries with relationship type information
        """
        if DEBUG:
            count = self.civicrm.getcount('RelationshipType')
            logger.info(u'{0} RelationshipType records in server'.format(count))
        with Timer() as t:
            types = self.civicrm.get('RelationshipType', limit=999)
        logger.info(
            u'get RelationshipType API call took {0:.2n}s'.format(t.elapsed_secs))
        return types

    @property
    @ram.cache(lambda *args: (time() // TTL))
    def get_relationship_types(self):
        """Cached version of _get_relationship_types() function."""
        return self._get_relationship_types
