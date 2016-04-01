import pygame
import sys

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

	for i in xrange(200):
		walls.append((width / 2,i))

	for i in xrange(height - 200, height):
		walls.append((width / 2,i))

	for i in xrange(300):
		walls.append((i,height / 2))

	for i in xrange(width - 300, width):
		walls.append((i,height / 2))

	# circle(Surface, color, pos, radius, width=0)


	for center in centers:
		pygame.draw.circle(screen, GREY, center, 40, 0 )
	# pygame.draw.circle(screen, GREY, (60,60), 40, 0)

	for wall in walls:
		pygame.draw.rect( screen, BROWN, [wall[0],wall[1],10,10] )

	pygame.display.flip()

	isRunning = True

	while isRunning:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)

def main():
	playGame()

if __name__ == "__main__":
	main()