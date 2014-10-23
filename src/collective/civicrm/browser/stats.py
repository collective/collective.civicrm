# -*- coding: utf-8 -*-
from collective.civicrm.browser.base import CiviCRMBaseView
from collective.civicrm.config import INMEDIATE_TIMING
from profilehooks import timecall


class StatsView(CiviCRMBaseView):

    """A page displaying statistics of content on a CiviCRM server."""

    def render(self):
        """Render the page."""
        return self.index()

    def __call__(self):
        """Open the connection to the CiviCRM server.

        :returns: the page to be rendered
        """
        super(StatsView, self).__call__()
        return self.render()

    @property
    @timecall(immediate=INMEDIATE_TIMING)
    def Activity(self):
        """Return the total number of Activity records."""
        return self.civicrm.getcount('Activity')

    @property
    @timecall(immediate=INMEDIATE_TIMING)
    def Contact(self):
        """Return the total number of Contact records."""
        return self.civicrm.getcount('Contact')

    @property
    @timecall(immediate=INMEDIATE_TIMING)
    def ContactType(self):
        """Return the total number of ContactType records."""
        return self.civicrm.getcount('ContactType')

    @property
    @timecall(immediate=INMEDIATE_TIMING)
    def Group(self):
        """Return the total number of Group records."""
        return self.civicrm.getcount('Group')

    @property
    @timecall(immediate=INMEDIATE_TIMING)
    def GroupContact(self):
        """Return the total number of GroupContact records."""
        return self.civicrm.getcount('GroupContact')

    @property
    @timecall(immediate=INMEDIATE_TIMING)
    def Relationship(self):
        """Return the total number of Relationship records."""
        return self.civicrm.getcount('Relationship')

    @property
    @timecall(immediate=INMEDIATE_TIMING)
    def RelationshipType(self):
        """Return the total number of RelationshipType records."""
        return self.civicrm.getcount('RelationshipType')

    @property
    @timecall(immediate=INMEDIATE_TIMING)
    def Tag(self):
        """Return the total number of Tag records."""
        return self.civicrm.getcount('Tag')
