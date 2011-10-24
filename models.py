
import logging
import os
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
from google.appengine.api import taskqueue
import random
from django.utils import simplejson as json
import hashlib
from myutil import *
from wordlist import *
from  pprint import pprint
import string


class User(db.Model):
    username = db.StringProperty()
    
    
class Wordlist(db.Model):
    user = db.ReferenceProperty(collection_name="a")
    language = db.TextProperty()
    theList = db.TextProperty()
    


  
class Entry(db.Model):
    user = db.ReferenceProperty(collection_name="b")
    word = db.TextProperty()
    fromLanguage = db.TextProperty()
    toLanguage = db.TextProperty()
    score = db.IntegerProperty(default=0)


def clearModels():
    for a in User.all():
        a.delete()
    for a in Entry.all():
        a.delete()
   

def getUser(username):
    u = User.gql("where username = :username", username=username).get()
    if not u:
        u = User(username = username)
        u.put()
    return u

    
def getUserInfo(me, target, count):
    def isMe(u):
        return me.key() == u.key()
        
    targetIsMe = isMe(target)
        
    def getUserJso(u):
        if isMe(u):
            return {
                "key" : str(me.key()),
                "username" : me.username
            }
        else:
            return {
                "key" : str(u.key()),
                "username" : u.username[0:4] + ".."
            }               
        
    data = {
        "me" : getUserJso(me),
        "user" : getUserJso(target),
   
    }   
    
    return data    


def enterContest(user, fromLanguage, toLanguage):
    now = mytime()
    word = "" 
    wlFound = False
    for ent in Wordlist.gql("where user = :user", user=user):  
        if ent.language == toLanguage:
            wlFound = ent
            #logging.info('WL FOUND %s  %s  %s', ent.user,ent.language,ent.theList)
            
    if not wlFound:
        newWl = Wordlist()
        newWl.theList = ','.join(getAllWords())
        newWl.user = user
        newWl.language = toLanguage
        word = string.split(newWl.theList, ',')[0]
        newWl.put()
    else:
        word = string.split(wlFound.theList, ',')[0]
        
    #word = getWords(1)[0] 

    def returnJso(e):
        jso = {
            "key" : str(e.key()),
            "word" : e.word,
            "fromLanguage" : e.fromLanguage,
            "toLanguage" : e.toLanguage
        }
        
        return jso
        
    found = False
    for ent in Entry.gql("where user = :user", user=user):  
        if ent.fromLanguage == fromLanguage and ent.toLanguage == toLanguage and ent.word == word:
            found = ent
            #logging.info('found from %s to %s word %s', ent.fromLanguage,ent.toLanguage,ent.word)
    
    
    #e = Entry.gql("where user = :user and word = :word and fromLanguage = :fromLanguage and toLanguage = :toLanguage", user=user, word=word, fromLanguage=fromLanguage, toLanguage=toLanguage ).get()
    if found:
        return returnJso(found)
    else:   
        e = Entry()
        e.user = user
        e.word = word
        e.fromLanguage = fromLanguage
        e.toLanguage = toLanguage
        e.put()
        return returnJso(e)

def submitResult(u, e, result):
    if u.key() != e.user.key():
        raise BaseException("this is not your entry")           
    
    wlFound = False
    for ent in Wordlist.gql("where user = :user", user=u):  
        if ent.language == e.toLanguage:
            wlFound = ent      
    
    if result == '1':
        if e.score < 10:
            e.score = e.score + 1
    else:
        if e.score > 0:
            e.score = int(e.score / 2)
    e.put()
    
    if wlFound:
        wordList = string.split(wlFound.theList, ',')
        lengthList = float(len(wordList))
        wordList.remove(e.word)
        wordScore = e.score
        if wordScore == 10:
            wordList.append( e.word)
        elif wordScore == 0:
            pos =  5 + random.randint(1, 20) 
            #logging.info('To pos %s | score %s | length %s', str(pos), str(wordScore) , str( lengthList / 100)) 
            if pos < 0:
                pos = 0
            wordList.insert(pos ,e.word)
        
        else:
            pos = int ( lengthList / 100 * wordScore * 10) - random.randint(1, int( lengthList / 100  * 10)) 
            #logging.info('To pos %s | score %s | length %s', str(pos), str(wordScore) , str( lengthList / 100)) 
            if pos < 0:
                pos = 0
                
            
            wordList.insert(pos ,e.word)
        wlFound.theList = ','.join(wordList)
        wlFound.put()
    
    return True
   

