import tweepy
import urllib
from datetime import datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def printTextPicture ( background, text1, text2, text3, text4 )
	i = datetime.now()
	now = i.strftime('%Y%m%d-%H%M%S')
	photo_name = '/twitter_BOT/textPictures/' + now + '.jpg'

	#creating text image
	fontsize1 = 28
	fontsize2 = 20
	fnt1 = ImageFont.truetype("Bradley.ttf", fontsize)
	fnt2 = ImageFont.truetype("Bradley.ttf", fontsize)
	txt = Image.new('RGBA', base.size, (255,255,255,0))
	d = ImageDraw.Draw(txt)
	d.text((10,10), text1, font = fnt1, fill=(255,255,255,128))
	d.text((10,60), text2, font = fnt2, fill=(255,255,255,255))
	d.save(textPrinted)
	(textw, texth) = textPrinted.size
	
	#seeting background
	img = Image.open(background)
	(width, height) = img.size
	heightZ = height
	widthZ = width
	
	#resize text according to needs
	textResize = textPrinted.resize((width, ((texth*width)/textw)), Image.ANTIALIAS)
	(text2w, text2h) = textResize.size

	#inserting Text into Background
	offset = ((width - text2w)/2, (height - text2h)/2)
	img.paste(textResize, offset, mask = textResize)
	img.save(photoText)

	return photoText
