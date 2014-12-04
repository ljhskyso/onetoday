import tweepy, time, sys
 
def post_tweet(tweet_content, reply_type, reply_to_status_id):
                                            #added the decision tree where if reply type is "1" then it responds as a normal tweet. Otherwise
    if reply_type == 1:                     #we reply back to the tweet as a reply
        
        # argfile = str(sys.argv[1])
 
    #enter the corresponding information from your Twitter application:
        CONSUMER_KEY = 'BGpaGCjm9GDTIh6faQVj24TlE'#keep the quotes, replace this with your consumer key
        CONSUMER_SECRET = 'PV18Pv7Ewp23IUsPIS3uYikq2BbPs9Hubl9sK4zm7kCgfvAEIn'#keep the quotes, replace this with your consumer secret key
        ACCESS_KEY = '2800992971-Cq7Yz1LE1hNvExrXl3ghe2BJY781hhzM6fZqb2G'#keep the quotes, replace this with your access token
        ACCESS_SECRET = 'o37J0HKqEKPpfeCu9CNnXR7okW92ULCBKMHxSvxKbqzzZ'#keep the quotes, replace this with your access token secret
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)
 
    # filename=open(argfile,'r')
    # f=filename.readlines()
    # filename.close()
 
    # for line in f:
        api.update_status(tweet_content)
        # time.sleep(60)#Tweet every 60 seconds
###############


    else:
        api.update_status(tweet_content, reply_to_status_id)
        
        
        
    
