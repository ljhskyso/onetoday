import json
from apiclient.discovery import build

def project_search( keyword ):
    
  print('call onetoday for: ' + keyword)
    
  service = build('onetoday', 'v1',
            developerKey='AIzaSyChpIe6eRbzRDlgMecR3IsMBZmWb1WG2Cw')

  # keyword = 'android for autism'

  s_resp =  service.projects().search(
      query=keyword
    ).execute()

  # print(s_resp)

  if 'projects' in s_resp:
      project = s_resp["projects"][0]

      url = project["projectUrl"]
      prj_name = project["tagLine"]
      
      # print('url:               ' + project["projectUrl"])
      # print('tagLine:           ' + project["tagLine"])
      # print('Description:       ' + project["unitDescriptionMultiple"])
      # print('projectFact:       ' + project["projectFact"])
      # print('message:           ' + project["message"])
      # print('shortDescription:  ' + project["unitDescription"])
  else:
      #url = 'no project available'
      #prj_name = 'null'
      
      keyword = "water"
      
      s_resp =  service.projects().search(
      query=keyword
    ).execute()

      project = s_resp["projects"][0]
      
      url = project["projectUrl"]
      prj_name = project["tagLine"]
      
      
#      s_resp =  service.offers().create(
#      categoryID=keyword
#    ).execute()
#
#      project = s_resp["projects"][0]
#      
#      url = project["projectUrl"]
#      prj_name = project["tagLine"]
      
      #using the google api function offers.create
      
      
      
  return [ url, prj_name ]

  
def main():
  keyword = '  china'
  [s1, s2] = project_search( keyword )
  print(s1)
  print(s2)


if __name__ == '__main__':
  main()
