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

SOURCE = u'2'
TARGETS = u'3'


class ActivitiesView(CiviCRMBaseView):

    """A page displaying activities between contacts on a CiviCRM server."""

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
        super(ActivitiesView, self).__call__()
        return self.render()

    @property
    def has_activities(self):
        """Return True if the contact has activities."""
        return len(self.activities) > 0

    @property
    @view.memoize
    def activities(self):
        """Return a cached list of activities of a contact."""
        return self._get_contact_activities(self.contact_id)

    def _get_contact_activities(self, contact_id):
        """Return a list of activities of a contact. The list is sorted by
        activity_date_time in reverse order.

        :param contact_id: [required] the id of the contact to search for
        :type contact_id: int
        :returns: list of dictionaries with activities information
        """
        if DEBUG:
            count = self.civicrm.getcount('Activity')
            logger.info(u'{0} Activity records in server'.format(count))
        with Timer() as t:
            # XXX: sorting should be done here instead; how?
            activities = self.civicrm.get(
                'Activity', contact_id=contact_id, limit=999)
        logger.info(
            u'get Activity API call took {0:.2n}s'.format(t.elapsed_secs))
        activities.sort(key=lambda a: a['activity_date_time'], reverse=True)
        return activities[:25]

    @property
    def _get_contacts_by_activity(self):
        """Return a list of contacts on activities.

        :returns: dictionaries with contacts on each activity
        :rtype: dict
        """
        with Timer() as t:
            activities = self.civicrm.get('ActivityContact', limit=9999)
        logger.info(
            u'get ActivityContact API call took {0:.2n}s'.format(t.elapsed_secs))
        # simplify access by converting list of activities in a dictionary
        contacts = {}
        for a in activities:
            c = contacts.get(a['activity_id'], {SOURCE: [], TARGETS: []})
            c[a['record_type_id']].append(a['contact_id'])
            contacts[a['activity_id']] = c
        return contacts

    @property
    @ram.cache(lambda *args: (time() // TTL))
    def get_contacts_by_activity(self):
        """Cached version of _get_contacts_by_activity() function."""
        return self._get_contacts_by_activity

    @ram.cache(lambda method, self, activity: repr(activity))
    def source(self, activity):
        activities = self.get_contacts_by_activity[activity['id']]
        contact = int(activities[SOURCE][0])
        return self.get_contact(contact)['sort_name']

    @ram.cache(lambda method, self, activity: repr(activity))
    def targets(self, activity):
        activities = self.get_contacts_by_activity[activity['id']]
        contacts = [int(c) for c in activities[TARGETS]]
        pool = ThreadPool(THREADS)
        contacts = [pool.spawn(self.get_contact, c) for c in contacts]
        gevent.wait()
        contacts = [c.get()['sort_name'] for c in contacts]
        return ', '.join(contacts)
