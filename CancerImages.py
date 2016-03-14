import ImageProcessor
from PIL import Image


##########################################initial pics################################################
'''
for levels in range(1, 5):
	for pics in range(1, 26):
		imageLocale = '/home/jsinghal/Documents/Intel Science Project/Images/DataSetPure/Level ' + str(levels) + '/Image' + str(pics) + '.bmp'	#gets the locale of the image
		localeSave = '/home/jsinghal/Documents/Intel Science Project/Images/DataSetResized/Level ' + str(levels) + '/Image' + str(pics) + '.bmp'
		im = Image.open(imageLocale)	#opens the image
		imR = im.resize((150, 150))	#resized copy
		imR.save(localeSave)		#saves the resized copy

		imageLocaleLesion = '/home/jsinghal/Documents/Intel Science Project/Images/DataSetPure/Level ' + str(levels) + '/Image' + str(pics) + 'Lesion.bmp'
		localeLesionSave = '/home/jsinghal/Documents/Intel Science Project/Images/DataSetResized/Level ' + str(levels) + '/Image' + str(pics) + 'Lesion.bmp'
		imL = Image.open(imageLocaleLesion)
		imLR = imL.resize((150, 150))
		imLR.save(localeLesionSave)'''

for levels in range(1, 5):
	for pics in range(1, 26):
		imageLocale = '/home/jsinghal/Documents/Intel Science Project/Images/DataSetPure/Level ' + str(levels) + '/Image' + str(pics) + '.bmp'	#gets the locale of the image
		localeSave = '/home/jsinghal/Documents/Intel Science Project/Images/DataSetResized2/Level ' + str(levels) + '/Image' + str(pics) + '.bmp'
		im = Image.open(imageLocale)	#opens the image
		imR = im.resize((100, 100))	#resized copy
		imR.save(localeSave)		#saves the resized copy

		imageLocaleLesion = '/home/jsinghal/Documents/Intel Science Project/Images/DataSetPure/Level ' + str(levels) + '/Image' + str(pics) + 'Lesion.bmp'
		localeLesionSave = '/home/jsinghal/Documents/Intel Science Project/Images/DataSetResized2/Level ' + str(levels) + '/Image' + str(pics) + 'Lesion.bmp'
		imL = Image.open(imageLocaleLesion)
		imLR = imL.resize((100, 100))
		imLR.save(localeLesionSave)
