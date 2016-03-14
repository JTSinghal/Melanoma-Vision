import math
import random
import string
import sys
import ImageProcessor
import sqlite3
from PIL import Image

###################################Database stuff#####################################################
borderDB = sqlite3.connect('connections1Border.db')
borderCurs = borderDB.cursor()
symmetryDB = sqlite3.connect('connections2Symmetry.db')
symmetryCurs = symmetryDB.cursor()
mainDB = sqlite3.connect('connections2Main.db')
mainCurs = mainDB.cursor()


def createTables():	#just used once
	#borderCurs.execute("CREATE TABLE connections1(id INTEGER PRIMARY KEY, connStrength REAL)")
	#symmetryCurs.execute("CREATE TABLE connections2(id INTEGER PRIMARY KEY, connStrength REAL)")
	mainCurs.execute("CREATE TABLE connections3(id INTEGER PRIMARY KEY, connStrength REAL)")

def addConnBorder(strength):
	borderCurs.execute('''INSERT INTO connections1(connStrength) VALUES (?)''', (strength, ))
def addConnSymmetry(strength):
	symmetryCurs.execute('''INSERT INTO connections2(connStrength) VALUES (?)''', (strength, ))
def addConnMain(strength):
	mainCurs.execute('''INSERT INTO connections3(connStrength) VALUES (?)''', (strength, ))

def writeBorder():
	counter = 0
	for x in borderNetwork.connInput:
		for y in x:
			addConnBorder(y)
			counter += 1
			print counter
	borderDB.commit()	
	counter = 0
	for x in borderNetwork.connHidden:
		for y in x:
			addConnBorder(y)
			counter += 1
			print counter
	borderDB.commit()
def writeSymmetry():	#why not try to make this the only way to save and delete the entire table contents before saving new
	for x in symmetryNetwork.connInput:
		for y in x:
			print y	#Y IS A CURSOR FOR SOME REASON
			addConnSymmetry(y)
		symmetryDB.commit()
	for x in symmetryNetwork.connHidden:
		for y in x:
			addConnSymmetry(y)
		symmetryDB.commit()
def writeMain():
	counter = 0
	for x in MAINBRAIN.connInput:
		for y in x:
			addConnMain(y)
	mainDB.commit()
	for x in MAINBRAIN.connHidden:
		for y in x:
			addConnMain(y)
			counter += 1
			print counter
	mainDB.commit()

def readBorderInput(x, y):
	sql = "SELECT connStrength FROM connections1 WHERE id = ?"
	result = borderCurs.execute(sql, (((x * 5000) + (y + 1)), ))
	result = borderCurs.fetchone()
	borderDB.commit()
	print result
	borderNetwork.connInput[x][y] = result

def readBorderHidden(x, y):
	sql = "SELECT connStrength FROM connections1 WHERE id = ?"
	result = borderCurs.execute(sql, ((50000000 + x + 1), )).fetchone()[0]
	if x % 100 == 0:
		print x
	borderNetwork.connHidden[x][y] = result

def readSymmetryInput(x, y):
	sql = "SELECT connStrength FROM connections2 WHERE id = ?"
	result = symmetryCurs.execute(sql, (((x * 3) + (y + 1)), )).fetchone()[0]
	#print result
	symmetryNetwork.connInput[x][y] = result
def readSymmetryHidden(x, y):
	sql = "SELECT connStrength FROM connections2 WHERE id = ?"
	result = symmetryCurs.execute(sql, ((12 + x + 1), )).fetchone()[0]
	symmetryNetwork.connHidden[x][y] = result

def readMainInput(x, y):
	sql = "SELECT connStrength FROM connections3 WHERE id = ?"
	result = mainCurs.execute(sql, (((x * 3) + (y + 1)), )).fetchone()[0]
	print result
	MAINBRAIN.connInput[x][y] = result
def readMainHidden(x, y):
	sql = "SELECT connStrength FROM connections3 WHERE id = ?"
	result = mainCurs.execute(sql, ((12 + x + 1), )).fetchone()[0]
	MAINBRAIN.connHidden[x][y] = result

def deleteBorder():
	for x in range(0, 50005000):
		borderCurs.execute("DELETE FROM connections1 WHERE id = ?", (x + 1, ))
		print x
	borderDB.commit()
