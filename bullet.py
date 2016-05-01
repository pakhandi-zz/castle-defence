import math

def getDirection(orientation):
	deg = orientation
	x = +1
	y = -1

	if orientation > 90 and orientation <= 180:
		deg = 180 - orientation
		x = -1
		y = -1
	elif orientation > 180 and orientation<= 270:
		deg = orientation - 180
		x = -1
		y = +1
	elif orientation > 270 and orientation <= 360:
		deg = 360 - orientation
		x = +1
		y = +1

	return deg, x, y

class Bullet:

	timeTravelled = 0
	orientation = 0
	coordinate = (0,0)
	firedBy = -1

	def __init__(self, orientation, coordinate, firedBy):
		self.orientation = orientation
		self.coordinate = coordinate
		self.firedBy = firedBy

		self.updateCoordinate(30)

	def updateCoordinate(self, unitDistance):
		deg, x, y = getDirection(self.orientation)
		self.coordinate = (self.coordinate[0] + (x * unitDistance * math.cos(math.radians(deg))) , self.coordinate[1] + (y * unitDistance * math.sin(math.radians(deg))) )