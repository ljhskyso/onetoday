from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import SignedJwtAssertionCredentials
import httplib2
import os.path

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

f = file('%s/%s' % (SITE_ROOT,'client_secret.json'), 'rb')
key = f.read()
f.close()

http = httplib2.Http()
storage = Storage('analytics.dat')
credentials = storage.get()

if credentials is None or credentials.invalid:
    credentials = SignedJwtAssertionCredentials(' 861582065756-ha6l6i5bmf2fue7ovkfe3vdm87qjvvjf@developer.gserviceaccount.com', key, scope='https://www.google.com/analytics/feeds/')
    storage.put(credentials)
else:
    credentials.refresh(http)

http = credentials.authorize(http)
service = build(serviceName='analytics', version='v3', http=http)

data_query = service.data().ga().get(
    ids = table_id.channel_value,
    start_date = date_start,
    end_date = date_end,
    metrics = 'ga:pageviews,ga:visitors',
    sort = '-ga:pageviews').execute()

query = data_query.get('totalsForAllResults')

for key, value in query.iteritems():
          print '%s: %s' % (key,value)