def deleteSymmetry():
	for x in range(0, 15):
		symmetryCurs.execute("DELETE FROM connections2 WHERE id = ?", (x + 1, ))
	symmetryDB.commit()
def deleteMain():
	for x in range(0, 15):
		mainCurs.execute("DELETE FROM connections3 WHERE id = ?", (x + 1, ))
	mainDB.commit()

def exitHandler():
	#deleteBorder()
	deleteSymmetry()
	#deleteMain()
	#writeBorder()
	#writeSymmetry()
	#writeMain()
	symmetryCurs.execute("SELECT * FROM connections2")
	for x in symmetryCurs:
		print x
	print ""
	print symmetryCurs.fetchone()
#########################################Network class################################################
class NeuralNetwork(object):
	def __init__(self, numInput, numHidden, numOutput):
		self.numInput = numInput + 1	#nums of nodes in each layer
		self.numHidden = numHidden
		self.numOutput = numOutput

		self.inputLayer = [1] * self.numInput	#creating layers
		self.hiddenLayer = [1] * self.numHidden
		self.outputLayer = [1] * self.numOutput

		#node weight matrixes
		self.connInput = makeMatrix (self.numInput, self.numHidden)
		self.connHidden = makeMatrix (self.numHidden, self.numOutput)
		#initializeVals to random vals
		randomizeMatrix(self.connInput, -0.2, 0.2)
		randomizeMatrix(self.connHidden, -0.2, 0.2)
		#last change matrices for momentum
		self.changeInput = makeMatrix(self.numInput, self.numHidden)
		self.changeOutput = makeMatrix(self.numHidden, self.numOutput)

	def tick(self, inputs):
		for x in range(0, len(inputs)):	#puts values into input nodes
			self.inputLayer[x] = inputs[x]
		for x in range(0, self.numHidden): #fires to hidden layer
			sume = 0.0
			for y in range(0, self.numInput):
				#print self.inputLayer[y]
				#print self.connInput[y][x]
				sume += self.inputLayer[y] * self.connInput[y][x]
			self.hiddenLayer[x] = sigmoid(sume)
		for x in range(0, self.numOutput):
			sume = 0.0
			for y in range(0, self.numHidden):
				sume += self.hiddenLayer[y] * self.connHidden[y][x]
			self.outputLayer[x] = sigmoid(sume)
		return self.outputLayer

	def backProp(self, targets, learningRate, momentum):
		outputErrors = [0] * self.numOutput
		for x in range(0, self.numOutput):	#initial errors
			error = targets[x] - self.outputLayer[x]
			outputErrors[x] = error * dsigmoid(self.outputLayer[x])

		for x in range(0, self.numHidden):	#update hidden to output conns
			for y in range(0, self.numOutput):
				change = outputErrors[y] * self.hiddenLayer[x]
				self.connHidden[x][y] += learningRate * change + momentum * self.changeOutput[x][y]
				self.changeOutput[x][y] = change

		hiddenErrors = [0] * self.numHidden
		for x in range(0, self.numHidden):	#hidden errors
			error = 0.0
			for y in range(0, self.numOutput):
				error += outputErrors[y] * self.connHidden[x][y]
			hiddenErrors[x] = error * dsigmoid(self.hiddenLayer[x])

		for x in range(0, self.numInput):	#update input to hidden conns
			for y in range(0, self.numHidden):
				change = hiddenErrors[y] * self.inputLayer[x]
				self.connInput[x][y] += learningRate * change + momentum * self.changeInput[x][y]
				self.changeInput[x][y] = change

		error = 0.0	#total complete error
		for x in range(0, len(targets)):
			error += 0.5 * (targets[x] - self.outputLayer[x])**2
		return error


def sigmoid (x):
  return math.tanh(x)
def dsigmoid (y):
  return 1 - y**2

def makeMatrix ( I, J, fill=0.0):
  m = []
  for i in range(I):
    m.append([fill]*J)
  return m
  
def randomizeMatrix ( matrix, a, b):
  for i in range ( len (matrix) ):
    for j in range ( len (matrix[0]) ):
      matrix[i][j] = random.uniform(a,b)

