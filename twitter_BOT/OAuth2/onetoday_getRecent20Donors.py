import sys

from oauth2client import client
from googleapiclient import sample_tools

from plus_getUserPhoto import getPlusUserPhoto


def getRecent20DonorsFromOfferId(offer_id, argv):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
      argv, 'onetoday', 'v1', __doc__, __file__,
      # scope='https://www.googleapis.com/auth/plus.me')
      # scope='https://www.googleapis.com/auth/onetoday.readonly')
      scope='https://www.googleapis.com/auth/onetoday')

  try:
    ##########################################################################      
    #API Calls
    
    # person = service.users().get(userId="me").execute()
    # print person
    
    # res = service.offers().createForProject(projectId="AMiJ0n4XXOOPtkJnwjrZfTHSWsQuut-Gxc-cqdA").execute()
    
    # res = service.offers().createForProject(projectId='AMiJ0n7gMJHPNcuhNKvUj9iw95Vy2SFGA5LOM4E').execute()
    res = service.offers().get(offerId = offer_id).execute()
    
    
    donors = res["projectInfo"]["donors"]["users"]
    dodate = res["projectInfo"]["donors"]["donationDates"]
    length = len(donors);
    
    for x in range(0, length):
        
        plusId = donors[x]["plusId"]
        
        [displayname, url] = getPlusUserPhoto(plusId, argv)
        # print displayname
        
        print "ontoday user " + displayname + " donated @ " + str(dodate[x])

    # print res

    #API Calls
    ##########################################################################      

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run'
      'the application to re-authorize.')
      
def main(argv):
    getRecent20DonorsFromOfferId(5707702298738688, argv)
    # getRecent20DonorsFromOfferId(5713144022302720, argv)
    
    
if __name__ == '__main__':
  main(sys.argv)
