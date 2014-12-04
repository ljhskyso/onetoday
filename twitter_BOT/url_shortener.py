import pprint
import sys

from oauth2client import client
from apiclient import sample_tools

def shortener(argv, input):
  service, flags = sample_tools.init(
      argv, 'urlshortener', 'v1', __doc__, __file__,
      scope='https://www.googleapis.com/auth/urlshortener')

  try:
    url = service.url()

    # Create a shortened URL by inserting the URL into the url collection.
    body = {'longUrl': input}
    resp = url.insert(body=body).execute()
    # pprint.pprint(resp)

    short_url = resp['id']
    
    print(short_url)
    
    
    # # Convert the shortened URL back into a long URL
    # resp = url.get(shortUrl=short_url).execute()
    # pprint.pprint(resp)

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run'
      'the application to re-authorize')

if __name__ == '__main__':
    url = 'http://2cood.com/2cood_logo_square2.png' 
  shortener(sys.argv, url)
