from PIL import Image
import numpy as np
import cv2

def imageParser(imageLocale):	#WORKS #imageLocale needs to be in quotes	#this function is pretty much only used for gaussianBlur
    cancerImageMain = Image.open(imageLocale)
    pixelValues = list(cancerImageMain.getdata())

    (width, height) = cancerImageMain.size 
    rowMaker = []
    pixelValuesInPic = []

    previousX = 0
    for x in range(0, len(pixelValues)):
            if ((x %(width)) == width-1) :
                rowMaker.append(pixelValues[x])
                pixelValuesInPic.append(rowMaker)
                rowMaker = []
            else :
		rowMaker.append(pixelValues[x])
    #print pixelValuesInPic
    return pixelValuesInPic
			
def imageParserPixels(pixelArray):
	rowMaker = []
	pixelValuesInPic = []

	for x in range(0, len(pixelArray)):
		if ((x % 100) == 99):
			rowMaker.append(pixelArray[x])
			pixelValuesInPic.append(rowMaker)
			rowMaker = []
		else:
			rowMaker.append(pixelArray[x])

	return pixelValuesInPic

def imageDeParser(parsedArray):	#WORKS
	deparsedArray = []
	for x in range(len(parsedArray)):
		for y in range(len(parsedArray[x])):
			deparsedArray.append(parsedArray[x][y])
	return deparsedArray

picturePlaceholder = []
pictureChanger = []

################Image Denoiser
def gaussianBlur(imageLocale):    #only blurs three so that a lot stays the same

    global picturePlaceholder
    global pictureChanger

    picturePlaceholder = imageParser(imageLocale)
    pictureChanger = picturePlaceholder
    numrows = len(picturePlaceholder) - 1
    numcols = len(picturePlaceholder[0]) - 1
    for rows in range(0, numrows):  #makes the kernel
        for cols in range(0, numcols):
            if rows == 0 and cols == 0:
		try:
                	picturePlaceholder[rows][cols] = averageCorner(rows, cols, pictureChanger[rows][cols], pictureChanger[rows + 1][cols], pictureChanger[rows + 1][cols + 1], pictureChanger[rows][cols + 1])
		except:
			print 'FAILEDC1 '+ str(rows) + ' ' + str(cols)
			break
            elif rows == 0 and cols == numcols:
		try:                
			picturePlaceholder[rows][cols] = averageCorner(rows, cols, pictureChanger[rows][cols], pictureChanger[rows + 1][cols], pictureChanger[rows][cols - 1], pictureChanger[rows + 1][cols - 1])
		except:
			print 'FAILEDC2 '+ str(rows) + ' ' + str(cols)
			break
            elif rows == numrows and cols == 0:
		try:
                	picturePlaceholder[rows][cols] = averageCorner(rows, cols, pictureChanger[rows][cols], pictureChanger[rows][cols + 1], pictureChanger[rows - 1][cols], pictureChanger[rows - 1][cols + 1])
		except:
			print 'FAILEDC3 '+ str(rows) + ' ' + str(cols)
			break
	    elif rows == numrows and cols == numcols:
		try:
                	picturePlaceholder[rows][cols] = averageCorner(rows, cols, pictureChanger[rows][cols], pictureChanger[rows][cols - 1], pictureChanger[rows - 1][cols], pictureChanger[rows - 1][cols - 1])
		except:
			print 'FAILEDC4 '+ str(rows) + ' ' + str(cols)
			break
            elif cols == 0:
		try:
                	picturePlaceholder[rows][cols] = averageEdge(rows, cols, pictureChanger[rows][cols], pictureChanger[rows - 1][cols], pictureChanger[rows + 1][cols], pictureChanger[rows - 1][cols + 1], pictureChanger[rows][cols + 1], pictureChanger[rows + 1][cols + 1])
		except:
			print 'FAILEDC5 '+ str(rows) + ' ' + str(cols)
			break
            elif cols == numcols:
		try:
	                picturePlaceholder[rows][cols] = averageEdge(rows, cols, pictureChanger[rows][cols], pictureChanger[rows - 1][cols], pictureChanger[rows + 1][cols], pictureChanger[rows - 1][cols - 1], pictureChanger[rows][cols - 1], pictureChanger[rows + 1][cols - 1])
		except:
			print 'FAILEDC6 '+ str(rows) + ' ' + str(cols)
			break
            elif rows == 0:
		try:
                	picturePlaceholder[rows][cols] = averageEdge(rows, cols, pictureChanger[rows][cols], pictureChanger[rows][cols - 1], pictureChanger[rows][cols + 1], pictureChanger[rows + 1][cols - 1], pictureChanger[rows + 1][cols], pictureChanger[rows + 1][cols + 1])
		except:
			print 'FAILEDC7 '+ str(rows) + ' ' + str(cols)
			break
            elif rows == numrows:
		try:
                	picturePlaceholder[rows][cols] = averageEdge(rows, cols, pictureChanger[rows][cols], pictureChanger[rows][cols - 1], pictureChanger[rows][cols + 1], pictureChanger[rows - 1][cols - 1], pictureChanger[rows - 1][cols], pictureChanger[rows - 1][cols + 1])
		except:
			print 'FAILEDC8 '+ str(rows) + ' ' + str(cols)
			break
            else:
		try:
                	picturePlaceholder[rows][cols] = averageReg(rows, cols, pictureChanger[rows][cols], pictureChanger[rows][cols - 1], pictureChanger[rows][cols + 1], pictureChanger[rows - 1][cols - 1], pictureChanger[rows - 1][cols], pictureChanger[rows - 1][cols + 1], pictureChanger[rows + 1][cols - 1], pictureChanger[rows + 1][cols], pictureChanger[rows + 1][cols + 1])
		except:
			print (rows, cols)
			break
    return imageDeParser(picturePlaceholder)

