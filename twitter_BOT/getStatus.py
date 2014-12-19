import json
from apiclient.discovery import build
from getPictures import getPictures

def project_status( iprojectId ):
	
	print('getting status for: ' + iprojectId)
	
	service = build('onetoday', 'v1', 
	          developerKey='AIzaSyChpIe6eRbzRDlgMecR3IsMBZmWb1WG2Cw')

	s_status = service.projects().stats().get( projectId = iprojectId ).execute()
	
	project_status = s_status
	totalDonated = s_status["totalDonated"]
	totalMatched = s_status["totalMatched"]
	totalFromBrands = s_status["totalFromBrands"]
	donorsCount = s_status["donorsCount"]
	
	return [ totalDonated, totalMatched, totalFromBrands, donorsCount]

