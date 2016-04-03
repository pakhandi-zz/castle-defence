import pygame
import sys
import math
from copy import deepcopy
import server
import thread
from Queue import Queue

pygame.init()
pygame.display.init()

class Bullet:

	def __init__(self):
		timeTravelled = 0
		orientation = 0
		coordinate = (0,0)
		firedBy = -1
		# return self

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
	TOTAL_TIME = 100000
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

	# center of every player
	playerCenter = [0 for i in xrange(4)]
	
	# coordinate of every player
	playerCoordinate = []
	playerCoordinate.append((100,100))
	playerCoordinate.append((width - 140, height - 140))
	playerCoordinate.append((width - 140, 100))
	playerCoordinate.append((100,height - 140))

	# player cursors
	playerCursor = []
	newPlayerCursor = []

	playerCursor.append(pygame.image.load('green_tank.png'))
	newPlayerCursor.append(pygame.image.load('green_tank.png'))

	playerCursor.append(pygame.image.load('red_tank.png'))
	newPlayerCursor.append(pygame.image.load('red_tank.png'))

	playerCursor.append(pygame.image.load('blue_tank.png'))
	newPlayerCursor.append(pygame.image.load('blue_tank.png'))

	playerCursor.append(pygame.image.load('yellow_tank.png'))
	newPlayerCursor.append(pygame.image.load('yellow_tank.png'))

	# Orientation of each player
	playerOrientation = [0 for i in xrange(4)]
	playerOrientation[1] = 180
	newPlayerCursor[1] = pygame.transform.rotate(playerCursor[1], playerOrientation[1])

	playerOrientation[2] = 180
	newPlayerCursor[2] = pygame.transform.rotate(playerCursor[2], playerOrientation[2])

	# Player rectangle
	playerRectangle = [pygame.rect for i in xrange(4)]

	# Player Life
	playerLife = [100 for i in xrange(4)]

	# player life bar
	playerLifeBar = [pygame.rect for i in xrange(4)]
	playerLifeBar[0] = pygame.Rect(100, 40, 100, 5)
	playerLifeBar[1] = pygame.Rect(width - 230, height - 50, 100, 5)
	playerLifeBar[2] = pygame.Rect(width - 230, 40, 100, 5)
	playerLifeBar[3] = pygame.Rect(100, height - 50, 100, 5)

	# player reverse
	playerReverse = [1 for i in xrange(4)]


	# points
	playerDied = [0 for i in xrange(4)]
	playerKilled = [0 for i in xrange(4)]

	# castleLife
	castleLife = [500 for i in xrange(4)]

	# flames images
	flames = []

	flames.append(pygame.image.load('flames0.png'))
	flames.append(pygame.image.load('flames1.png'))
	flames.append(pygame.image.load('flames2.png'))

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

	electrics.append(pygame.image.load('electric0.png'))
	electrics.append(pygame.image.load('electric1.png'))

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

	# life of each player
	playerLife = [100 for i in xrange(4)]
	
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

	# r = pygame.draw.rect(screen, BROWN, [200, 200, 20 , 10] )

	while isRunning:
		TOTAL_TIME -= 1
		if TOTAL_TIME <= 0:
			break;
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				TOTAL_TIME = 0
				sys.exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					playerOrientation[0] = ( (playerOrientation[0] + rotationOffset) + 360 ) % 360
					newPlayerCursor[0] = pygame.transform.rotate(playerCursor[0], playerOrientation[0])
				elif event.key == pygame.K_s:
					playerOrientation[0] = ( (playerOrientation[0] - rotationOffset) + 360 ) % 360
					newPlayerCursor[0] = pygame.transform.rotate(playerCursor[0], playerOrientation[0])
				elif event.key == pygame.K_d:
					playerOrientation[1] = ( (playerOrientation[1] + rotationOffset) + 360 ) % 360
					newPlayerCursor[1] = pygame.transform.rotate(playerCursor[1], playerOrientation[1])
				elif event.key == pygame.K_f:
					playerOrientation[1] = ( (playerOrientation[1] - rotationOffset) + 360 ) % 360
					newPlayerCursor[1] = pygame.transform.rotate(playerCursor[1], playerOrientation[1])
				elif event.key == pygame.K_g:
					playerOrientation[2] = ( (playerOrientation[2] + rotationOffset) + 360 ) % 360
					newPlayerCursor[2] = pygame.transform.rotate(playerCursor[2], playerOrientation[2])
				elif event.key == pygame.K_h:
					playerOrientation[2] = ( (playerOrientation[2] - rotationOffset) + 360 ) % 360
					newPlayerCursor[2] = pygame.transform.rotate(playerCursor[2], playerOrientation[2])
				elif event.key == pygame.K_j:
					playerOrientation[3] = ( (playerOrientation[3] + rotationOffset) + 360 ) % 360
					newPlayerCursor[3] = pygame.transform.rotate(playerCursor[3], playerOrientation[3])
				elif event.key == pygame.K_k:
					playerOrientation[3] = ( (playerOrientation[3] - rotationOffset) + 360 ) % 360
					newPlayerCursor[3] = pygame.transform.rotate(playerCursor[3], playerOrientation[3])
				elif event.key == pygame.K_z:
					temp = Bullet()
					temp.firedBy = 0
					temp.timeTravelled = 0
					temp.orientation = playerOrientation[0]
					temp.coordinate = playerCenter[0]
					deg, x, y = getDirection(temp.orientation)
					temp.coordinate = (temp.coordinate[0] +  (x * 30 * math.cos(math.radians(deg ) ) ) , temp.coordinate[1] + (y * 30 * math.sin(math.radians(deg ) ) ) )
					bullets.append(temp)
				elif event.key == pygame.K_c:
					temp = Bullet()
					temp.firedBy = 1
					temp.timeTravelled = 0
					temp.orientation = playerOrientation[1]
					temp.coordinate = playerCenter[1]
					deg, x, y = getDirection(temp.orientation)
					temp.coordinate = (temp.coordinate[0] +  (x * 30 * math.cos(math.radians(deg ) ) ) , temp.coordinate[1] + (y * 30 * math.sin(math.radians(deg ) ) ) )
					bullets.append(temp)
				elif event.key == pygame.K_b:
					temp = Bullet()
					temp.firedBy = 2
					temp.timeTravelled = 0
					temp.orientation = playerOrientation[2]
					temp.coordinate = playerCenter[2]
					deg, x, y = getDirection(temp.orientation)
					temp.coordinate = (temp.coordinate[0] +  (x * 30 * math.cos(math.radians(deg ) ) ) , temp.coordinate[1] + (y * 30 * math.sin(math.radians(deg ) ) ) )
					bullets.append(temp)
				elif event.key == pygame.K_m:
					temp = Bullet()
					temp.firedBy = 3
					temp.timeTravelled = 0
					temp.orientation = playerOrientation[3]
					temp.coordinate = playerCenter[3]
					deg, x, y = getDirection(temp.orientation)
					temp.coordinate = (temp.coordinate[0] +  (x * 30 * math.cos(math.radians(deg ) ) ) , temp.coordinate[1] + (y * 30 * math.sin(math.radians(deg ) ) ) )
					bullets.append(temp)
				elif event.key == pygame.K_w:
					if playerReverse[0] == 1:
						playerReverse[0] = -1
					else:
						playerReverse[0] = 1
				elif event.key == pygame.K_r:
					if playerReverse[1] == 1:
						playerReverse[1] = -1
					else:
						playerReverse[1] = 1
				elif event.key == pygame.K_y:
					if playerReverse[2] == 1:
						playerReverse[2] = -1
					else:
						playerReverse[2] = 1
				elif event.key == pygame.K_i:
					if playerReverse[3] == 1:
						playerReverse[3] = -1
					else:
						playerReverse[3] = 1
		
		for i in xrange(4):
			if playerIsAlive[i] == 0:
				playerLife[i] = 100
				if i == 1 or i == 2:
					playerOrientation[i] = 180
				else:
					playerOrientation[i] = 0
				newPlayerCursor[i] = pygame.transform.rotate(playerCursor[i], playerOrientation[i])
				playerIsAlive[i] = 1
				if i == 0:
					playerCoordinate[i] = (100, 100)
				elif i == 1:
					playerCoordinate[i] = (width - 100, height - 100)
				elif i == 2:
					playerCoordinate[i] = (width - 100, 100)
				else:
					playerCoordinate[i] = (100, height - 100)

		# print len(bullets)

		bulletIsAlive = [1 for i in xrange(len(bullets))]

		for i in xrange(len(bullets)):
			for j in xrange(numberOfPlayers):
				rect = playerRectangle[j]
				if rect.collidepoint(bullets[i].coordinate) and bulletIsAlive[i] == 1:
					playerLife[j] = playerLife[j] - BULLET_DAMAGE
					if playerLife[j] <= 0:
						playerDied[j] = playerDied[j] + 1
						playerKilled[bullets[i].firedBy] += 1
						playerIsAlive[j] = 0
					bulletIsAlive[i] = 0

		for i in xrange(numberOfPlayers):

			if playerLife <= 0:
				playerIsAlive[i] = 0

			deg, x, y = getDirection(playerOrientation[i])
			playerCenter[i] = newPlayerCursor[i].get_rect().center
			playerCenter[i] = (playerCenter[i][0] + playerCoordinate[i][0] , playerCenter[i][1] + playerCoordinate[i][1])
			playerCoordinate[i] = (playerCoordinate[i][0] +  (x * playerReverse[i] * unitDistance * math.cos(math.radians(deg ) ) ) , playerCoordinate[i][1] + (y *  playerReverse[i] * unitDistance * math.sin(math.radians(deg ) ) ) )
			screen.blit(newPlayerCursor[i], playerCoordinate[i] )

		for j in xrange(numberOfPlayers):
			rect = newPlayerCursor[j].get_rect()
			rect.center = playerCenter[j]
			if ( playerOrientation[j] > 15 and playerOrientation[j] < 75) or ( playerOrientation[j] > 105 and playerOrientation[j] < 165 ) or (playerOrientation[j] > 195 and playerOrientation[j] < 235) or ( playerOrientation[j] > 285 and playerOrientation[j] < 345 ):
				rect = rect.inflate(-20,-20)
			elif playerOrientation[j] % 90 != 0:
				rect = rect.inflate(-10,-10)
			playerRectangle[j] = rect

		# collision with upper and lower flames
		for i in xrange(width):
			point = (i, 20)
			for j in xrange(numberOfPlayers):
				if playerIsAlive[j] == 0:
					continue
				rect = playerRectangle[j]
				# pygame.draw.rect(screen, GREY, [rect.x, rect.y, rect.width, rect.height])
				if rect.collidepoint(point):
					playerIsAlive[j] = 0
					playerDied[j] += 1
					print "Hit"
					continue
			point = (i, height - 20)
			for j in xrange(numberOfPlayers):
				if playerIsAlive[j] == 0:
					continue
				rect = playerRectangle[j]
				if rect.collidepoint(point):
					playerIsAlive[j] = 0
					playerDied[j] += 1
					print "Hit"
					continue

		# collision with left and right flames
		for i in xrange(height):
			point = (20, i)
			for j in xrange(numberOfPlayers):
				if playerIsAlive[j] == 0:
					continue
				rect = playerRectangle[j]
				if rect.collidepoint(point):
					playerIsAlive[j] = 0
					playerDied[j] += 1
					print "Hit"
					continue
			point = (width - 20, i)
			for j in xrange(numberOfPlayers):
				if playerIsAlive[j] == 0:
					continue
				rect = playerRectangle[j]
				if rect.collidepoint(point):
					playerIsAlive[j] = 0
					playerDied[j] += 1
					print "Hit"
					continue

		# collision with electrics
		for i in xrange(4):
			for j in xrange(numberOfPlayers):
				if playerIsAlive[j] == 0:
					continue
				rect = playerRectangle[j]
				if rect.colliderect(electricsRectangle[i]):
					playerIsAlive[j] = 0
					playerDied[j] += 1
					print "Hit"
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
				rect1 = playerRectangle[i]
				rect2 = playerRectangle[j]
				if rect1.colliderect(rect2) == 1:
					playerIsAlive[i] = 0
					playerIsAlive[j] = 0
					playerDied[i] = playerDied[i] + 1
					playerDied[j] = playerDied[j] + 1

		screen.fill(BLACK)

		for i in xrange(numberOfPlayers):
			if playerIsAlive[i] == 1:
				screen.blit(newPlayerCursor[i], playerCoordinate[i] )

		for i in xrange(numberOfPlayers):
			pygame.draw.rect(screen, WHITE, playerLifeBar[i])

		for i in xrange(numberOfPlayers):
			if playerIsAlive[i] == 1:
				rect = deepcopy(playerLifeBar[i])
				rect.width = playerLife[i]
				pygame.draw.rect(screen, GREEN, rect)

		for i in xrange(len(bullets)):
			bullets[i].timeTravelled = bullets[i].timeTravelled + 1
			deg, x, y = getDirection(bullets[i].orientation)
			bullets[i].coordinate = (bullets[i].coordinate[0] +  (x * bulletDistance * math.cos(math.radians(deg ) ) ) , bullets[i].coordinate[1] + (y * bulletDistance * math.sin(math.radians(deg ) ) ) )
			pygame.draw.circle(screen, WHITE, (int(bullets[i].coordinate[0]), int(bullets[i].coordinate[1])), 2, 0 )

		for i in xrange(4):
			pygame.draw.circle(screen, GREY, centers[i], 40, 0 )
			screen.blit(font1.render("+"+str(playerKilled[i]),True, GREEN), (centers[i][0] - 40, centers[i][1] - 20))
			screen.blit(font1.render("/",True, WHITE), (centers[i][0], centers[i][1] - 20))
			screen.blit(font1.render("-"+str(playerDied[i]),True, RED), (centers[i][0] + 5, centers[i][1] - 20))

		# for wall in walls:
		# 	pygame.draw.rect( screen, BROWN, [wall[0],wall[1],10,10] )
		ftype = (ftype + 1) % 3
		for point in flamesCoordinate:
			screen.blit( flames[ftype] , point)
		etype = (etype + 1) % 2
		for point in electricsCoordinates:
			screen.blit( electrics[etype] , point)
		for point in electricsHorizontolCoordinates:
			screen.blit( electricsHorizontol[etype] , point)
		pygame.draw.rect( screen, BLUE, [100, 5, TOTAL_TIME / 100, 5] )
		pygame.display.update()
		clock.tick(80)
	screen.fill(BLACK)
	pygame.display.update()
	screen.blit(font2.render("RANK",True, WHITE), (150, 100))
	screen.blit(font2.render("PLAYER",True, WHITE), (320, 100))
	screen.blit(font2.render("KILLS",True, WHITE), (550, 100))
	screen.blit(font2.render("DEATHS",True, WHITE), (720, 100))
	screen.blit(font2.render("TOTAL",True, WHITE), (930, 100))


	color = [GREEN, RED, BLUE, YELLOW]
	toPrint = [(400, 220), (400, 340), (400, 460), (400, 580)]

	playerKilled
	playerDied
	numberOfPlayers
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
        q = Queue()
        thread.start_new_thread(server.accept_connections, (q,))
        connections = 0
        ready = 0
        flag = 0
        while True:
            if connections == ready and flag == 1:
                break
            msg = q.get()
            if msg == 'connect':
                connections += 1
            elif msg == 'Ready':
                ready += 1
            flag = 1
        # ready = 4
        playGame(ready)

