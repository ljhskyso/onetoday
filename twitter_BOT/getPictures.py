import tweepy
import urllib
from datetime import datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def getPictures(photo_url):
	i = datetime.now()
	now = i.strftime('%Y%m%d-%H%M%S')
	photo_name = './images/' + now + '.jpg'
	urllib.urlretrieve(photo_url, photo_name)
	

	#new_image manipulation
	fontsize = 28
	font = ImageFont.truetype("Ayuthaya.ttf", fontsize)
	img = Image.open(photo_name)
	(width, height) = img.size
	heightZ = height
	widthZ = width / 2
	logo = Image.open('./backPicture2.png')
	(logow, logoh) = logo.size
	print logo.mode
	

	#resize logo according to needs
	logo2 = logo.resize((width, ((logoh*width)/logow)), Image.ANTIALIAS)
	(logo2w, logo2h) = logo2.size	

	#inserting logo on pictures
	offset = ((width - logo2w)/2, (height - logo2h)/2)  
	img.paste(logo2, offset, mask=logo2)	
	


	#draw = ImageDraw.Draw(img)
	#draw.text((0, height), "Be the #Hero today!",(255,255,255), font=font )
	img.save(photo_name)

	return photo_name
