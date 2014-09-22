# -*- coding: utf-8 -*-
from collective.civicrm.browser.base import CiviCRMBaseView
from collective.civicrm.config import DEBUG
from collective.civicrm.config import THREADS
from collective.civicrm.config import TTL
from collective.civicrm.logger import logger
from collective.civicrm.timer import Timer
from gevent.threadpool import ThreadPool
from plone.memoize import ram
from plone.memoize import view
from time import time

import gevent


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
        return self._resolve_relationships(relationships)

    def _get_relationships_by_contact(self, contact_id):
        """Return a dictionary with 2 lists of active relationships of
        a contact on a CiviCRM server. Note that a contact can have
        relationships in different directions, so it can be marked as
        contact_a or contact_b. That's why we need to make 2 separated
        calls to the CiviCRM API.

        :param contact_id: [required] the id of the contact to search for
        :type contact_id: int
        :returns: list of dictionaries with relationship information
        """
        if DEBUG:
            count = self.civicrm.getcount('Relationship')
            logger.info(u'{0} Relationship records in server'.format(count))
        relationships = {}
        with Timer() as t:
            relationships = self.civicrm.get(
                'Relationship', contact_id_a=contact_id, is_active=1, limit=999)
            relationships.extend(self.civicrm.get(
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

    def _get_related_contacts(self, relationships):
        """Return a list of related contacts from a CiviCRM server.
        Run the API calls concurrently to speed up the process.

        :param relationships: [required] relationship information of the
            selected contact
        :type relationships: list of dictionaries with relationship
            information
        :returns: dictionary with contact information dictionaries
        """
        contacts = []
        for r in relationships:
            if int(r['contact_id_a']) == self.contact_id:
                contacts.append(r['contact_id_b'])
            elif int(r['contact_id_b']) == self.contact_id:
                contacts.append(r['contact_id_a'])
        pool = ThreadPool(THREADS)
        contacts = [pool.spawn(self.get_contact, c) for c in contacts]
        gevent.wait()
        contacts = [c.get() for c in contacts]
        # make mapping easier by returning contact_id as dictionary key
        return dict([(c['contact_id'], c) for c in contacts])

    def _resolve_relationships(self, relationships):
        """Resolve the contact relationships by mapping correctly the
        labels and contact ids.

        :param relationships: [required] relationship information of the
            selected contact
        :type relationships: list of dictionaries with relationship
            information
        :returns: list of related contact information dictionaries
        """
        types = self.get_relationship_types
        contacts = self._get_related_contacts(relationships)
        results = []
        for r in relationships:
            type_id = int(r['relationship_type_id']) - 1
            if int(r['contact_id_a']) == self.contact_id:
                r['relationship_type'] = types[type_id]['label_a_b']
                contact = contacts[r['contact_id_b']]
            elif int(r['contact_id_b']) == self.contact_id:
                r['relationship_type'] = types[type_id]['label_b_a']
                contact = contacts[r['contact_id_a']]
            r['id'] = contact['contact_id']
            r['sort_name'] = contact['sort_name']
            r['city'] = contact['city']
            r['email'] = contact['email']
            r['phone'] = contact['phone']
            results.append(r)
        return results
