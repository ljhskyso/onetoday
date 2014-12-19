import ConfigParser
import os, sys, time, json
import tweepy

from projects_searchBeta import project_search
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
# db = MySQLDatabase('hw2', user='dbhw',passwd='')
db = MySQLDatabase('twitter_bot', user='root',passwd='onetoday@CT')
# -----------------------------------------------end:   10/31 by Jiheng

# -----------------------------------------------begin: 12/11 by Jiheng
from NSL_get_keyword import NSL_get_keyword

DEFAULT_TRIGGER_HASHTAG = '#onetodaybeta' 
DEFAULT_TRIGGER_ATSIGN  = '@one_today'
# -----------------------------------------------end:   12/11 by Jiheng


class StdOutListener(StreamListener):
    ''' Handles data received from the stream. '''
 
    def on_status(self, status):

        print( 'Tweet user:  ' + status.user.screen_name )
        print( 'Tweet text:  ' + status.text )
        # Picture-urls in tweets
        if 'media' in status.entities:
            for media in status.entities['media']:
                print( 'Tweet image: ' + media['media_url'] )
        else:
            print( 'Tweet image: no media content' )

####### post activities1 - find the keyword in the tweet
        receive_tweet( status )
        keyword = ''
        keyword_array = status.entities['hashtags']
        
# -----------------------------------------------begin: 12/11 by Jiheng
        for hashtag in status.entities['hashtags']:
            if hashtag['text'] != DEFAULT_TRIGGER_HASHTAG:
                keyword = keyword + ' ' + hashtag['text']
        if keyword == '':
            # if there is no keyword hastag found, do NSL
            print('')
            print( 'no keyword hastag found, calling NSL API to get keywords of the content...' )
            rsp = NSL_get_keyword( status.text )
            
            # parse keywords found from NSL into keyword array
            keyword = ' '
            for word in rsp:
                if (word != 'project') :
                    keyword = keyword + ' ' + word
# -----------------------------------------------end:   12/11 by Jiheng


####### post activities2 - call onetoday for project info
        print('searching project for: ' + keyword)
        [ url, prj_name, photo_path ] = project_search( keyword )
        
####### post activities3 - post a reply tweet
      
###### KIM the content of the text was changed
        tweet_content = '@' + status.user.screen_name + ' You can also Be the Hero today! \'' + prj_name + '\'' + url
        # '!! For $1 you can make the difference today! Learn how: ' +
        
       	#tweet_content = 'You can also Be the Hero today! $1 can make a difference \'' + prj_name + '\'' + url

###### KIM the following path includes the address for the picture. You should be able to put in here the picture retrieved from Google
        photo_file = photo_path
	#photo_file = '/twitter_BOT/images/education.jpg'
	#the following line replaces the static path photo_path
	#photo_path = prj_photo_url
	#photo_file = photo_path
        print('replying: ' + tweet_content)

    #    print('status_id: ' + status.id)
     #   print('status_reply_user_id: ' + status.in_reply_to_user_id)
      #  print('photofile: ' + photo_file)


###### KIM the following line replaces post_tweet(tweet_content) since the function post_tweet on post.py was modified to receive the path for the image 
        post_tweet(photo_file, tweet_content, status.id)
        print('----------------------------')
 
    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening
 
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening
 

####################################################################################
# -----------------------------------------------begin: 10/31 by Jiheng
# private functions
def get_user_id( twitter_id, twitter_screen_name ):
    sql = 'SELECT user_id, twitter_screenname from t_User WHERE twitter_id = "' + twitter_id + '"'
    rsp = db.execute_sql( sql ).fetchall()
    if len(rsp) == 0:
        sql = 'INSERT INTO t_User ( twitter_id, twitter_screenname, google_id, google_username) VALUES ( ' + twitter_id + ', "' + twitter_screen_name + '", null, null )'
        rsp = db.execute_sql( sql )
        sql = 'SELECT user_id from t_User WHERE twitter_id = ' + twitter_id
        rsp = db.execute_sql( sql ).fetchall()
        return rsp[0][0]
    else:
        if twitter_screen_name != rsp[0][1]:
            try:
                sql = 'UPDATE t_User SET twitter_screenname = ' + '"' + twitter_screen_name + '"' + ' WHERE user_id = "' + str(rsp[0][0]) + '"'
                db.execute_sql( sql )
            except:
                print 'error! cannot update the screen_name WHILE screen_name has changed for the twitter_id'
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
    
#    while True:
 #       try:
  #          stream = Stream(auth, listener)
   #         print('listener is now under running...')
    #        stream.filter(track=['#onetodaybeta', '#myhero', '@one_today'])
     #   except:
      #      print("stream authentication failed")
       #     print ''
        #    print 'restarting the server............'
         #   print ''

    stream = Stream(auth, listener)
    print('listener is now under running...')
    stream.filter(track=[DEFAULT_TRIGGER_HASHTAG, DEFAULT_TRIGGER_ATSIGN])


