import logging
import util
import webapp2
import traceback
from google.appengine.api import memcache
from collections import namedtuple
from glassfit.debug import timestamp_after
from datetime import datetime

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
                'iconUrl': 'http://imgur.com/cancel.jpg'
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

def schedule_workouts(workouts, schedule):
    skip = 0
    now = datetime.now()
    ids = []
    for workout in workouts:
        body = None
        date_scheduled = timestamp_after(now, 0)
        if skip == 0:
            body = create_card_body(workout, None)
        else:
            date_scheduled = timestamp_after(now, skip)
            body = create_card_body(workout, date_scheduled)
        logging.info("Scheduling card in %s", date_scheduled)
        card = schedule(body)
        skip += workout.time
        ids.append(card['id'])
    return ids

def serialize_ids(ids):
    return '__'.join([str(x) for x in ids])

def deserialize_ids(ids):
    return ids.split('__')

def save_workout(userid, workouts_ids):
    memcache.set(key=userid, value=serialize_ids(workouts_ids), time=3600)

def cancel_workouts(userid, cancel):
    try:
        for workout_id in deserialize_ids(memcache.get(key=userid)):
            cancel(workout_id) # error handling should be done in cancel
    except Exception:
        logging.warn('Cancel did not handle exception:')
        logging.warn(traceback.format_exc())

class StartPrototype(webapp2.RequestHandler):
    @util.auth_required
    def get(self):
        cancel_workouts(self.userid, lambda w_id:
                self.mirror_service.timeline().delete(id=w_id).execute())
        workout_ids = schedule_workouts(workouts,
                lambda body: self.mirror_service.timeline() \
                    .insert(body=body).execute())
        logging.info("Scheduled workouts: %s", str(workout_ids))
        save_workout(self.userid, workout_ids)

PROTOTYPE_PATH = [
    ('/proto', StartPrototype)
]
