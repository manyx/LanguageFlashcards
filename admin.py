
import logging
import os
from urlparse import urlparse
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
from myutil import *
from myjson import *
from google.appengine.api import images
from google.appengine.api import taskqueue

sapi_list = {}
def registerSecureAPI(name):
    def temp(func):
        sapi_list["/admin/" + name] = func
        return func
    return temp

class SecureMeta(webapp.RequestHandler):
    def get(self):
        self.go()
    def post(self):
        self.go()
    def go(self):
        func = sapi_list[self.request.path]
        func(self)

@registerSecureAPI("test")
def api_test(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write("ok")

class Admin(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'admin.html')
        u = urlparse.urlparse(self.request.url)
        dashboard = ""
        if u.netloc.startswith("localhost"):
            dashboard = "/_ah/admin"
        else:
            appname = u.netloc[:u.netloc.find(".")]
            dashboard = "https://appengine.google.com/dashboard?&app_id=s~" + appname
        self.response.out.write(template.render(path, {"dashboard" : dashboard}))

application = webapp.WSGIApplication([
    ('/admin.html', Admin),
    ('/admin', Admin),
    ('/admin/.*', SecureMeta),
], debug = True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
