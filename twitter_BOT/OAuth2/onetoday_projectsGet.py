import sys

from oauth2client import client
from googleapiclient import sample_tools


def api_projects_get(prj_id, argv):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
      sys.argv, 'onetoday', 'v1', __doc__, __file__,
      scope='https://www.googleapis.com/auth/onetoday.readonly')

  try:
    ##########################################################################      
    #API Calls
    project = service.projects().get(projectId=prj_id).execute()
    
    unitCost = project["project"]['unitCost']
    amt_unitCost = int(unitCost["micros"]) / 1000000
    cur_unitCost = unitCost["currency"]
    
    unitQuantity = int(project["project"]['unitDescriptionQuantity'])
    if (unitQuantity == 1):
        unitDescription = project["project"]['unitDescription']
    else:
        unitDescription = project["project"]['unitDescriptionMultiple']
    unit = unitDescription
    
    
    totalDonated = project["projectStats"]['totalDonated']
    amt_totalDonated = int(totalDonated["micros"]) / 1000000
    cur_totalDonated = totalDonated["currency"]
    
    donorsCount = project["projectStats"]['donorsCount']
    
    
    
    charity = project["project"]["charity"]
    if "unitGoal" in charity:
        target_unit = charity["unitGoal"]
    else:
        target_unit = 1000
     
     

    return [amt_unitCost, cur_unitCost, unitQuantity, unit, amt_totalDonated, cur_totalDonated, donorsCount]
    #API Calls
    ##########################################################################      

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run'
      'the application to re-authorize.')

def api_projects_get_target_unit(prj_id, argv):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
      sys.argv, 'onetoday', 'v1', __doc__, __file__,
      scope='https://www.googleapis.com/auth/onetoday.readonly')

  try:
    ##########################################################################      
    #API Calls
    project = service.projects().get(projectId=prj_id).execute()
    
    if "unitGoal" in project["project"]:
        target_unit = project["project"]["unitGoal"]
    else:
        target_unit = 1000

    return target_unit
    #API Calls
    ##########################################################################      

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run'
      'the application to re-authorize.')
      

      
def main(argv):
    plusId = api_projects_get_target_unit("AMiJ0n5JOoaFnzi09oeAU0GZL1yGXbABHIhPlRM", argv)
    print plusId

if __name__ == '__main__':
  main(sys.argv)
