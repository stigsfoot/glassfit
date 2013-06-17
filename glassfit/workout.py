import logging
import webapp2
from os import path
import util
import time
from debug import format_timestamp

# need this module to format datetime's per google's wishes

# A workout card is intended to
# 1. display a workout animated gif
# 2. display instructions
# 3. display a timer
# 4. schedule another card

# Right now we just hard code stuff
workouts_base = path.join(path.dirname(__file__), '../', 'templates/workouts/')


def workout_template(workout):
    return path.join(workouts_base, workout)


def body(workout):
    return {'text': 'Working out: doing {w}'.format(w=workout)}


class Card(webapp2.RequestHandler):
    @util.auth_required
    def get(self, workout_name, duration):
        """Render a workout card from a workout_name and a duration"""
        logging.info("Attempting to workout: {w} for {d}".format(w=workout_name, d=duration))
        template_path = workout_template(workout_name)
        logging.info("Rendering: {path}".format(path=template_path))
        self.mirror_service.timeline().insert(body=body(workout_name)).execute()

        timestamp_after_duration = int(time.mktime(time.gmtime())) + int(duration)

        logging.info("Notification will occur in {time}" \
                .format(time=timestamp_after_duration))

        rfc3339 = format_timestamp(timestamp_after_duration)

        logging.info("Using timestamp {s}".format(s=rfc3339))

        card = self.mirror_service.timeline().insert(body={
            'text': 'Finished exercise. Should have waited {s} seconds' \
                    .format(s=duration),
            'notification': {
                    'deliveryTime': rfc3339,
                    'level': 'DEFAULT'
                },
            }
        ).execute()

        logging.info("Sent a workout card %s", card)
        logging.info('Sleeping for 2.0 seconds and then cancelling')
        time.sleep(2.0)
        self.mirror_service.timeline().delete(id=card['id']).execute()
        logging.info('Deleted card')


WORKOUT_PATHS = [
        ('/workout/(.+)/(\d+)', Card)
]
