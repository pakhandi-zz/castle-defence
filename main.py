import pygame
import sys
import math
from copy import deepcopy
import Server
import thread
from Queue import Queue

import tank
import bullet

pygame.init()
pygame.display.init()


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

BULLET_DAMAGE = 10
# 10 ** 18


width = 1200
height = 700
# (width, height) = (1200, 700)
BLACK = (0, 0, 0)
BROWN = (240,150,0)
GREY = (200,200,200)
WHITE = (255,255,255)
GREEN = (0, 155, 0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)



def playGame(numberOfPlayers):
	TOTAL_TIME = 100000 / 5
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Castle Defence")

	font1 = pygame.font.SysFont('Arial', 20)

	font2 = pygame.font.SysFont('Arial', 40)

	screen.fill(BLACK)

	bullets = []

	# centers for the towers
	centers = []
	centers.append((60, 60))
	centers.append((width - 60, height - 60))
	centers.append(( width - 60, 60))
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

	# player is alive
	playerIsAlive = [1 for i in xrange(4)]
	
	# coordinate of every player
	playerCoordinate = []
	playerCoordinate.append((100,100))
	playerCoordinate.append((width - 140, height - 140))
	playerCoordinate.append((width - 140, 100))
	playerCoordinate.append((100,height - 140))

	# imagefilenames
	imageFilename = ['images/green_tank.png', 'images/red_tank.png', 'images/blue_tank.png', 'images/yellow_tank.png']

	bgImage = pygame.image.load('images/terrain.jpg')

	# Orientation of each player
	playerOrientation = [0 for i in xrange(4)]
	playerOrientation[1] = 180
	playerOrientation[2] = 180

	# details for lifeBar
	playerLifeBarX = [100, width - 230, width - 230, 100]
	playerLifeBarY = [40, height - 50, 40, height - 50]
	playerLifeBarW = 100
	playerLifeBarH = 5

	# details for boost bar
	playerBoostBarX = [100, width - 230, width - 230, 100]
	playerBoostBarY = [50, height - 40, 50, height - 40]
	playerBoostBarW = 100
	playerBoostBarH = 5

	# points
	playerDied = [0 for i in xrange(4)]
	playerKilled = [0 for i in xrange(4)]

	# castleLife
	castleLife = [500 for i in xrange(4)]

	# flames images
	flames = []

	flames.append(pygame.image.load('images/flames0.png'))
	flames.append(pygame.image.load('images/flames1.png'))
	flames.append(pygame.image.load('images/flames2.png'))

	# flames coordinate

	flamesCoordinate = []

	i = 0
	while True:
		if i > width + 20:
			break
		flamesCoordinate.append((i,0))
		flamesCoordinate.append((i,height - 20))
		i = i + 20

	i = 0
	while True:
		if i > height + 20:
			break;
		flamesCoordinate.append((0,i))
		flamesCoordinate.append((width - 20, i))
		i = i + 20

	# electric images
	electrics = []
	electricsHorizontol = []

	electrics.append(pygame.image.load('images/electric0.png'))
	electrics.append(pygame.image.load('images/electric1.png'))

	electricsHorizontol.append(pygame.transform.rotate(electrics[0], 90))
	electricsHorizontol.append(pygame.transform.rotate(electrics[1], 90))

	# electrics coordinate
	electricsCoordinates = []
	electricsHorizontolCoordinates = []

	i = 0
	while True:
		if i >= 200:
			break
		electricsCoordinates.append((width / 2, i))
		i = i + 40

	i = height - 200
	while True:
		if i >= height:
			break
		electricsCoordinates.append((width / 2, i))
		i = i + 40

	i = 0
	while True:
		if i >= 300:
			break
		electricsHorizontolCoordinates.append((i, height / 2))
		i = i + 40

	i = width - 300
	while True:
		if i >= width:
			break
		electricsHorizontolCoordinates.append((i, height / 2))
		i = i + 40

	# electrics rectangle
	electricsRectangle = [pygame.rect for i in xrange(4)]
	electricsRectangle[0] = pygame.Rect(width / 2, 0, 20, 200)
	electricsRectangle[1] = pygame.Rect(width / 2, height - 200, 20, 200)
	electricsRectangle[2] = pygame.Rect(0, height / 2, 300, 20)
	electricsRectangle[3] = pygame.Rect(width - 300, height / 2, 300, 20)

	
	
	for center in centers:
		pygame.draw.circle(screen, GREY, center, 40, 0 )
	
	# for wall in walls:
	# 	pygame.draw.rect( screen, BROWN, [wall[0],wall[1],10,10] )

	pygame.display.flip()

	isRunning = True
	clock = pygame.time.Clock()

	bulletDistance = 1.5

	unitDistance = 0.5
	ftype = 0
	etype = 0

	bulletLifeTime = 500

	rotationOffset = 10

	tanks = []
	for i in xrange(4):
		tanks.append(tank.Tank(playerCoordinate[i], imageFilename[i], playerOrientation[i], 100, 50, playerLifeBarX[i], playerLifeBarY[i], playerLifeBarW, playerLifeBarH, playerBoostBarX[i], playerBoostBarY[i], playerBoostBarW, playerBoostBarH))

	rotateAntiClockwiseKeys = [pygame.K_a, pygame.K_d, pygame.K_g, pygame.K_j]
	rotateClockwiseKeys = [pygame.K_s, pygame.K_f, pygame.K_h, pygame.K_k]

	while isRunning:
		TOTAL_TIME -= 1
		if TOTAL_TIME <= 0:
			break;
		thisBoost = [0 for i in xrange(4)]
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				TOTAL_TIME = 0
				sys.exit(0)
			if event.type == pygame.KEYDOWN:
				for i in xrange(len(rotateAntiClockwiseKeys)):
					if event.key == rotateAntiClockwiseKeys[i]:
						ind = i
						tanks[ind].rotateAntiClockwise(rotationOffset)
				
				for i in xrange(len(rotateClockwiseKeys)):
					if event.key == rotateClockwiseKeys[i]:
						ind = i
						tanks[ind].rotateClockwise(rotationOffset)

				if event.key == pygame.K_z:
					ind = 0
					temp = bullet.Bullet(tanks[ind].orientation, tanks[ind].center, ind)
					bullets.append(temp)
				elif event.key == pygame.K_c:
					ind = 1
					temp = bullet.Bullet(tanks[ind].orientation, tanks[ind].center, ind)
					bullets.append(temp)
				elif event.key == pygame.K_b:
					ind = 2
					temp = bullet.Bullet(tanks[ind].orientation, tanks[ind].center, ind)
					bullets.append(temp)
				elif event.key == pygame.K_m:
					ind = 3
					temp = bullet.Bullet(tanks[ind].orientation, tanks[ind].center, ind)
					bullets.append(temp)
				elif event.key == pygame.K_w:
					ind = 0
					tanks[ind].toggleReverse()
				elif event.key == pygame.K_r:
					ind = 1
					tanks[ind].toggleReverse()
				elif event.key == pygame.K_y:
					ind = 2
					tanks[ind].toggleReverse()
				elif event.key == pygame.K_i:
					ind = 3
					tanks[ind].toggleReverse()
				elif event.key == pygame.K_e:
					ind = 0
					if tanks[ind].boost > 0:
						thisBoost[ind] = 1
						tanks[ind].boost -= 1
				elif event.key == pygame.K_t:
					ind = 1
					if tanks[ind].boost > 0:
						thisBoost[ind] = 1
						tanks[ind].boost -= 1
				elif event.key == pygame.K_u:
					ind = 2
					if tanks[ind].boost > 0:
						thisBoost[ind] = 1
						tanks[ind].boost -= 1
				elif event.key == pygame.K_o:
					ind = 3
					if tanks[ind].boost > 0:
						thisBoost[ind] = 1
						tanks[ind].boost -= 1
	
		
		# respawn dead tank
		for i in xrange(4):
			if playerIsAlive[i] == 0:
				print "creating new ",i
				tanks[i] = (tank.Tank(playerCoordinate[i], imageFilename[i], playerOrientation[i], 100, 50, playerLifeBarX[i], playerLifeBarY[i], playerLifeBarW, playerLifeBarH, playerBoostBarX[i], playerBoostBarY[i], playerBoostBarW, playerBoostBarH))
				playerIsAlive[i] = 1

		# move the tank
		for i in xrange(numberOfPlayers):
			if tanks[i].life <= 0:
				tanks[i].isAlive = 0
			tanks[i].updateCenter()
			tanks[i].updateCoordinate(thisBoost[i])

		# make the base rectangle for the tank
		for j in xrange(numberOfPlayers):
			rect = tanks[j].mobileCursor.get_rect()
			rect.center = tanks[j].center
			if ( tanks[j].orientation > 15 and tanks[j].orientation < 75) or ( tanks[j].orientation > 105 and tanks[j].orientation < 165 ) or (tanks[j].orientation > 195 and tanks[j].orientation < 235) or ( tanks[j].orientation > 285 and tanks[j].orientation < 345 ):
				rect = rect.inflate(-20,-20)
			elif tanks[j].orientation % 90 != 0:
				rect = rect.inflate(-10,-10)
			tanks[j].rectangle = rect

		
		bulletIsAlive = [1 for i in xrange(len(bullets))]

		for i in xrange(len(bullets)):
			for j in xrange(numberOfPlayers):
				rect = tanks[j].rectangle
				if rect.collidepoint(bullets[i].coordinate) and bulletIsAlive[i] == 1:
					tanks[j].life = tanks[j].life - BULLET_DAMAGE
					if tanks[j].life <= 0:
						playerDied[j] = playerDied[j] + 1
						playerKilled[bullets[i].firedBy] += 1
						playerIsAlive[j] = 0
					bulletIsAlive[i] = 0

		# collision with upper and lower flames
		for i in xrange(width):
			point = (i, 20)
			for j in xrange(numberOfPlayers):
				if playerIsAlive[j] == 0:
					continue
				rect = tanks[j].rectangle
				if rect.collidepoint(point):
					playerIsAlive[j] = 0
					playerDied[j] += 1
					continue
			point = (i, height - 20)
			for j in xrange(numberOfPlayers):
				if playerIsAlive[j] == 0:
					continue
				rect = tanks[j].rectangle
				if rect.collidepoint(point):
					playerIsAlive[j] = 0
					playerDied[j] += 1
					continue

		# collision with left and right flames
		for i in xrange(height):
			point = (20, i)
			for j in xrange(numberOfPlayers):
				if playerIsAlive[j] == 0:
					continue
				rect = tanks[j].rectangle
				if rect.collidepoint(point):
					playerIsAlive[j] = 0
					playerDied[j] += 1
					continue
			point = (width - 20, i)
			for j in xrange(numberOfPlayers):
				if playerIsAlive[j] == 0:
					continue
				rect = tanks[j].rectangle
				if rect.collidepoint(point):
					playerIsAlive[j] = 0
					playerDied[j] += 1
					continue

		# collision with electrics
		for i in xrange(4):
			for j in xrange(numberOfPlayers):
				if playerIsAlive[j] == 0:
					continue
				rect = tanks[j].rectangle
				if rect.colliderect(electricsRectangle[i]):
					playerIsAlive[j] = 0
					playerDied[j] += 1
					continue
			for j in xrange(len(bullets)):
				point = bullets[j].coordinate
				rect = electricsRectangle[i]
				if rect.collidepoint(point):
					bulletIsAlive[j] = 0

		# increase living time of bullets
		for i in xrange(len(bullets)):
			bullets[i].timeTravelled = bullets[i].timeTravelled + 1
			if bullets[i].timeTravelled >= bulletLifeTime:
				bulletIsAlive[i] = 0

		# removing bullets
		removed = 0
		for i in xrange(len(bulletIsAlive)):
			if bulletIsAlive[i] == 0:
				bullets.pop(i - removed)
				removed = removed + 1

		# Collision of tanks
		for i in xrange(numberOfPlayers):
			for j in xrange(numberOfPlayers):
				if i == j:
					continue
				if playerIsAlive[j] == 0:
					continue
				rect1 = tanks[i].rectangle
				rect2 = tanks[j].rectangle
				if rect1.colliderect(rect2) == 1:
					playerIsAlive[i] = 0
					playerIsAlive[j] = 0
					playerDied[i] = playerDied[i] + 1
					playerDied[j] = playerDied[j] + 1

		screen.fill(BLACK)
		i = 0
		while i <= 1200:
			j = 0
			while j <= 700:
				screen.blit(bgImage, (i, j))
				j += 200
			i += 200

		 
		for i in xrange(numberOfPlayers):
			pygame.draw.rect(screen, BLACK, tanks[i].boostBar)

		for i in xrange(numberOfPlayers):
			if playerIsAlive[i] == 1:
				rect = deepcopy(tanks[i].boostBar)
				rect.width = tanks[i].boost * 2
				pygame.draw.rect(screen, BLUE, rect)

		for i in xrange(numberOfPlayers):
			pygame.draw.rect(screen, BLACK, tanks[i].lifeBar)

		for i in xrange(numberOfPlayers):
			if playerIsAlive[i] == 1:
				rect = deepcopy(tanks[i].lifeBar)
				rect.width = tanks[i].life
				pygame.draw.rect(screen, GREEN, rect)

		for i in xrange(4):
			pygame.draw.circle(screen, GREY, centers[i], 40, 0 )
			screen.blit(font1.render("+"+str(playerKilled[i]),True, GREEN), (centers[i][0] - 40, centers[i][1] - 20))
			screen.blit(font1.render("/",True, WHITE), (centers[i][0], centers[i][1] - 20))
			screen.blit(font1.render("-"+str(playerDied[i]),True, RED), (centers[i][0] + 5, centers[i][1] - 20))
		
		# display border
		ftype = (ftype + 1) % 3
		for point in flamesCoordinate:
			screen.blit( flames[ftype] , point)
		
		# process bullets
		for i in xrange(len(bullets)):
			bullets[i].timeTravelled = bullets[i].timeTravelled + 1
			bullets[i].updateCoordinate(1.5)
			pygame.draw.circle(screen, BLACK, (int(bullets[i].coordinate[0]), int(bullets[i].coordinate[1])), 2, 0 )

		# display electricity
		etype = (etype + 1) % 2
		for point in electricsCoordinates:
			screen.blit( electrics[etype] , point)
		for point in electricsHorizontolCoordinates:
			screen.blit( electricsHorizontol[etype] , point)
		pygame.draw.rect( screen, BLUE, [100, 5, TOTAL_TIME / 100, 5] )

		# display tanks
		for i in xrange(numberOfPlayers):
			if playerIsAlive[i] == 1:
				screen.blit(tanks[i].mobileCursor, tanks[i].coordinate )

		pygame.display.update()
		clock.tick(80)

	return
	screen.fill(BLACK)
	pygame.display.update()
	screen.blit(font2.render("RANK",True, WHITE), (150, 100))
	screen.blit(font2.render("PLAYER",True, WHITE), (320, 100))
	screen.blit(font2.render("KILLS",True, WHITE), (550, 100))
	screen.blit(font2.render("DEATHS",True, WHITE), (720, 100))
	screen.blit(font2.render("TOTAL",True, WHITE), (930, 100))


	color = [GREEN, RED, BLUE, YELLOW]
	toPrint = [(400, 220), (400, 340), (400, 460), (400, 580)]

	total_score = []
	for i in xrange(numberOfPlayers):
		total_score.append((i, playerKilled[i] - playerDied[i]))
	total_score.sort(reverse=True, key=lambda a: a[1])

	for i in xrange(numberOfPlayers):
		val = total_score[i][0]
		pygame.draw.circle(screen, color[val], toPrint[i], 50, 0)

	toPrint = [(200, 200), (200, 320), (200, 440), (200, 560)]
	for i in xrange(numberOfPlayers):
		screen.blit(font2.render(str(i + 1),True, WHITE), toPrint[i])



	toPrint = [(550, 200), (550, 320), (550, 440), (550, 560)]
	for i in xrange(numberOfPlayers):
		val = total_score[i][0]
		screen.blit(font2.render(str(playerKilled[val]),True, WHITE), toPrint[i])

	toPrint = [(750, 200), (750, 320), (750, 440), (750, 560)]
	for i in xrange(numberOfPlayers):
		val = total_score[i][0]
		screen.blit(font2.render(str(playerDied[val]),True, WHITE), toPrint[i])

	toPrint = [(950, 200), (950, 320), (950, 440), (950, 560)]
	for i in xrange(numberOfPlayers):
		val = total_score[i][0]
		screen.blit(font2.render(str(total_score[i][1]),True, WHITE), toPrint[i])

	pygame.display.update()


	while isRunning:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
		pass


if __name__ == "__main__":
		# ip = ''
		# port = 12345
		# max_players = 4
		# q = Queue()
		# # UP = None
		# DOWN = None
		# UP = [
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e),
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_t),
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_u),
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_o)
		# 		]
		# LEFT = [
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a),
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d),
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_g),
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_j)
		# 		]
		# RIGHT = [
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s),
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_f),
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_h),
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_k)
		# 		]
		# A = [
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_z),
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_c),
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_b),
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m)
		# 		]
		# B = [
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w),
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r),
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_y),
		# 		pygame.event.Event(pygame.KEYDOWN, key=pygame.K_i)
		# 		]

		# thread.start_new_thread(Server.accept_connections, (ip, port, q, max_players, UP, DOWN, LEFT, RIGHT, A, B))
		# connections = 0
		# ready = 0
		# flag = 0
		# while True:
		# 	if connections == ready and flag == 1:
		# 		break
		# 	msg = q.get()
		# 	if msg == 'connect':
		# 		connections += 1
		# 	elif msg == 'Ready':
		# 		ready += 1
		# 	flag = 1
		ready = 4
		playGame(ready)

