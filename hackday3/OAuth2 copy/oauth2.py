import json

from httplib2 import Http

from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build

client_email = '123456789000-abc123def456@developer.gserviceaccount.com'
with open("MyProject.p12") as f:
  private_key = f.read()

credentials = SignedJwtAssertionCredentials(client_email, private_key,
    'https://www.googleapis.com/auth/sqlservice.admin')

http = Http()
credentials.authorize(http)

sqladmin = build('sqladmin', 'v1beta3', http=http)
response = sqladmin.instances().list(project='examinable-example-123').execute()

print response