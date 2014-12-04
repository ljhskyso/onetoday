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
        keyword = ''
        for hashtag in status.entities['hashtags']:
            if hashtag['text'] != 'onetoday':
                keyword = keyword + ' ' + hashtag['text']
        
####### post activities2 - call onetoday for project info
        print('searching project for: ' + keyword)
        [ url, prj_name ] = project_search( keyword )

####### post activities3 - post a reply tweet
        tweet_content = 'Hello @' + status.user.screen_name + '!! For $1 you can make the difference today! Learn how: ' + url + ' Prj: \'' + prj_name + '\''
        print('replying: ' + tweet_content)
        post_tweet(tweet_content)
        print('----------------------------')
 


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
    
