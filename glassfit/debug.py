import logging
import json
import webapp2
import util
import rfc3339
from datetime import timedelta

# for now we are using this class for catchall stuff. probably the wrong
# place for this

def timestamp_after(date, after):
    return rfc3339.format(date + timedelta(seconds=after), utc=True) \
            .replace('Z','.0Z')

def get_proxy_url(path):
    proxy = "https://mirrornotifications.appspot.com/forward?url=http://glassproxy.herokuapp.com{url}"
    proxy_url = proxy.format(url=path)
    logging.info("Proxying to {u}".format(u=proxy_url))
    return proxy_url

class LastCards(webapp2.RequestHandler):
    """for debug purposes, shows the last X cards in the timeline"""

    @util.auth_required
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        timeline_items = self.mirror_service.timeline(). \
                list().execute()['items']
        self.response.write(json.dumps(timeline_items))


class LastSubscriptions(webapp2.RequestHandler):
    @util.auth_required
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(self.mirror_service \
                .subscriptions().list().execute()))

DEBUG_PATHS = [
    ('/d/cards', LastCards),
    ('/d/subs', LastSubscriptions)
]
