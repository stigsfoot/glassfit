import logging

class NotifyHandler(object):
    def __init__(self, request_handler, event, payload):
        logging.info("Dispatching event={event}".format(event=event))
        self.__table = {
            u'ready': self.ready_workout,
            u'finished': self.finish_workout,
            u'finished_exercise': self.finished_exercise,
        }

        self.event = event
        self.payload = payload

        self.request_handler = request_handler
        self.mirror_service = request_handler.mirror_service
        self.dispatch(event)

    def dispatch(self, event):
        self.__table.get(event, self.unknown)()

    def unknown(self):
        logging.info("Unknown event={evt} with payload {payload}" \
                .format( evt=self.event, payload=self.payload))

    def ready_workout(self):
        logging.info('NOTIFY - User ready to workout')

    def finish_workout(self):
        logging.info('NOTIFY - User finished workout')

    def finished_exercise(self):
        logging.info('NOTIFY - User finished an exercise')
