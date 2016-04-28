import pygame


class tank:
	# position of the tank
	coordinate = (0,0)

	# the image to display for this tank
	imageFile = ""

	fixedCursor = ""
	mobileCursor = ""


	center = 0

	# current orientation of the tank
	orientation = 0

	# the base rectangle for a tank
	rectangle = ""

	# amount of life for a tank
	life = 100
	
	# boost of this tank
	boost = 50

	# life bar for this tank
	lifeBar = ""

	# boost bar for this tank
	boostBar = ""

	# multiplier to get direction of movement for a tank
	reverse = 1

	def __init__(self, (X, Y), imageFile, orientation, life, boost, lifeBarX, lifeBarY, lifeBarW, lifeBarH, boostBarX, boostBarY, boostBarW, boostBarH):

		self.coordinate = (X,Y)
		self.imageFile = imageFile
		self.orientation = orientation
		self.life = life
		self.boost = boost
		self.lifeBar = pygame.Rect(lifeBarX, lifeBarY, lifeBarW, lifeBarH)
		self.boostBar = pygame.Rect(boostBarX, boostBarY, lifeBarY, lifeBarX)
		self.fixedCursor = pygame.image.load(self.imageFile)
		self.mobileCursor = self.fixedCursor
		self.mobileCursor =  pygame.transform.rotate(self.fixedCursor, self.orientation)
		self.rectangle = pygame.rect

	def rotateAntiClockwise(self, offset):
		self.orientation += offset + 360
		self.orientation %= 360
		self.updateMobileCursor()

	def rotateClockwise(self, offset):
		self.orientation -= offset + 360
		self.orientation %= 360
		self.updateMobileCursor()

	def updateMobileCursor(self):
		self.mobileCursor = pygame.transform.rotate(self.fixedCursor, self.orientation)
	
