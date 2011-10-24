
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
import urllib2

api_list = {}
def registerAPI(name):
    def temp(func):
        if name.startswith("_"):
            api_list["/_api/" + name] = func
        else:
            api_list["/api/" + name] = func
        return func
    return temp

class Meta(webapp.RequestHandler):
    def get(self):
        self.go()
    def post(self):
        self.go()
    def go(self):
        func = api_list[self.request.path]
        func(self)

def getCurrentUser(self):
    user = users.get_current_user()
    if not user:
        raise BaseException("must be logged in")
    username = user.nickname()
    if self.request.get("me"):
        if users.is_current_user_admin():
            username = self.request.get("me")
        elif username != self.request.get("me"):
            raise BaseException("must be admin to set user")
    return getUser(username)
    
# /api/enterContest
@registerAPI("enterContest")
def api_enterContest(self):
    u = getCurrentUser(self)
    fromLanguage = self.request.get("fromlanguage")
    toLanguage = self.request.get("tolanguage")
    e = enterContest(u, fromLanguage , toLanguage)
    
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(json.dumps(e))

# /api/submitResult
@registerAPI("submitResult")
def api_submitResult(self):
    u = getCurrentUser(self)
    e = Entry.get(Key(self.request.get("entry")))
    result = self.request.get("result")
    ok = submitResult(u, e, result)
    
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(json.dumps({"ok" : ok}))

# /api/getUserInfo
@registerAPI("getUserInfo")
def api_getContests(self):
    me = getCurrentUser(self)
    user = me
    if self.request.get("user"):
        user = User.get(Key(self.request.get("user")))
    ret = getUserInfo(me, user, 10)
    
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(json.dumps(ret))

# /_api/_clear
@registerAPI("_clear")
def api_clear(self):
    clearModels()
    
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(json.dumps({"ok!" : True}))

# /_api/_eval
@registerAPI("_eval")
def api_eval(self):
    buf = []
    def output(a):
        buf.append(a)
    exec self.request.get("cmd") in globals(), locals()
    
    ret = json.dumps({"ok!" : True})
    if len(buf) > 0:
        ret = "\n".join(buf)
    
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(ret)


# /_api/_clear
@registerAPI("_clear")
def func(self):
    for i in User.all():
        i.delete()
    for i in Entry.all():
        i.delete()
    for i in Wordlist.all():
        i.delete()
    
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(json.dumps({"ok!" : True}))

# /_api/_temp
@registerAPI("_temp")
def api_eval(self):
    for u in User.all():
        u.username = u.userid
        u.put()
    
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(json.dumps({"ok!" : True}))

application = webapp.WSGIApplication([
    ('/api/.*', Meta),
    ('/_api/.*', Meta),
], debug = True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