#so it goes throught eh first 2 rows, without hassle, but when it gets to row three, it faults at [2][2]

def averageCorner(r, c, v1, v2, v3, v4): #v1 is the value that needs to be changed
    global picturePlaceholder

    averageValue = ((v1[0] + v2[0] + v3[0] + v4[0]) / 4, (v1[1] + v2[1] + v3[1] + v4[1]) / 4, (v1[2] + v2[2] + v3[2] + v4[2]) / 4)

    picturePlaceholder[r][c] = averageValue
    return picturePlaceholder[r][c] #in the end this happens

def averageEdge(r, c, v1, v2, v3, v4, v5, v6): #v1 is the value that needs to be changed
    global picturePlaceholder

    averageValue = ((v1[0] + v2[0] + v3[0] + v4[0] + v5[0] + v6[0]) / 6, (v1[1] + v2[1] + v3[1] + v4[1] + v5[1] + v6[1]) / 6, (v1[2] + v2[2] + v3[2] + v4[2] + v5[2] + v6[2]) / 6)

    picturePlaceholder[r][c] = averageValue
    return picturePlaceholder[r][c] #in the end this happens

def averageReg(r, c, v1, v2, v3, v4, v5, v6, v7, v8, v9): #v1 is the value that needs to be changed
    global picturePlaceholder

    averageValue = ((v1[0] + v2[0] + v3[0] + v4[0] + v5[0] + v6[0] + v7[0] + v8[0] + v9[0]) / 8, (v1[1] + v2[1] + v3[1] + v4[1] + v5[1] + v6[1] + v7[1] + v8[1] + v9[1]) / 8, (v1[2] + v2[2] + v3[2] + v4[2] + v5[2] + v6[2] + v7[2] + v8[2] + v9[2]) / 8)

    picturePlaceholder[r][c] = averageValue
    return picturePlaceholder[r][c] #in the end this happens


def grayScaler(imgPixVals):	#RUN THIS AFTER NLDENOISER 	#WORKS
	grayScalePixVals = []	#this function takes a deparsed array
	sume = 0
	for pixVals in imgPixVals:
		for x in range(0, len(pixVals)):

			if x == 0:
				sume += 0.21 * pixVals[x]
			elif x == 1:
				sume += 0.72 * pixVals[x]
			else:
				sume += 0.07 * pixVals[x]
		grayScalePixVals.append(sume)
		sume = 0
	return grayScalePixVals	#returns deparsed array

