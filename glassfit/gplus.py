import logging
import util
import json
from pprint import pformat
import webapp2

def share_workout_gplus(handler, data):
    """Create a g+ moment and then update the finish card to show
    the user that we've shared it on g+"""
    logging.info("Supposed to be sharing with g+")

    moment = {
        "type":"http://schemas.google.com/AddActivity",
        "target": {
            "id": "target-id-1",
            "type":"http://schemas.google.com/AddActivity",
            "name": "The Google+ Platform",
            "description": "A page that describes just how awesome Google+ is!",
            "image": "https://developers.google.com/+/plugins/snippet/examples/thing.png"
        }
    }
        
    handler.gplus_service.moments().insert(
        userId='me',
        collection='vault',
        body=moment
    ).execute()

    item = handler.mirror_service.timeline().get(id=data['itemId']).execute()
    # might not show anything since its an html card
    item['text'] = 'finished workout'
    handler.mirror_service.timeline().update(
            id=data['itemId'], body=item).execute()

class TestGplus(webapp2.RequestHandler):
    """Test g+ service using this endpoint"""
    @util.auth_required
    def get(self):
        if hasattr(self, 'gplus_service') and \
        self.gplus_service is not None:
            self.response.write("gplus is working")
        else:
            self.response.write("gplus isn't working")
            return
        user = self.gplus_service.people().get(userId='me').execute()
        self.response.write('<pre>%s</pre>' % pformat(user))

class TestInsertMoment(webapp2.RequestHandler):
    """test inserting a moment"""
    @util.auth_required
    def get(self):
        share_workout_gplus(self, None)

class ListMoments(webapp2.RequestHandler):
    """List all moments that this app created"""
    @util.auth_required
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        moments = self.gplus_service.moments().list(userId='me',
                collection='vault').execute()
        self.response.write(json.dumps(moments))

GPLUS_PATH = [
    ('/d/gplus', TestGplus),
    ('/d/insert_moment', TestInsertMoment),
    ('/d/moments', ListMoments)
]
