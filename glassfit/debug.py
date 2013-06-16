import logging
from pprint import pprint
import json
import webapp2
import util
from feed.date import rfc3339

# for now we are using this class for catchall stuff. probably the wrong
# place for this

def format_timestamp(stamp):
    """format timestamp according to google"""
    import re
    tf = rfc3339.timestamp_from_tf(stamp)
    return re.sub(r'''-\d\d:\d\d''', '.561Z', tf)

def show_current_timeline_card(mirror_service, last_x=1):
    timeline = mirror_service.timeline().list(maxResults=last_x) \
            .execute()['items']
    pprint(timeline)
    logging.info("Look the current timeline item over here")


class LastCards(webapp2.RequestHandler):
    """for debug purposes, shows the last X cards in the timeline"""

    @util.auth_required
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        timeline_items = self.mirror_service.timeline(). \
                list().execute()['items']
        self.response.write(json.dumps(timeline_items))


class LastSubscriptions(webapp2.RequestHandler):
    @util.auth_required
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(self.mirror_service \
                .subscriptions().list().execute()))


DEBUG_PATHS = [
        ('/d/cards', LastCards),
        ('/d/subs', LastSubscriptions)
        ]
