import ImageProcessor
import sys
import sqlite3
from PIL import Image

#database requirements
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
	for x in borderNetwork.inputLayer:
		for y in x.connections:
			addConnBorder(y)
			counter += 1
			print counter
	borderDB.commit()	
	counter = 0
	for x in borderNetwork.hiddenLayer:
		for y in x.connections:
			addConnBorder(y)
			counter += 1
			print counter
	borderDB.commit()
def writeSymmetry():	#why not try to make this the only way to save and delete the entire table contents before saving new
	for x in symmetryNetwork.inputLayer:
		for y in x.connections:
			print y	#Y IS A CURSOR FOR SOME REASON
			addConnSymmetry(y)
	symmetryDB.commit()
	for x in symmetryNetwork.hiddenLayer:
		for y in x.connections:
			addConnSymmetry(y)
	symmetryDB.commit()
def writeMain():
	counter = 0
	for x in MAINBRAIN.inputLayer:
		for y in x.connections:
			addConnMain(y)
	mainDB.commit()
	for x in MAINBRAIN.hiddenLayer:
		for y in x.connections:
			addConnMain(y)
			counter += 1
			print counter
	mainDB.commit()

def readBorderInput(x, y):
	sql = "SELECT connStrength FROM connections1 WHERE id = ?"
	result = borderCurs.execute(sql, (((x * 5000) + (y + 1)), )).fetchone()[0]
	if x % 100 == 0:
		print x
	borderNetwork.inputLayer[x].connections[y] = result

def readBorderHidden(x, y):
	sql = "SELECT connStrength FROM connections1 WHERE id = ?"
	result = borderCurs.execute(sql, ((50000000 + x + 1), )).fetchone()[0]
	if x % 100 == 0:
		print x
	borderNetwork.hiddenLayer[x].connections[y] = result

def readSymmetryInput(x, y):
	sql = "SELECT connStrength FROM connections2 WHERE id = ?"
	result = symmetryCurs.execute(sql, (((x * 3) + (y + 1)), )).fetchone()[0]
	#print result
	symmetryNetwork.inputLayer[x].connections[y] = result
def readSymmetryHidden(x, y):
	sql = "SELECT connStrength FROM connections2 WHERE id = ?"
	result = symmetryCurs.execute(sql, ((12 + x + 1), )).fetchone()[0]
	symmetryNetwork.hiddenLayer[x].connections[y] = result

def readMainInput(x, y):
	sql = "SELECT connStrength FROM connections3 WHERE id = ?"
	result = mainCurs.execute(sql, (((x * 3) + (y + 1)), ))
	result = result.fetchone()[0]
	print result
	MAINBRAIN.inputLayer[x].connections[y] = result
def readMainHidden(x, y):
	sql = "SELECT connStrength FROM connections3 WHERE id = ?"
	result = mainCurs.execute(sql, ((12 + x + 1), )).fetchone()[0]
	MAINBRAIN.inputLayer[x].connections[y] = result

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
	deleteBorder()
	deleteSymmetry()
	deleteMain()
	writeBorder()
	writeSymmetry()
	writeMain()

class Neuron(object):
	def __init__(self, value, connections, threshold):
		self.value = value
		self.connections = connections
		self.threshold = threshold
	def fire(self, array):
		if self.value >= self.threshold:
			for x in self.connections:
				for y in range(0, len(array)):
					array[y].value = array[y].value + self.value * x
	def borderFire(self, array):
		if self.value >= self.threshold:
			for x in range(0, len(self.connections)):
				array[x].value += self.connections[x]

#####################################Border Neural Network############################################

