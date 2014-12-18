import json
from apiclient.discovery import build
from getPictures import getPictures

std_url = 'https://onetoday.google.com/p/WYFbIPaX'
std_prj_name = 'You are a real Hero!'
std_photo_path = '/twitter_BOT/images/std_image.jpg'
std_return = [ std_url, std_prj_name, std_photo_path ]

# -----------------------------------------------

def project_search( keyword ):
    
  print('call onetoday for: ' + keyword)

try:    
  service = build('onetoday', 'v1', developerKey='AIzaSyChpIe6eRbzRDlgMecR3IsMBZmWb1WG2Cw')

  # keyword = 'android for autism'

  if keyword != ' ':
      
      s_resp =  service.projects().search( query=keyword ).execute()

  # print(s_resp)
  
      if 'projects' in s_resp:
          project = s_resp["projects"][0]

          url = project["projectUrl"]
          prj_name = project["tagLine"]
          prj_photo_url = project["photoUrl"]
	  photo_path = getPictures(prj_photo_url)
          # print('url:               ' + project["projectUrl"])
          # print('tagLine:           ' + project["tagLine"])
          # print('Description:       ' + project["unitDescriptionMultiple"])
          # print('projectFact:       ' + project["projectFact"])
          # print('message:           ' + project["message"])
          # print('shortDescription:  ' + project["unitDescription"])
      else:
          #url = 'no project available'
          #prj_name = 'null'
      
          # keyword = 'water'
          #
          # s_resp =  service.projects().search( query=keyword ).execute()
          #
          # project = s_resp["projects"][0]
      
          # url = project["projectUrl"]
          # prj_name = project["tagLine"]
          # prj_photo_url = project["photoUrl"]
      # photo_path = getPictures(prj_photo_url)
          url = std_url
          prj_name = std_prj_name
          photo_path = std_photo_path
      
  else:
        #url = 'no project available'
        #prj_name = 'null'
    
    #         keyword = 'water'
    #
    #         s_resp =  service.projects().search( query=keyword ).execute()
    #
    #         project = s_resp["projects"][0]
    #
    #         url = project["projectUrl"]
    #         prj_name = project["tagLine"]
    #          prj_photo_url = project["photoUrl"]
    # photo_path = getPictures(prj_photo_url)
        url = std_url
        prj_name = std_prj_name
        photo_path = std_photo_path
      
#      s_resp =  service.offers().create(
#      categoryID=keyword
#    ).execute()
#
#      project = s_resp["projects"][0]
#      
#      url = project["projectUrl"]
#      prj_name = project["tagLine"]
      
      #using the google api function offers.create
  return [ url, prj_name, photo_path ]


except:
  print 'cannot connect to Google APIs'
  return std_return


  
def main():
  keyword = ' '
    
  [s1, s2] = project_search( keyword )
  print(s1)
  print(s2)


if __name__ == '__main__':
  main()
  