################################################Picture first change##################################
pictures = []
pictureRow = []
parsedPixVals = []	
parsedRow = []

for y in range(1, 5):
	for x in range(1, 26):
		locale = '/home/jsinghal/Documents/Intel Science Project/Images/DataSetResized2/Level ' + str(y) + '/Image' + str(x) + 'Lesion.bmp'
		im = Image.open(locale)
		pictureRow.append(im.getdata())
		print pictureRow
	pictures.append(pictureRow)
	pictureRow = []

for x in pictures:
	for y in x:
		parsedRow.append(ImageProcessor.imageParserPixels(y))
	parsedPixVals.append(parsedRow)
	parsedRow = []

print pictures[1][22]

print "done first pic change"

#############################################Picture second change####################################
picturesMain = []
parsedPixValsMain = []

for x in range(1, 51):
	locale = '/home/jsinghal/Documents/Intel Science Project/Images/DataSetMain/LesionSR' + str(x) + '.jpg'
	im = Image.open(locale)
	pixVals = im.getdata()
	picturesMain.append(pixVals)
	parsedPixValsMain.append(ImageProcessor.imageParserPixels(pixVals))

for x in range(51, 91):
	locale = '/home/jsinghal/Documents/Intel Science Project/Images/DataSetMain/LesionSR' + str(x) + '.bmp'
	im = Image.open(locale)
	pixVals = im.getdata()
	picturesMain.append(pixVals)
	parsedPixValsMain.append(ImageProcessor.imageParserPixels(pixVals))

print "done second pic change"

###############################################Main running stuff#####################################

##Border Requirements
#borderNetwork = NeuralNetwork(10000, 5000, 1)
print "done border network"
trainTo = 0
trainTos = []

##Asymmetry Requirements
symmetryNetwork = NeuralNetwork(4, 3, 1)
print "done symmetry network"
strainTo = 0
strainTos = []

def findCenter(edgeCoordinates):
	leftBound = edgeCoordinates[0][0]
	rightBound = edgeCoordinates[-1][0]
	topBound = edgeCoordinates[0][1]
	bottomBound = edgeCoordinates[-1][1]

	for coordinates in edgeCoordinates:
		if coordinates[0] < leftBound:
			leftBound = coordinates[0]
		if coordinates[0] > rightBound:
			rightBound = coordinates[0]
		if coordinates[1] < topBound:
			topBound = coordinates[1]
		if coordinates[1] > bottomBound:
			bottomBound = coordinates[1]

	center = [(leftBound + rightBound) / 2, (topBound + bottomBound) / 2]
	return center

def getNetInputs(picArray):	#parsed
	edgeCoordinates = ImageProcessor.edgeImageMaker(picArray)
	centerX, centerY = findCenter(edgeCoordinates)

	numVerticalBottom = 0
	numVerticalTop = 0
	numHorizontalLeft = 0
	numHorizontalRight = 0
	diagonal1Input = 0
	diagonal2Input = 0

	for x in range(0, len(picArray[centerY])):
		if picArray[centerY][x] == 255:
			if x > centerX:
				numHorizontalRight += 1
			else:
				numHorizontalLeft += 1
	for x in range(0, len(picArray)):
		print x
		if picArray[x][centerX] == 255:
			if x > centerY:
				numVerticalBottom += 1
			else:
				numVerticalTop += 1

	moverX = centerX
	moverY = centerY
	diagonal1Way = 0
	diagonal2Way = 0

	while moverX != 100 and moverY != 0:
		if picArray[moverY][moverX] == 255:
			diagonal1Way += 1
		moverX += 1
		moverY -= 1
	moverX, moverY = centerX, centerY
	while moverX != 0 and moverY != 100:
		if picArray[moverY][moverX] == 255:
			diagonal2Way += 1
		moverX -= 1
		moverY +=1
	moverX, moverY = centerX, centerY
	diagonal1Input = abs(diagonal2Way - diagonal1Way)

	diagonal1Way = 0
	diagonal2Way = 0
	while moverX != 100 and moverY != 100:
		if picArray[moverY][moverX] == 255:
			diagonal1Way += 1
		moverX += 1
		moverY += 1
	moverX = centerX
	moverY = centerY
	while moverX != 0 and moverY != 0:
		if picArray[moverY][moverX] == 255:
			diagonal2Way += 1
		moverX -= 1
		moverY -= 1
	diagonal2Input = abs(diagonal2Way - diagonal1Way)

	return [abs(numVerticalBottom - numVerticalTop), abs(numHorizontalLeft - numHorizontalRight), diagonal1Way, diagonal2Way]