class BorderNeuralNetwork(object):
	def __init__(self, numIn, threshold):
		neuronInst = Neuron(0, [], threshold)
		self.inputLayer = []
		self.hiddenLayer = []
		self.output = [neuronInst]	#THRESHOLD NEEDS TO BE CHANGED
		for x in range(0, numIn):
			neuronInst = Neuron(0, [], threshold)
			self.inputLayer.append(neuronInst)

		for x in range(0, int(0.5 * numIn)):
			neuronInst = Neuron(0, [], threshold)
			self.hiddenLayer.append(neuronInst)
			for y in self.inputLayer:
				y.connections.append(0.005)
		for x in self.hiddenLayer:
			x.connections.append(0.005)

	def tick(self):
		for x in self.inputLayer:
			x.borderFire(self.hiddenLayer)
			print x.value
		for x in self.hiddenLayer:
			x.fire(self.output)
			print x.value
		return self.output[0].value

	def clear(self):
		for x in self.hiddenLayer:
			x.value = 0
		self.output[0].value = 0

	def learn(self, target):	
		out = self.output[0].value
		hiddenErrors = []
		hiddenError = 0
		outputError = out * (1 - out) * (target - out)

		for x in self.hiddenLayer:
			for y in x.connections:
				y += outputError * xconnections
			hiddenErrors.append(x.value * (1 - x.value) * (outputError))
		for x in self.inputLayer:
			for y in range(0, len(x.connections)):
				x.connections[y] += hiddenErrors[y] * x.value
###################################################Symmetry border network############################
class SymmetryNeuralNetwork(object):
	def __init__(self, threshold):
		neuronInst = Neuron(0, [], threshold)
		self.inputLayer = []
		self.hiddenLayer = []
		self.outputLayer = [neuronInst]
		self.threshold = threshold
		for x in range(0, 4):	#debug whether you can put it directly in arrays or not
			neuronInst = Neuron(0, [], threshold)
			self.inputLayer.append(neuronInst)
		for x in range(0, 3):
			neuronInst = Neuron(0, [], threshold)
			self.hiddenLayer.append(neuronInst)
			for y in self.inputLayer:
				y.connections.append(0.0005)
			self.hiddenLayer[x].connections.append(0.0005)

	def tick(self):
		for x in self.inputLayer:
			x.fire(self.hiddenLayer)
		for x in self.hiddenLayer:
			x.fire(self.outputLayer)

		if self.outputLayer[0] >= self.threshold:
			return True
		else:
			return False

	def testTick(self):
		for x in self.inputLayer:
			x.fire(self.hiddenLayer)
		for x in self.hiddenLayer:
			x.fire(self.outputLayer)

		return self.outputLayer[0].value

	def clear(self):
		for x in self.hiddenLayer:
			x.value = 0
		self.outputLayer[0].value = 0

	def learn(self, target):	#target = 0 or threshold according to whether or not you wanna fire it
		hiddenErrors = []
		hiddenError = 0
		out = self.outputLayer[0].value
		outputError = out * (1 - out) * (target - out)

		for x in self.hiddenLayer:
			for y in range(0, len(x.connections)):
				x.connections[y] += outputError * x.connections[y]
			hiddenErrors.append(x.value * (1 - x.value) * (outputError))
		for x in self.inputLayer:
			for y in range(0, len(x.connections)):
				x.connections[y] += hiddenErrors[y] * x.value

######################Pictures########################################################################
pictures = []
pictureRow = []
parsedPixVals = []	
parsedRow = []

for y in range(1, 5):
	for x in range(1, 26):
		locale = '/home/jsinghal/Documents/Intel Science Project/Images/DataSetResized/Level ' + str(y) + '/Image' + str(x) + 'Lesion.bmp'
		im = Image.open(locale)
		pictureRow.append(im.getdata())
	pictures.append(pictureRow)
	pictureRow = []

for x in pictures:
	for y in x:
		parsedRow.append(ImageProcessor.imageParserPixels(y))
	parsedPixVals.append(parsedRow)
	parsedRow = []
###########################################User Interface#############################################

###Border Requirements
borderNetwork = BorderNeuralNetwork(10000, 1)
trainTo = 0
trainTos = []

###Asymmetry Requirements
symmetryNetwork = SymmetryNeuralNetwork(1)
strainTo = 0
strainTos = []

