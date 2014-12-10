import sys

from oauth2client import client
from googleapiclient import sample_tools


def getPlusUserPhoto(user_id, argv):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
      argv, 'plus', 'v1', __doc__, __file__,
      scope='https://www.googleapis.com/auth/plus.me')

  try:
    ##########################################################################      
    #API Calls
    person = service.people().get(userId=user_id).execute()
    
    displayName = person['displayName']
    imageUrl = person['image']['url']

    # print 'The user: %s' % displayName
    # print 'The image: %s' % imageUrl
    # print ''
    
    return [displayName, imageUrl]
    
    # print
    # print '%-040s -> %s' % ('[Activitity ID]', '[Content]')

    # Don't execute the request until we reach the paging loop below.
    request = service.activities().list(
        userId=person['id'], collection='public')

    # Loop over every activity and print the ID and a short snippet of content.
    while request is not None:
      activities_doc = request.execute()
      for item in activities_doc.get('items', []):
        print '%-040s -> %s' % (item['id'], item['object']['content'][:30])

      request = service.activities().list_next(request, activities_doc)

    #API Calls
    ##########################################################################      

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run'
      'the application to re-authorize.')

def main(argv):
    getPlusUserPhoto("me", argv)

if __name__ == '__main__':
  main(sys.argv)
