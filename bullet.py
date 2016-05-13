import math

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