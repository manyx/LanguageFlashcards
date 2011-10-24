
import logging
import os
import cgi
from google.appengine.ext import blobstore
from google.appengine.ext.blobstore import *
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db
from google.appengine.ext.db import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import *
from google.appengine.api.images import *
from django.utils import simplejson as json
from models import *
import datetime
import urllib

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        username = user.nickname()
        logoutUrl = users.create_logout_url("/")
        
        self.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'main.html')
        self.response.out.write(template.render(path, {'username' : json.dumps(username), 'logoutUrl' : json.dumps(logoutUrl)}))
        
application = webapp.WSGIApplication([
    ('/', MainPage),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

