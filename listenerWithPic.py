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
        # Prints the text of the tweet
        print('Tweet user: ' + status.user.screen_name)
        print('Tweet text: ' + status.text)
 
 ####### post activities1 - find the keyword in the tweet      
        keyword = ''
        for hashtag in status.entities['hashtags']:
            if hashtag['text'] != 'onetoday':
                keyword = keyword + ' ' + hashtag['text']
        
####### post activities2 - call onetoday for project info
        print('searching project for: ' + keyword)
        [ url, prj_name, photo_path ] = project_search( keyword )

####### post activities3 - post a reply tweet
      
	###### KIM the content of the text was changed
	tweet_content = '@' + status.user.screen_name + ' $1 can make the difference today! \'' + prj_name + '\'' + url
        # '!! For $1 you can make the difference today! Learn how: ' +
        

	###### KIM the following path includes the address for the picture. You should be able to put in here the picture retrieved from Google
	
	#photo_path = '/twitter_BOT/images/education.jpg'
	#the following line replaces the static path photo_path
	#photo_path = prj_photo_url
	photo_file = photo_path
        print('replying: ' + tweet_content)

	print(status.id)
	print(status.in_reply_to_user_id)
	print(photo_file)


        ###### KIM the following line replaces post_tweet(tweet_content) since the function post_tweet on post.py was modified to receive the path for the image 
	post_tweet(photo_file, tweet_content, status.id)
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
    
