import ConfigParser
import os, sys, time, json
import tweepy

from projects_search import project_search
from post import post_tweet

from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Stream
from keys import keys

consumer_key = keys['consumer_key']
consumer_secret = keys['consumer_secret']
access_token = keys['access_token']
access_token_secret = keys['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# -----------------------------------------------begin: 10/31 by Jiheng
import peewee
from peewee import *

# database selection
db = MySQLDatabase('hw2', user='dbhw',passwd='')
# db = MySQLDatabase('twitter_bot', user='ct.onetoday',passwd='onetoday@CT')
# -----------------------------------------------end:   10/31 by Jiheng



class StdOutListener(StreamListener):
    ''' Handles data received from the stream. '''
 
    def on_status(self, status):

        print( 'Tweet user:  ' + status.user.screen_name )
        print( 'Tweet text:  ' + status.text )
        # Picture-urls in tweets
        if 'media' in status.entities:
            for media in status.entities['media']:
                # print( media['media_url_https'] )
                print( 'Tweet image: ' + media['media_url'] )
        else:
            print( 'no media content' )
        
####### post activities1 - find the keyword in the tweet
        receive_tweet( status )
        keyword = ''
        keyword_array = status.entities['hashtags']
        for hashtag in status.entities['hashtags']:
            if hashtag['text'] != 'onetoday':
                keyword = keyword + ' ' + hashtag['text']
        
####### post activities2 - call onetoday for project info
        print('searching project for: ' + keyword)
        [ url, prj_name ] = project_search( keyword )
        # if prj_name = 'null':
        #     if len(keyword_array) == 1:
        #         print 'null_prj_name'
        #         # call standard project
        #     else:
        #         i = 0
        #         while (prj_name == 'null'):
        #             if keyword_array[i] != 'onetoday':
        #                 keyword = keyword_array[i]
        #                 [ url, prj_name ] = project_search( keyword )
        #                 i++

 
 ####### post activities3 - post a reply tweet
        tweet_content = 'Hello @' + status.user.screen_name + '!! For $1 you can make the difference today! Learn how: ' + url + ' Prj: \'' + prj_name + '\''
        print('replying: ' + tweet_content)
        post_tweet(tweet_content)
        print('----------------------------')

 
 
        # tweet_content = 'Hello @' + status.user.screen_name + '! Prj: \'' + prj_name + '\'' + ' Url: ' + url
        # # '!! For $1 you can make the difference today! Learn how: ' +
        #
        #
        # reply_type = 1                              #placeholder
        # reply_to_status_id = 1                      #placeholder
        # print('replying: ' + tweet_content)
        # post_tweet(tweet_content, reply_type, reply_to_status_id)       #added two fields, one for the reply type (is it a tweet or comment) as well as the tweetID so we know where to post a reply to
        # print('----------------------------')
 
 
 
 

####################################################################################
# -----------------------------------------------begin: 10/31 by Jiheng
# private functions

def get_user_id( twitter_id, twitter_screen_name ):
    sql = 'SELECT user_id, twitter_screenname from t_User WHERE twitter_id = ' + twitter_id
    rsp = db.execute_sql( sql ).fetchall()
    if len(rsp) == 0:
        sql = 'INSERT INTO t_User ( twitter_id, twitter_screenname, google_id, google_username) VALUES ( ' + twitter_id + ', "' + twitter_screen_name + '", null, null )'
        rsp = db.execute_sql( sql )
        sql = 'SELECT user_id from t_User WHERE twitter_id = ' + twitter_id
        rsp = db.execute_sql( sql ).fetchall()
        return rsp[0][0]
    else:
        print rsp[0][1]
        # TODO - fix bug
        # if twitter_screen_name != rsp[0][1]:
            # sql = 'UPDATE t_User SET twitter_screenname = ' + '"' + twitter_screen_name + '"' + ' WHERE user_id = ' + str(rsp[0][0])
            # print sql
            # db.execute_sql( sql )
        return rsp[0][0]

def store_twt( user_id, twt_txt, hashtag_cnt):
    # store the tweet
    sql = 'INSERT INTO t_Twt_Received ( post_user_id, twt_received, hash_tag_cnt ) VALUES ( ' + user_id + ', "' + twt_txt + '", ' + hashtag_cnt + ' )'
    db.execute_sql( sql ).fetchall()
    sql = 'SELECT MAX(twt_received_id) FROM t_Twt_Received WHERE post_user_id = ' + user_id + ' AND twt_received = "' + twt_txt + '" AND hash_tag_cnt = ' + hashtag_cnt
    twt_id = db.execute_sql( sql ).fetchall()[0][0]
    
    return twt_id

def receive_tweet( status ):
    # step1: check if the user used BOT. If yes return the user_id; otherwise, create one
    twitter_screen_name = status.user.screen_name
    twitter_id = status.user.id_str
    print twitter_screen_name
    user_id = get_user_id( twitter_id, twitter_screen_name )
        
    # step2: store the tweet
    tweet_txt = status.text
    hashtags = status.entities['hashtags']
    
    
    store_twt( str(user_id), str(tweet_txt), str(len(hashtags)) )
    
####################################################

# def handle_null_project( prj_name ):
    # if len(keys) == 0:
        # call standard project
    # elif 
    
    


# -----------------------------------------------end:   10/31 by Jiheng
####################################################################################

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening
 
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening
        
 
if __name__ == '__main__':
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
   
    stream = Stream(auth, listener)
    print('listener is now under running...')
    stream.filter(track=['#onetoday'])
    
