"""cancelable card scheduler using task queues. purely a prototype
for now since we do everything through memcache for now. This is good
enough for a prototype but does work so well in real life b/c some users
might experience their workouts to be randomly wiped by google's random
memcache flushes"""

import logging
import webapp2
from google.appengine.api import taskqueue
from oauth2client.appengine import StorageByKeyName
from google.appengine.api import memcache
from model import Credentials
from glassfit.workout import WorkoutTemplate, WorkoutSet
import util

class TaskHandler(object):
    """A mixin that provides a request handler the ability to schedule
    cards using a task queue."""

    def send_cards(self, userid, cards):
        memcache.delete(key=userid)
        taskids = [ self.send_card_task(userid, card, time) \
                for card, time in cards ]
        memcache.set(key=userid, value='__'.join(taskids))
        logging.info('Tasks: %s for user:%s', str(taskids), userid)

    def send_card_task(self, userid, card, countdown):
        task = taskqueue.add(
            url='/cardq',
            params={
                'payload': card.to_json(),
                'userid': userid,
            },
            countdown=countdown)
        logging.info("Sent a card to user %s. %d seconds", userid, countdown)
        return task.name

def cancel_cards(userid):
    current_val = memcache.get(key=userid)
    if current_val is None:
        logging.warn('Nothing scheduled for user %s', current_val)
        return
    memcache_values = { card:1 for card in current_val.split('__') }
    memcache.set_multi(memcache_values, time=60*60)

class CardWorker(webapp2.RequestHandler):
    """A cardworker consumes scheduled cards from the push queue and
    inserts them into the timeline unless the task was cancelled"""

    def init_service(self, userid):
        creds = StorageByKeyName(Credentials, userid, 'credentials').get()
        self.mirror_service = util.create_service('mirror', 'v1', creds)

    def post(self):
        userid = self.request.get('userid')
        taskid = self.request.headers['X-AppEngine-TaskName']
        if memcache.get(key=taskid) is not None:
            logging.info("task(%s) for user(%s) cancelled", taskid, userid)
            memcache.delete(key=taskid)
        else:
            self.init_service(userid)
            workout = WorkoutSet.of_json(self.request.get('payload'))
            card_body = WorkoutTemplate(workout).render_template()
            self.mirror_service.timeline().insert(body=card_body).execute()
            logging.info('card(%s) inserted', taskid)

TASK_ROUTES = [ ('/cardq', CardWorker) ]
