import pygame
import sys
import math

width = 1200
height = 700
# (width, height) = (1200, 700)
BLACK = (0, 0, 0)
BROWN = (240,150,0)
GREY = (128,128,128)

def playGame():
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Castle Defence")
	screen.fill(BLACK)

	centers = []

	centers.append((60, 60))
	centers.append(( width - 60, 60))
	centers.append((width - 60, height - 60))
	centers.append((60, height - 60))

	walls = []

	playerCenter = [0 for i in xrange(4)]
	newPlayerCursor = []
	playerCoordinate = []
	playerCursor = []
	playerOrientation = [0 for i in xrange(4)]
	playerCoordinate.append((100,100))

	for i in xrange(200):
		walls.append((width / 2,i))

	for i in xrange(height - 200, height):
		walls.append((width / 2,i))

	for i in xrange(300):
		walls.append((i,height / 2))

	for i in xrange(width - 300, width):
		walls.append((i,height / 2))

	# circle(Surface, color, pos, radius, width=0)

	playerCursor.append(pygame.image.load('green_triangle.png'))
	newPlayerCursor.append(pygame.image.load('green_triangle.png'))
	# playerCursor = pygame.transform.rotate(playerCursor, 270)

	# screen.blit(playerCursor, (100, 100) )

	for center in centers:
		pygame.draw.circle(screen, GREY, center, 40, 0 )
	# pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)

	for wall in walls:
		pygame.draw.rect( screen, BROWN, [wall[0],wall[1],10,10] )

	pygame.display.flip()

	isRunning = True
	clock = pygame.time.Clock()

	unitDistance = 0.3

	# r = pygame.draw.rect(screen, BROWN, [200, 200, 20 , 10] )

	while isRunning:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					playerOrientation[0] = ( (playerOrientation[0] + 5) + 360 ) % 360
					newPlayerCursor[0] = pygame.transform.rotate(playerCursor[0], playerOrientation[0])
				elif event.key == pygame.K_s:
					playerOrientation[0] = ( (playerOrientation[0] - 5) + 360 ) % 360
					newPlayerCursor[0] = pygame.transform.rotate(playerCursor[0], playerOrientation[0])
		screen.fill(BLACK)

		print playerOrientation[0]

		deg = playerOrientation[0]
		x = +1
		y = -1

		if playerOrientation[0] > 90 and playerOrientation[0] <= 180:
			print "here"
			deg = 180 - playerOrientation[0]
			x = -1
			y = -1
		elif playerOrientation[0] > 180 and playerOrientation[0]<= 270:
			deg = playerOrientation[0] - 180
			x = -1
			y = +1
		elif playerOrientation[0] > 270 and playerOrientation[0] <= 360:
			deg = 360 - playerOrientation[0]
			x = +1
			y = +1

		playerCenter[0] = (newPlayerCursor[0].get_rect().x,newPlayerCursor[0].get_rect().y)
		playerCoordinate[0] = (playerCoordinate[0][0] +  (x * unitDistance * math.cos(math.radians(playerOrientation[0] ) ) ) , playerCoordinate[0][1] + (y * unitDistance * math.sin(math.radians(playerOrientation[0] ) ) ) )
		# playerCoordinate[0][1] = 
		screen.blit(newPlayerCursor[0], playerCoordinate[0] )
		for center in centers:
			pygame.draw.circle(screen, GREY, center, 40, 0 )
		# pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)

		for wall in walls:
			pygame.draw.rect( screen, BROWN, [wall[0],wall[1],10,10] )
		pygame.display.update()
		clock.tick(80)

def main():
	playGame()

if __name__ == "__main__":
	main()