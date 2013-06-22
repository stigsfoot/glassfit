import logging
import util
import webapp2

import glassfit.tasks as gtasks
import glassfit.workout as gworkout

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

PROTOTYPE_PATH = [ ('/proto', StartWorkouts), ]
