import logging
import webapp2
import util

import glassfit.notify

def start_page_card():
    """Initial card"""
    # TODO probably should some sort of a menu for the user here?
    # or maybe just immediately start a workout?
    timeline_item_body = {
        'text': 'Welcome to Glassfit. -- Menu here --',
        'notification': {
            'level': 'DEFAULT'
        }
    }
    return timeline_item_body

class StartSession(webapp2.RequestHandler):
    """Start a workout session for the user"""

    @util.auth_required
    def get(self):
        logging.info("Starting workout...Click to proceed")
        card = {
            'text': 'Are you ready to start working out?',
            'menuItems': [{
                              'action': 'CUSTOM',
                              'id': 'ready',
                              'values': [{
                                             'displayName': 'Ready!',
                                             'iconUrl': 'http://imgur/lets.go'
                                         }]
                          }],
        }

        self.mirror_service.timeline().insert(body=card).execute()
        self.response.write('User start workout')

        glassfit.notify.NotifyHandler(self, {
            'payload': 'ready'
        },None)

START_WORKOUT_PATH = [
    ('/start', StartSession)
]
