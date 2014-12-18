import sys

sys.path.append('./OAuth2')
from onetoday_getPlusUserId import getPlusUserId
from plus_getUserPhoto import getPlusUserPhoto
# from onetoday_getRecent20Donors import getRecent20DonorsFromOfferId
from onetoday_listRecent20Donors import listRecent20DonorsFromOfferId


plusId = getPlusUserId("me", sys.argv)
[name, img] = getPlusUserPhoto(plusId, sys.argv)
# getRecent20DonorsFromOfferId(5707702298738688, sys.argv)
# listRecent20DonorsFromOfferId(sys.argv)

print plusId
print name
print img