##Color Requirements
def getRGBequiv(coordinateRow, coordinateCol):	#coordinate of picture in the parsed data set
	centerCoord = centers[coordinateRow][coordinateCol]	#gets coord of center in actual pic
	pixValsParsed = imageParser('/home/jsinghal/Documents/Intel Science Project/Images/DataSetResized/Level ' + str(coordinateRow + 1) + '/Image' + str(coordinateCol + 1) + '.bmp')

	return pixValsParsed[centers[coordinateRow]][centers[coordinateCol]]

##User Interface
MAINBRAIN = NeuralNetwork(4, 3, 1)
print "done main network"
#createTables()
print "done creating tables"
#read
'''for x in range(0, 1):	#comment out for now, delete on first run and uncomment next time
	for y in range(0, 2000):
		readBorderInput(x, y)
	print x
for x in range(0, borderNetwork.numHidden):
	for y in range(0, borderNetwork.numOutput):
		readBorderHidden(x, y)'''

'''for x in range(0, symmetryNetwork.numInput - 1):
	for y in range(0, symmetryNetwork.numHidden):
		readSymmetryInput(x, y)
for x in range(0, symmetryNetwork.numHidden):
	for y in range(0, symmetryNetwork.numOutput):
		readSymmetryHidden(x, y)'''

'''for x in range(0, MAINBRAIN.numInput - 1):
	for y in range(0, MAINBRAIN.numHidden):
		readMainInput(x, y)
for x in range(0, MAINBRAIN.numHidden):
	for y in range(0, MAINBRAIN.numOutput):
		readMainHidden(x, y)'''

