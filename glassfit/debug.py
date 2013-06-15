import logging
from pprint import pprint
import json
import webapp2
import util

# class WithSession(webapp2.RequestHandler):
#     """A handler that extends WithSession can access the current session with self.session"""
#
#     def dispatch(self):
#         self.session_store = sessions.get_store(request=self.request)
#         try:
#             webapp2.RequestHandler.dispatch(self)
#         finally:
#             self.session_store.save_sessions(self.response)
#
#     @webapp2.cached_property
#     def session(self):
#         return self.session_store.get_session()


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
