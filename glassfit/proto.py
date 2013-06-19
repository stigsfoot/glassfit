import logging
import util
import webapp2
from collections import namedtuple

import glassfit.tasks as gtasks

Exercise = namedtuple('Exercise', ['name', 'time'])

workouts = [
    Exercise(name='squat', time=15),
    Exercise(name='pushup', time=20),
    Exercise(name='jumpingjacks', time=10)
]

def create_card_body(workout, delivery_time):
    body = {
        'text': 'Working out - doing {w} for {s} seconds'
            .format(w=workout.name, s=workout.time),
        'menuItems':[{
            'action': 'CUSTOM',
            'id': 'cancel',
            'values': [{
                'displayName': 'Cancel!',
                'iconUrl': 'http://i.imgur.com/dkvdDby.png'
            }],
        }],
    }
    if delivery_time is not None:
        body['notification'] = {
            # displayTime/deliveryTime is the other thing we can try
            #'displayTime': delivery_time,
            'deliveryTime': delivery_time,
            'level': 'DEFAULT'
        }
    return body

def schedule_workouts(workouts):
    skip = 0
    scheduled = []
    for workout in workouts:
        scheduled.append((create_card_body(workout, None), skip))
        skip += workout.time
    return scheduled

class StartPrototype(webapp2.RequestHandler, gtasks.TaskHandler):
    @util.auth_required
    def get(self):
        scheduled_cards = schedule_workouts(workouts)
        self.send_cards(self.userid, scheduled_cards)
        logging.info("Scheduled workouts: %s", str(scheduled_cards))


PROTOTYPE_PATH = [
    ('/proto', StartPrototype)
]
