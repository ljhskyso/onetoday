from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

img = Image.open("test.jpg")
draw = ImageDraw.Draw(img)


# font = ImageFont.truetype(<font-file>, <font-size>)
# font = ImageFont.truetype("sans-serif.ttf", 16)


# draw.text((x, y),"Sample Text",(r,g,b))
# draw.text((0, 0),"Sample Text",(255,255,255),font=font)
draw.text((0, 0),"Sample Textasdfuhilaeifuwajegiowaejg;iowejanfuweifunweofubwoguberigbe",(0,0,0))


# draw.line((0, 0) + im.size, fill=128)
# draw.line((0, im.size[1], im.size[0], 0), fill=128)

img.save('sample-out.jpg')