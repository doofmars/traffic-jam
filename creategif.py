import os
from PIL import Image, ImageFont, ImageDraw 

OFFSET = (140, 323)


#Open images an image:

inputName = "2017-05-05T13-40-01Z_image.png"
inputFrame = Image.open("sample/" + inputName)
scale = Image.open("resources/scale.png")
car = Image.open("resources/car.png")

#Paste frame in Scale
scale.paste(inputFrame)
scale.paste(car, (OFFSET[0] + 0, OFFSET[1] + 0), car)

# Create font
fonts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts')
font = ImageFont.truetype(os.path.join(fonts_path, 'SourceSansPro-Regular.ttf'), 24)

# Draw date on image
draw = ImageDraw.Draw(scale)
draw.text((10, 310), "Sample Text", (0,0,0), font=font)


scale.save("result.png")