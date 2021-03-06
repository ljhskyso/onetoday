#!/usr/bin/env python
import tweepy
#from our keys module (keys.py), import the keys dictionary
from keys import keys
 
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


print "Successfully logged in as " + api.me().name + "."
try:
 if len(sys.argv[1]) <= 140:
  api.update_status(sys.argv[1])
  print "Successfully tweeted: " + "'" + sys.argv[1] + "'!"
 else:
  raise IOError
except:
 print "Something went wrong: either your tweet was too long or you didn't pass in a string argument at launch."
finally:
 print "Shutting down script..."

twt = api.search(q="onetoday")     
 
#list of specific strings we want to check for in Tweets
t = ['#oneToday',
    '#one_today',
    '#ONETODAY',
    '#OneToday',
    '#onetoday',
    'onetoday']
 
for s in twt:
    for i in t:
        if i == s.text:
            sn = s.user.screen_name
            m = "Hello @%s Some kids in Indonesia would love to have running water. Fund a water well for $1. http://goo.gl/N9cux9 " % (sn)
            s = api.update_status(m, s.id)