command = raw_input("WHAT DO YOU WANNA DO? ")
while (command != "STOP"):
	if command == "teach border":
		for levels in range(0, len(pictures)):
			for pic in range(0, len(pictures[levels])):
				if pic == 0:
					trainTo = borderNetwork.tick(pictures[levels][pic])
					trainTos.append(trainTo[0])
				else:
					borderNetwork.tick(pictures[levels][pic])
					borderNetwork.backProp([trainTos[levels]], 0.5, 0.1)
				print "DONE WITH " + str(pic)
		command = raw_input("WHAT DO YOU WANNA DO? ")

	elif command == "teach symmetry":
		for levels in range(0, len(parsedPixVals)):
			for pic in range(0, len(pictures[levels])):
				if pic == 0:
					strainTo = symmetryNetwork.tick(getNetInputs(parsedPixVals[levels][pic]))
					print "gave first pic"
					strainTos.append(strainTo[0])
				else:
					symmetryNetwork.tick(getNetInputs(parsedPixVals[levels][pic]))
					symmetryNetwork.backProp([strainTos[levels]], 0.5, 0.1)
				print "DONE WITH " + str(pic)
		command = raw_input("WHAT DO YOU WANNA DO? ")

	elif command == "teach main":
		for pic in range(0, len(parsedPixValsMain)):
			symInputs = getNetInputs(parsedPixValsMain[pic])
			symOut = symmetryNetwork.tick(symInputs)
			borOut = borderNetwork.tick(picturesMain[pic])

			sizOut = 0
			for x in picturesMain[pic]:
				if x == 255:
					sizOut += 1
			if pic < 50:
				im = str('/home/jsinghal/Documents/Intel Science Project/Images/DataSetMain/Lesion' + str(pic + 1) + '.jpg')
			else:
				im = str('/home/jsinghal/Documents/Intel Science Project/Images/DataSetMain/Lesion' + str(pic + 1) + '.bmp')
			edge = ImageProcessor.edgeImageMaker(parsedPixValsMain[pic])
			centerStuff = findCenter(edge)
			gray = ImageProcessor.imageParserPixels(ImageProcessor.grayScaler(ImageProcessor.gaussianBlur(im)))
			coloOut = gray[centerStuff[1]][centerStuff[0]]
			if pic < 50:
				MAINBRAIN.tick([borOut, symOut, sizOut, coloOut])
				MAINBRAIN.backProp([-1], 0.5, 0.1)
			else:
				MAINBRAIN.tick([borOut, symOut, sizOut, coloOut])
				MAINBRAIN.backProp([1], 0.5, 0.1)
			print pic
		command = raw_input("WHAT DO YOU WANNA DO? ")

	elif command == "take":
		pictureInput = raw_input("WHAT WOULD YOU LIKE TO ENTER? ")
		im = Image.open('/home/jsinghal/Documents/Intel Science Project/Images/Cancer Images/' + pictureInput)	#you need to write the image and .jpg
		imLocaleSave = str('/home/jsinghal/Documents/Intel Science Project/Images/Cancer Images/R' + pictureInput)	#saves the image to a resized folder
		im = im.resize((100, 100))
		im.save(imLocaleSave)
		gaussianVals = ImageProcessor.gaussianBlur(imLocaleSave)
		grayScaleVals = ImageProcessor.grayScaler(gaussianVals)
		segmentedPixVals = ImageProcessor.imageSegmenter(grayScaleVals)
		#tick with inputs of segmented image border network
		outBorder = borderNetwork.tick(segmentedPixVals)
		outBorder = outBorder[0]	#this sets the output of the network to the variable outBorder
		borderOut = trainTos[0]		#this is to make an initial 'train to'
		for x in trainTos:
			if abs(x - outBorder) < borderOut:
				borderOut = x
		symmetryInputs = getNetInputs(segmentedPixVals)
		outSymmetry = symmetryNetwork.tick(symmetryInputs)
		symmetryOut = strainTos[0]
		for x in strainTos:
			if abs(x - outSymmetry) < symmetryOut:
				symmetryOut = x
		sizeOut = 0	#gets the size node of main brain
		for x in segmentedPixVals:
			if x == 255:
				sizeOut += 1
		parsedGrayGaussian = ImageProcessor.imageParserPixels(grayScaleVals)	#this gives a grid to get color from
		edge = edgeImageMaker(segmentedParsedGaussian)
		centerCoord = findCenter(edge)
		colorOut = parsedGrayGaussian[centerCoord[1]][centerCoord[0]]	#gives the color node of mb
		mainInput = [borderOut, symmetryOut, sizeOut, colorOut]
		result = MAINBRAIN.tick()
		if result > 0:
			print result
			boolResult = True
			print "malign"
		elif result < 0:
			print result
			boolResult = False
			print "benign"
		tell = raw_input("WAS IT MALIGN - True OR False? ")
		if boolResult != tell:
			if tell == True:
				MAINBRAIN.backProp([1], 0.5, 0.1)
			elif tell == False:
				MAINBRAIN.backProp([-1], 0.5, 0.1)
			else:
				tell = raw_input("COULD YOU PLEASE ENTER WHAT IT WAS AGAIN: ")
		else:
			borderNetwork.backProp([borderOut], 0.5, 0.1)
			symmetryNetwork.backProp([symmetryOut], 0.5, 0.1)
			if tell == True:
				MAINBRAIN.backProp([1], 0.5, 0.1)
			elif tell == False:
				MAINBRAIN.backProp([-1], 0.5, 0.1)
		command = raw_input("WHAT DO YOU WANNA DO? ")

	elif command == "exit":
		exitHandler()
		sys.exit(0)

	else:
		command = raw_input("COMMAND NOT VALID, PLEASE TRY AGAIN: ")

'''
#test of nn
testBrain = NeuralNetwork(4, 3, 1)
command = raw_input("What should we do? ")
while (command != "STOP"):
	if command == "TAKE":
		inputs = []
		for x in range(0, testBrain.numInput - 1):
			testBrain.inputLayer[x] = input("Enter term " + str(x + 1))
			inputs.append(testBrain.inputLayer[x])
		output = testBrain.tick(inputs)
		print output
		trainTo = input("what to train to? ")
		testBrain.backProp([trainTo], 0.5, 0.1)
		command = raw_input("What should we do? ")

#fix save folder for getting pics'''
