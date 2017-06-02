import sys, os, argparse, datetime, iso8601, math, imageio, progressbar, time
from dateutil.tz import tzlocal
from PIL import Image, ImageFont, ImageDraw 

OFFSET = (140, 323)
TMPFOLDER = "tmp"
TIMESCALE = Image.open("resources/scale.png")
CAR = Image.open("resources/car.png")
FONTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resougrces')
FONT = ImageFont.truetype(os.path.join(FONTS_PATH, 'SourceSansPro-Regular.ttf'), 24)

def processImages(args):
	#Get number of files in folder
	num_files = len([f for f in os.listdir(args.input)
					if os.path.isfile(os.path.join(args.input, f)) and f.endswith(args.ext)])
	#Start processing
	count = 0;
	with progressbar.ProgressBar(max_value=num_files, redirect_stdout=True) as bar:
		for filename in os.listdir(args.input):
			if filename.endswith(args.ext): 
				processImage(args.input, filename)
				count += 1
				bar.update(count)
		
def processImage(imagePath, imageName):
	
	#Load image from file
	inputFrame = Image.open(os.path.join(imagePath, imageName))
	
	#Copy timescale as canvas and paste frame in canvas
	canvas = TIMESCALE.copy()
	canvas.paste(inputFrame)
	
	#Calculate Car offset and paste car into canvas
	timestamp = imageName.split("_")[0].replace("-", ":").replace(":", "-", 2)
	date = iso8601.parse_date(timestamp).astimezone(tzlocal())
	timeOffset = date.hour * 18 + math.floor(date.minute / 60 * 18)
	canvas.paste(CAR, (OFFSET[0] + timeOffset, OFFSET[1] + 0), CAR)

	# Draw date on image
	draw = ImageDraw.Draw(canvas)
	draw.text((10, 310), "%s %02d.%02d" % (date.strftime("%a"), date.day, date.month), (0,0,0), font=FONT)
	
	#Save canvas to tmp folder
	canvas.save(os.path.join(imagePath, TMPFOLDER, imageName))
	
	return canvas	
	
def createGif(inputPath, outputFile, fps, ext):
	#Make gif animation
	
	num_files = len([f for f in os.listdir(inputPath)
					if os.path.isfile(os.path.join(inputPath, f)) and f.endswith(ext)])
	count = 0;
	with progressbar.ProgressBar(max_value=num_files, redirect_stdout=True) as bar:
		with imageio.get_writer(outputFile, mode='I', fps=fps) as writer:
			for filename in os.listdir(inputPath):
				image = imageio.imread(os.path.join(inputPath, filename))
				writer.append_data(image)
				count += 1
				bar.update(count)
				
	writer.close()
	print("Gif sucessfuly written to", outputFile)
	
	
def main():
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-i', '--input', dest='input', required= True, help='Path of images to process (all *.png-files)')
	parser.add_argument('-o', '--output', dest='output', required= True, help='Path of processed result gif')
	parser.add_argument('-f', '--file-name', dest='outputFileName', default='result.gif', help='Name of the result gif')
	parser.add_argument('-fps', '--frames-per-second', dest='fps', default=20, type=int, help='Frames per second in gif')
	parser.add_argument('-ex', '--file-extension', dest='ext', default=".png", help='Input file extension')
	args = parser.parse_args()
	
	print("Processing images in", args.input)
	if not os.path.isdir(args.input):
		print("Error: Input direcotry dose not exist")
		return
	if not os.path.isdir(args.output):
		print("Error: Output direcotry dose not exist")
		return
	
	if not os.path.isdir(os.path.join(args.input, TMPFOLDER)):
		os.makedirs(os.path.join(args.input, TMPFOLDER))
	
	processImages(args)
	print("Done processing image, creating gif")
	createGif(os.path.join(args.input, TMPFOLDER), os.path.join(args.output, args.outputFileName), args.fps, args.ext)
	
if __name__ == "__main__":
	main()