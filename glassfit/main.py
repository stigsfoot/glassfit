import logging
import webapp2
import util
import json

from glassfit.workout import jinja
import glassfit.notify

def start_page_card():
    template = jinja.get_template('welcome.json')
    return json.loads(template.render({}))

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
        }, None)

START_WORKOUT_PATH = [
    ('/start', StartSession)
]
