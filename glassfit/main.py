import logging
import json
import webapp2
import util

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
        self.response.write('User start workout')

START_WORKOUT_PATH = [
    ('/start', StartSession)
]
