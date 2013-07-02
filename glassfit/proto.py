import logging
import util
import webapp2

import glassfit.tasks as gtasks
import glassfit.workout as gworkout
from glassfit.main import start_page_card

def create_schedule(workouts):
    skip = 0
    scheduled = []
    for workout in workouts:
        scheduled.append((workout, skip))
        skip += workout.time
    return scheduled

class WorkoutScheduler(gtasks.TaskHandler):
    def schedule_workouts(self, userid, profile):
        logging.info("Preparing workout: %s", profile)
        scheduled_cards = create_schedule(gworkout.select_workout(profile))
        self.send_cards(userid, scheduled_cards)
        logging.info("Scheduled workouts: %s", str(scheduled_cards))

class StartWorkouts(webapp2.RequestHandler, WorkoutScheduler):
    @util.auth_required
    def get(self, profile):
        self.schedule_workouts(self.userid, profile)

class StartPrototype(webapp2.RequestHandler):
    @util.auth_required
    def get(self):
        self.response.write('Check your Glass Device. You will be able to customize and purchase new workouts in a future update here.')
        self.mirror_service.timeline().insert(body=start_page_card()).execute()

PROTOTYPE_PATH = [ 
    ('/proto/(.+)', StartWorkouts),
    ('/', StartPrototype)
]
