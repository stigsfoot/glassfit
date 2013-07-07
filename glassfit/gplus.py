import logging
import util
from pprint import pformat
import webapp2

def share_workout_gplus(mirror_service, finished_card):
    """Share a completed workout with g+ but not its stats"""
    logging.info("Supposed to be sharing with g+")

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

GPLUS_PATH = [ ('/d/gplus', TestGplus) ]
