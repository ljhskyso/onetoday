import tweepy
import urllib
from datetime import datetime

def getPictures(photo_url):
	i = datetime.now()
	now = i.strftime('%Y%m%d-%H%M%S')
	photo_name = '/twitter_BOT/images/' + now + '.jpg'
	urllib.urlretrieve(photo_url, photo_name)
	return photo_name
