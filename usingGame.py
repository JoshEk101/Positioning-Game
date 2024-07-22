import pygame
import sys
import random

def check_interception(A, B, C):
    x1, y1 = A
    x2, y2 = B
    x, y = C
    
    # Check for collinearity. Since this is a simple version, if the stone is not collinear,
    # then there is no way that the stone could interrupt the path of the two players. Essentially,
    # we are looking for one straight line.
    area = x1*(y2 - y) + x2*(y - y1) + x*(y1 - y2)
    if area != 0:
        return False 
    
    # This checks to see if the stone's coordinates lie between the players. Since we have
    # already checked that this is a straight line, if it turns out the stone's coordinates
    # lie between the two players, then we can say the path is interrupted.
    # This program also assumes that if we have collinearity, and the stone's coordinate is the 
    # same as a players, then the path is interrupted.
    if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
        return True
    else:
        return False

def randomCoordinates():
    playerOne = [random.choice([150, 300, 450, 600]), (random.choice([100, 200, 300, 400]))]
    playerTwo = [random.choice([150, 300, 450, 600]), random.choice([100, 200, 300, 400])]
    stone = [random.choice([150, 300, 450, 600]), random.choice([100, 200, 300, 400])]
    return playerOne, playerTwo, stone

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 500
COLOUR = (100, 0, 100)
COLOUR_LINE = (0, 0, 0)
PLAYER_ONE_COLOUR = (100, 0, 0)
PLAYER_TWO_COLOUR = (0, 100, 0)
STONE_COLOUR = (0, 0, 100)

pygame.init()

surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
surface.fill(COLOUR)
# note that 0, 0 is the top left of the screen

# vertical lines
pygame.draw.line(surface, COLOUR_LINE, (150, 0), (150, 500), 5)
pygame.draw.line(surface, COLOUR_LINE, (300, 0), (300, 500), 5)
pygame.draw.line(surface, COLOUR_LINE, (450, 0), (450, 500), 5)
pygame.draw.line(surface, COLOUR_LINE, (600, 0), (600, 500), 5)

# horizontal lines
pygame.draw.line(surface, COLOUR_LINE, (0, 100), (750, 100), 5)
pygame.draw.line(surface, COLOUR_LINE, (0, 200), (750, 200), 5)
pygame.draw.line(surface, COLOUR_LINE, (0, 300), (750, 300), 5)
pygame.draw.line(surface, COLOUR_LINE, (0, 400), (750, 400), 5)

playerOne, playerTwo, stone = randomCoordinates()

#red
pygame.draw.circle(surface, PLAYER_ONE_COLOUR, playerOne, 10)
#green
pygame.draw.circle(surface, PLAYER_TWO_COLOUR, playerTwo, 10)
#blue
pygame.draw.circle(surface, STONE_COLOUR, stone, 10)

title = check_interception(playerOne, playerTwo, stone)
pygame.display.set_caption(str(title))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()