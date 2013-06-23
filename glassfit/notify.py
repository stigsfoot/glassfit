import logging
import glassfit.tasks as gtasks

# FIXME
# for now we are misusing memcache to store user's workout sessions.
# this isn't a very good idea in general because memcache values can
# be flushed at any time. This will need to be changed to use the datastore
# later on.

class NotifyHandler(object):
    def __init__(self, request_handler, event, payload, userid):
        logging.info("User %s", userid)
        logging.info("Dispatching event={event}".format(event=event))

        self.__table = {
            u'ready': self.ready_workout,
            u'finish': self.finish_workout,
            u'cancel': self.cancel_all_workouts
        }

        self.request_handler = request_handler
        self.mirror_service = request_handler.mirror_service
        self.userid = userid
        self.payload = payload

        if 'payload' in event:
            self.event = event['payload']
            self.dispatch(self.event)
        else:
            logging.info('Unrecognized event')

    def cancel_all_workouts(self):
        gtasks.cancel_cards(self.userid)

    def dispatch(self, event):
        self.__table.get(event, self.unknown)()

    def unknown(self):
        logging.info("Unknown event={evt} with payload {payload}" \
                .format(evt=self.event, payload=self.payload))

    def ready_workout(self):
        logging.info("Starting work out. Redirecting...")
        self.request_handler.ready_schedule_workouts()

    def finish_workout(self):
        logging.info('NOTIFY - User completed workout')

