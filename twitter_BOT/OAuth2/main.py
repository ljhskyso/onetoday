import sys

sys.path.append('./OAuth2')

from oauth2client import client
from googleapiclient import sample_tools

from plus_getUserPhoto import getPlusUserPhoto
from getPictures import getUserPic

import urllib

import os
import tweepy
import urllib
from datetime import datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def listRecent20DonorsFromOfferId(prj_id, argv):
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
    
    
    # res = service.offers().get(offerId = 5707702298738688).execute()
    res = service.offers().createForProject(projectId=prj_id).execute()
    # res = res[0]
    
    project = res["projectInfo"]["project"]
    projid = project["id"]
    project = res["projectInfo"]["project"]
    projnm = project["tagLine"]
    
    print projid
    print projnm
    # print project["projectFact"]
    print
    print "========================"
    print
    
    donors = res["projectInfo"]["donors"]["users"]
    dodate = res["projectInfo"]["donors"]["donationDates"]
    length = len(donors);
    
    for x in range(0, length):
        
        plusId = donors[x]["plusId"]
        
        [displayname, url] = getPlusUserPhoto(plusId, argv)
        # print displayname
        
        # get bigger size
        url = url + '0'
        
        
        print " user        " + displayname
        print " donated @   " + str(dodate[x])
        print " saved from  " + url
        
    	photo_name = './images_recent_donors/' + projid + "_" + str(x) + '.jpg'
        print " saved at    " + photo_name
        print

        # store the photos
    	urllib.urlretrieve(url, photo_name)

    #API Calls
    ##########################################################################      

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run'
      'the application to re-authorize.')
      
def combine_all_icons():
    
    # get the new image height
    header_height = 10
    footer_height = 10
    # fontsize = 10
    # font = ImageFont.truetype("Ayuthaya.ttf", fontsize)
    # twidth, theight = font.getsize(" ")
    # txt_height = len(img_txt) * theight
        
    # create the new image
    new_img = Image.new('RGB', (4 * 500, 5 * 500), (255,255,255))
    
    # add the text
    dir = './images_recent_donors/'
    s = os.listdir(dir)
    cnt = 0
    for pic in s:
        ext = pic[len(pic) - 3 :len(pic)]
        if ext == "jpg":
            col = cnt % 4
            row = ( cnt - col ) / 4
            x_img = col * 500
            y_img = row * 500
            
            print str(col) + ' ' + str(row)
            
            print dir + pic
            img = Image.open(dir + pic)
            new_img.paste( img, (x_img, y_img) )
        cnt = cnt + 1

            
    
    # paste the old image
    
    # save the new image
    photo_name = "./images_recent_donors/recentdonors.jpg"
    new_img.save(photo_name)
    
    return photo_name
    


def main(argv):
    listRecent20DonorsFromOfferId('AMiJ0n7gMxcFNyUajWjd5Wlcs_pCPMJWgeadcno', argv)
    print combine_all_icons()
    
if __name__ == '__main__':
  main(sys.argv)