def findCenter(edgeCoordinates):
	leftBound = edgeCoordinates[0][0]
	rightBound = edgeCoordinates[-1][0]
	topBound = edgeCoordinate[0][1]
	bottomBound = edgeCoordinate[-1][1]

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

	verticalPixels = []
	numTop = 0
	horizontalPixels = []
	numRight = 0
	diagonal1Pixels = []
	diagonal2Pixels = []

	for levels in parsedDataSet:
		for pics in levels:
			for y in range(0, len(pics)):
				if pics[y][centerX] == 255:
					verticalPixels.append([centerX, y])	#appends coordinates
				if y == centerY:
					for x in range(0, len(pics[y])):
						if pics[y][x] == 255:
							horizontalPixels.append([x, centerY])

	moverX = centerX
	moverY = centerY
	diagonal1Way = 0   #adds to this number then get absolute from the array to get symmetry
	for levels in parsedDataSet:
		for pics in levels:
			while moverX != 150 and moverY != 0:	#top right
				moverX += 1
				moverY -= 1
				if pics[moverY][moverX] == 255:
					diagonal1Way += 1
			moverX = centerX
			moverY = centerY
			diagonal1Pixels.append(diagonal1Way)
			diagonal1Way = 0
			while moverX != 0 and moverY != 150:	#bottom left
				moverX -= 1
				moverY += 1
				if pics[moverY][moverX] == 255:
					diagonal1Way += 1
			moverX = centerX
			moverY = centerY
			diagonal1Pixels.append(diagonal1Way)
			diagonal1Way = 0
			while moverX != 0 and moverY != 0:	#top left
				moverX -= 1
				moverY -= 1
				if pics[moverY][moverX] == 255:
					diagonal1Way += 1
			moverX = centerX
			moverY = centerY
			diagonal2Pixels.append(diagonal1Way)
			diagonal1Way = 0
			while moverX != 150 and moverY != 150:	#bottom right
				moverX += 1
				moverY += 1
				if pics[moverY][moverX] == 255:
					diagonal1Way += 1
			diagonal2Pixels.append(diagonal1Way)

	symmetryIndexes = []
	for cos in verticalPixels:
		if cos[0] > centerX:
			numTop += 1
	for cos in horizontalPixels:
		if cos[1] > centerY:
			numRight += 1

	symmetryIndexes.append(abs(numTop - (len(verticalPixels) - numTop)))
	symmetryIndexes.append(abs(numRight - (len(horizontalPixels) - numRight)))
	symmetryIndexes.append(abs(len(diagonal1Pixels[0]) - len(diagonal1Pixels[1])))
	symmetryIndexes.append(abs(len(diagonal2Pixels[0]) - len(diagonal2Pixels[1])))

	return symmetryIndexes

#######Color Requirements
def getRGBequiv(coordinateRow, coordinateCol):	#coordinate of picture in the parsed data set
	centerCoord = centers[coordinateRow][coordinateCol]	#gets coord of center in actual pic
	pixValsParsed = imageParser('/home/jsinghal/Documents/Intel Science Project/Images/DataSetResized/Level ' + str(coordinateRow + 1) + '/Image' + str(coordinateCol + 1) + '.bmp')

	return pixValsParsed[centers[coordinateRow]][centers[coordinateCol]]

###UserInterface
MAINBRAIN = SymmetryNeuralNetwork(1)
#createTables()
#writeMain()
#read
'''for x in range(0, len(borderNetwork.inputLayer)):
	for y in range(0, len(borderNetwork.inputLayer[x].connections)):
		readBorderInput(x, y)'''
print "starting"
for x in range(0, len(borderNetwork.hiddenLayer)):
	for y in range(0, len(borderNetwork.hiddenLayer[x].connections)):
		readBorderHidden(x, y)

for x in range(0, len(symmetryNetwork.inputLayer)):
	for y in range(0, len(symmetryNetwork.inputLayer[x].connections)):
		readSymmetryInput(x, y)
for x in range(0, len(symmetryNetwork.hiddenLayer)):
	for y in range(0, len(symmetryNetwork.hiddenLayer[x].connections)):
		readSymmetryHidden(x, y)

for x in range(0, len(MAINBRAIN.inputLayer)):
	for y in range(0, len(MAINBRAIN.inputLayer[x].connections)):
		readMainInput(x, y)
for x in range(0, len(MAINBRAIN.hiddenLayer)):
	for y in range(0, len(MAINBRAIN.hiddenLayer[x].connections)):
		readMainHidden(x, y)
	
