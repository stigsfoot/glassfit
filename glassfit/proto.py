import logging
import util
import webapp2

import glassfit.tasks as gtasks
import glassfit.workout as gworkout
from glassfit.main import start_page_card

def schedule_workouts(workouts):
    skip = 0
    scheduled = []
    for workout in workouts:
        scheduled.append((workout, skip))
        skip += workout.time
    return scheduled

class StartWorkouts(webapp2.RequestHandler, gtasks.TaskHandler):
    @util.auth_required
    def get(self):
        scheduled_cards = schedule_workouts(gworkout.workout)
        self.send_cards(self.userid, scheduled_cards)
        logging.info("Scheduled workouts: %s", str(scheduled_cards))

class StartPrototype(webapp2.RequestHandler):
    @util.auth_required
    def get(self):
        self.response.write('start page')
        self.mirror_service.timeline().insert(body=start_page_card()).execute()

PROTOTYPE_PATH = [ 
    ('/proto', StartWorkouts),
    ('/', StartPrototype)
]
