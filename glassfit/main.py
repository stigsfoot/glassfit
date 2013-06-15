import logging
import json
import webapp2
import util

def get_url(self, path):
    """Like get_full_url but also wraps the url with a proxy"""
    proxy = "https://mirrornotifications.appspot.com/forward?url={url}"
    return proxy.format(url=util.get_full_url(self, '/start'))

class WorkoutState(object):
    valid_states = ['ready', 'warmup', 'workout']

    def __init__(self, state={'ready': True}):
        assert len(state.keys()) is 1
        state_name = state.keys()[0]
        if state_name not in WorkoutState.valid_states:
            raise ValueError('Invalid WorkoutState {s}'.format(s=state_name))
        self.state = state

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    @classmethod
    def from_json(cls, js):
        return cls(json.loads(js))


class StartSession(webapp2.RequestHandler):
    """Start a workout session for the user"""

    @util.auth_required
    def get(self):
        logging.info("Starting workout...Click to proceed")
        # self.session['state'] = WorkoutState()
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
        callback_url = get_url(self, '/start')
        logging.info("Using callback {url}".format(url=callback_url))
        body = { # self.userid is initialized in util.auth_required.
            'collection': self.request.get('collection', 'timeline'),
            'userToken': self.userid,
            'callbackUrl': callback_url
        }
        self.mirror_service.subscriptions().insert(body=body).execute()
        return 'Presented user with option to start workout'


START_WORKOUT_PATH = [
    ('/start', StartSession)
]