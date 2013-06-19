import logging
from collections import namedtuple

from datetime import datetime
from debug import timestamp_after

import glassfit.tasks as gtasks


# FIXME
# for now we are misusing memcache to store user's workout sessions.
# this isn't a very good idea in general because memcache values can
# be flushed at any time. This will need to be changed to use the datastore
# later on.

Exercise = namedtuple('Exercise', ['name', 'time'])

def body(workout):
    return {'text': 'Working out: doing {w}'.format(w=workout)}

workouts = [
    Exercise(name='squat', time=15),
    Exercise(name='pushup', time=20),
    Exercise(name='jumpingjacks', time=10)
]

def workout_flow(current):
    """Just for demoing purposes, we should have something more sophisticated
    later"""
    {
        None: Exercise(name='squat', time=15),
        'squat': Exercise(name='pushup', time=20),
        'pushup': Exercise(name='jumpingjacks', time=10),
        'jumpingjacks': None
    }

class NotifyHandler(object):
    def __init__(self, request_handler, event, payload, userid):
        logging.info("User %s", userid)
        logging.info("Dispatching event={event}".format(event=event))

        self.__table = {
            u'ready': self.ready_workout,
            u'finished': self.finish_workout,
            u'finished_exercise': self.finished_exercise,
            u'cancel': self.cancel_all_workouts
        }

        self.request_handler = request_handler
        self.mirror_service = request_handler.mirror_service

        self.event = event['payload']
        self.payload = payload
        self.userid = userid

        self.dispatch(self.event)

    def cancel_all_workouts(self):
        gtasks.cancel_cards(self.userid)

    def schedule_workout(self, body, after):
        body['notification'] = {
            'deliveryTime': timestamp_after(datetime.now(), after),
            'level': 'DEFAULT'
        }
        self.mirror_service.timeline().insert(body=body).execute()

    def cue_workout(self, exercise):
        logging.info("Cueing exercise: {name} for {s} seconds:" \
                .format(name=exercise.name, s=exercise.time))

    def dispatch(self, event):
        self.__table.get(event, self.unknown)()

    def unknown(self):
        logging.info("Unknown event={evt} with payload {payload}" \
                .format(evt=self.event, payload=self.payload))

    def ready_workout(self):
        current = 0
        for w in workouts:
            self.schedule_workout(body(w.name), current)
            current += w.time
        self.mirror_service.timeline().insert(body={'text': 'finished'}).execute()

    def finish_workout(self):
        logging.info('NOTIFY - User finished workout')

