import logging
from pprint import pprint
import json
import webapp2
import util

# for now we are using this class for catchall stuff. probably the wrong
# place for this


def show_current_timeline_card(mirror_service, last_x=1):
    timeline = mirror_service.timeline().list(maxResults=last_x).execute()['items']
    pprint(timeline)
    logging.info("Look the current timeline item over here")


class LastCards(webapp2.RequestHandler):
    """for debug purposes, shows the last X cards in the timeline"""

    @util.auth_required
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        timeline_items = self.mirror_service.timeline().list().execute()['items']
        self.response.write(json.dumps(timeline_items))


DEBUG_PATHS = [
    ('/debug', LastCards)
]
