import pygame
import sys
import math

width = 1200
height = 700
# (width, height) = (1200, 700)
BLACK = (0, 0, 0)
BROWN = (240,150,0)
GREY = (128,128,128)

def playGame(numberOfPlayers):
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Castle Defence")
	screen.fill(BLACK)

	# centers for the towers
	centers = []
	centers.append((60, 60))
	centers.append(( width - 60, 60))
	centers.append((width - 60, height - 60))
	centers.append((60, height - 60))

	# walls
	walls = []
	for i in xrange(200):
		walls.append((width / 2,i))
	for i in xrange(height - 200, height):
		walls.append((width / 2,i))
	for i in xrange(300):
		walls.append((i,height / 2))
	for i in xrange(width - 300, width):
		walls.append((i,height / 2))

	# center of every player
	playerCenter = [0 for i in xrange(4)]
	
	# coordinate of every player
	playerCoordinate = []
	playerCoordinate.append((100,100))
	playerCoordinate.append((width - 100, height - 100))
	playerCoordinate.append((width - 100, 100))
	playerCoordinate.append((100,height - 100))

	
	# Orientation of each player
	playerOrientation = [0 for i in xrange(4)]

	# player cursors
	playerCursor = []
	newPlayerCursor = []

	playerCursor.append(pygame.image.load('green_triangle.png'))
	newPlayerCursor.append(pygame.image.load('green_triangle.png'))

	playerCursor.append(pygame.image.load('red_triangle.png'))
	newPlayerCursor.append(pygame.image.load('red_triangle.png'))

	playerCursor.append(pygame.image.load('blue_triangle.png'))
	newPlayerCursor.append(pygame.image.load('blue_triangle.png'))

	playerCursor.append(pygame.image.load('yellow_triangle.png'))
	newPlayerCursor.append(pygame.image.load('yellow_triangle.png'))
	
	for center in centers:
		pygame.draw.circle(screen, GREY, center, 40, 0 )
	
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
				elif event.key == pygame.K_d:
					playerOrientation[1] = ( (playerOrientation[1] + 5) + 360 ) % 360
					newPlayerCursor[1] = pygame.transform.rotate(playerCursor[1], playerOrientation[1])
				elif event.key == pygame.K_f:
					playerOrientation[1] = ( (playerOrientation[1] - 5) + 360 ) % 360
					newPlayerCursor[1] = pygame.transform.rotate(playerCursor[1], playerOrientation[1])
				elif event.key == pygame.K_g:
					playerOrientation[2] = ( (playerOrientation[2] + 5) + 360 ) % 360
					newPlayerCursor[2] = pygame.transform.rotate(playerCursor[2], playerOrientation[2])
				elif event.key == pygame.K_h:
					playerOrientation[2] = ( (playerOrientation[2] - 5) + 360 ) % 360
					newPlayerCursor[2] = pygame.transform.rotate(playerCursor[2], playerOrientation[2])
				elif event.key == pygame.K_j:
					playerOrientation[3] = ( (playerOrientation[3] + 5) + 360 ) % 360
					newPlayerCursor[3] = pygame.transform.rotate(playerCursor[3], playerOrientation[3])
				elif event.key == pygame.K_k:
					playerOrientation[3] = ( (playerOrientation[3] - 5) + 360 ) % 360
					newPlayerCursor[3] = pygame.transform.rotate(playerCursor[3], playerOrientation[3])
		
		screen.fill(BLACK)

		for i in xrange(numberOfPlayers):
			print i
			deg = playerOrientation[i]
			x = +1
			y = -1

			if playerOrientation[i] > 90 and playerOrientation[i] <= 180:
				deg = 180 - playerOrientation[i]
				x = -1
				y = -1
			elif playerOrientation[i] > 180 and playerOrientation[i]<= 270:
				deg = playerOrientation[i] - 180
				x = -1
				y = +1
			elif playerOrientation[i] > 270 and playerOrientation[i] <= 360:
				deg = 360 - playerOrientation[i]
				x = +1
				y = +1

			playerCenter[i] = (newPlayerCursor[i].get_rect().x,newPlayerCursor[i].get_rect().y)
			playerCoordinate[i] = (playerCoordinate[i][0] +  (x * unitDistance * math.cos(math.radians(deg ) ) ) , playerCoordinate[i][1] + (y * unitDistance * math.sin(math.radians(deg ) ) ) )
			# playerCoordinate[0][1] = 

			screen.blit(newPlayerCursor[i], playerCoordinate[i] )
		for center in centers:
			pygame.draw.circle(screen, GREY, center, 40, 0 )
		for wall in walls:
			pygame.draw.rect( screen, BROWN, [wall[0],wall[1],10,10] )
		pygame.display.update()
		clock.tick(80)

def main():
	playGame(4)

if __name__ == "__main__":
	main()