command = raw_input("WHAT DO YOU WANNA DO?")
while (command != "STOP"):
	if command == "TEACH BORDER":
		for levels in range(0, len(pictures)):
			for pic in range(0, len(pictures[levels])):
				if pics == 0:
					for pixelVals in range(0, len(pictures[level][pic])):
						borderNetwork.inputLayer[pixelVals].value = pic[pixelVals]
					trainTo = borderNetwork.tick()
					borderNetwork.clear()
					trainTos.append(trainTo)
				else:
					for pixelVals in range(0, len(pictures[levels][pic])):
						borderNetwork.inputLayer[pixelVals].value = pic[pixelVals]
					borderNetwork.tick()
					borderNetwork.learn(trainTos[levels])
					borderNetwork.clear()
	elif command == "TEACH SYMMETRY":
		for levels in parsedPixVals:
			for pics in range(0, len(levels)):
				inputs = getNetInputs(pics)
				if pics == 0:
					for neurons in range(0, len(symmetryNetwork.inputLayer)):
						symmetryNetwork.inputLayer[neurons].value = inputs[neurons]
					strainTo = symmetryNetwork.testTick()
					strainTos.append(strainTo)
					symmetryNetwork.clear()
				else:
					for neurons in range(0, len(symmetryNetwork.inputLayer)):
						symmetryNetwork.inputLayer[neurons].value = inputs[neurons]
					symmetryNetwork.testTick()
					symmetryNetwork.learn(strainTos[pics])
					symmetryNetwork.clear()

	elif command == "TAKE":
		pictureInput = raw_input("WHAT WOULD YOU LIKE TO ENTER")
		im = Image.open('/home/jsinghal/Documents/Intel Science Project/Images/Cancer Images/' + pictureInput)
		imLocaleSave = str('home/jsinghal/Documents/Intel Science Project/Images/Denoised Images/R' + pictureInput)	#RG = resized
		im = im.resize((150, 150))
		im.save(imSaveLocale)
		gaussianVals = ImageProcessor.gaussianBlur(imLocaleSave)
		for x in range(0, len(borderNetwork.inputLayer)):
			borderNetwork.inputLayer[x].value = gaussianVals[x]
		outBorder = borderNetwork.tick()
		borderOut = trainTos[0]
		for x in trainTos:
			if abs(x - outBorder) < borderOut:
				borderOut = x		#borderOut is the first node of main
		segmentedParsedGaussian = ImageProcessor.imageParserPixels(ImageProcessor.imageSegmenter(ImageProcessor.grayScaler(gaussianVals)))#this is parsed and grayscale and segmented
		symmetryInputs = getNetInputs(segmentedParsedGaussian)
		for x in range(0, len(symmetryInputs)):
			symmetryNetwork.inputLayer[x].value = symmetryInputs[x]
		outSymmetry = symmetryNetwork.testTick()
		symmetryOut = strainTos[0]
		for x in strainTos:
			if abs(x - outSymmetry) < symmetryOut:
				symmetryOut = x		#symmetryOut is the second nodeof main
		sizeOut = 0
		for x in segmentedParsedGaussian:
			for y in rows:
				if segmentedParsedGaussian == 255:
					sizeOut += 1	#sizeOut is the third node of main
		parsedGrayGaussian = ImageProcessor.imageParserPixels(ImageProcessor.grayScaler(gaussianVals))
		edge = edgeImageMaker(segmentedParsedGaussian)
		centerCoord = findCenter(edge)
		colorOut = parsedGrayGaussian[centerCoord[1]][centerCoord[0]] #colorOut is the 4th
		mainInput = [borderOut, symmetryOut, sizeOut, colorOut]
		for x in range(0, len(MAINBRAIN.inputLayer)):
			MAINBRAIN.inputLayer[x].value = mainInput[x]
		result = str(MAINBRAIN.tick())
		print result
		tell = raw_input("Malign - True or False?")
		if result != tell:
			if tell == True:
				MAINBRAIN.learn(1)	#change this - might not be threshold
			elif tell == False:
				MAINBRAIN.learn(0.5)	#whatever the thresold divide by 2
		elif result == tell:
			borderNetwork.learn(borderOut)
			borderNetwork.clear()
			symmetryNetwork.learn(symmetryOut)
			symmetryNetwork.clear()
	elif command == "EXIT":
		exitHandler()
		sys.exit(0)