def reImage(pixelVals, savePlace, width, height):#WORKS#the function puts the image back into image form instead of an array of grayscale pixel values#where does it save? #how does it save? #RUN THIS FUCTION AFTER DENOISING AND AFTER GRAYSCALER
	denoisedImage = Image.new("L", (width, height))
	denoisedImage.putdata(pixelVals)
	denoisedImage.save(savePlace)	#this "savePlace" is the same place as denoised also needs to have name and file type at end
    
################Boundary Finding
def imageSegmenter(grayScaleVals):
	tempGrayScaleVals = grayScaleVals	#WORKS
	for x in range(0, len(tempGrayScaleVals)):
		if abs(0 - tempGrayScaleVals[x]) <= 127:
			tempGrayScaleVals[x] = 255
		elif abs(255 - tempGrayScaleVals[x]) <= 128:
			tempGrayScaleVals[x] = 0
	return tempGrayScaleVals

def imageSegmenterWithSave(grayScaleVals, edgeDetectedSavePlace):	#segments into white gray and black and makes picture
	tempGrayScaleVals = grayScaleVals	#WORKS
	for x in range(0, len(tempGrayScaleVals)):
		if abs(0 - tempGrayScaleVals[x]) <= 127:
			tempGrayScaleVals[x] = 255
		elif abs(255 - tempGrayScaleVals[x]) <= 128:
			tempGrayScaleVals[x] = 0

	detectedImage = Image.new("L", (100, 100))
	detectedImage.putdata(tempGrayScaleVals)
	detectedImage.save(edgeDetectedSavePlace)

def edgeImageMaker(pixelValuesInPic):	#parsed parameter
	hotSpot = [] #takes the indexes of parsed picture and puts them in an array so that computer knows where edge is
	numrows = len(pixelValuesInPic) - 1
	numcols = len(pixelValuesInPic[0]) - 1
	for x in range(0, (numrows + 1)):
		for y in range(0, (numcols + 1)):
			if x == 0 and y == 0:
				print pixelValuesInPic[x][y]
				if abs(pixelValuesInPic[x][y + 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x + 1][y] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x + 1][y + 1] - pixelValuesInPic[x][y]) >= 127:
					hotSpot.append([x, y])
			elif x == 0 and y == numcols:
				if abs(pixelValuesInPic[x][y - 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x + 1][y] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x + 1][y - 1] - pixelValuesInPic[x][y]) >= 127:
					hotSpot.append([x, y])
			elif x == numrows and y == 0:
				if abs(pixelValuesInPic[x][y + 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x - 1][y] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x - 1][y + 1] - pixelValuesInPic[x][y]) >= 127:
					hotSpot.append([x, y])
			elif x == numrows and y == numcols:
				if abs(pixelValuesInPic[x][y - 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x - 1][y] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x - 1][y - 1] - pixelValuesInPic[x][y]) >= 127:
					hotSpot.append([x, y])
			elif  x == 0:
				if abs(pixelValuesInPic[x][y - 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x + 1][y - 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x + 1][y] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x + 1][y + 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x][y + 1] - pixelValuesInPic[x][y]) >= 127:
					hotSpot.append([x, y])
			elif x == numrows:
				if abs(pixelValuesInPic[x][y - 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x - 1][y - 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x - 1][y] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x - 1][y + 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x][y + 1] - pixelValuesInPic[x][y]) >= 127:
					hotSpot.append([x, y])
			elif y == 0:	#out of range?
				if abs(pixelValuesInPic[x - 1][y] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x - 1][y + 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x][y + 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x + 1][y + 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x + 1][y] - pixelValuesInPic[x][y]) >= 127:
					hotSpot.append([x, y])
			elif y == numcols:
				if abs(pixelValuesInPic[x - 1][y] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x - 1][y - 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x][y - 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x + 1][y - 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x + 1][y] - pixelValuesInPic[x][y]) >= 127:
					hotSpot.append([x, y])
			else:
				if abs(pixelValuesInPic[x - 1][y - 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x - 1][y] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x - 1][y + 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x][y + 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x][y - 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x + 1][y - 1] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x + 1][y] - pixelValuesInPic[x][y]) >= 127 or abs(pixelValuesInPic[x + 1][y + 1] - pixelValuesInPic[x][y]) >= 127:
					hotSpot.append([x, y])
	return hotSpot 
