import pygame
import sys
import random

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 600
COLOUR = (200, 200, 200)
COLOUR_LINE = (0, 0, 0)
# PLAYER_ONE_COLOUR = (100, 0, 0) 
PLAYER_TWO_COLOUR = (100, 0, 0) #red
STONE_COLOUR = (100, 100, 100) #blue
BUTTON_COLOUR = (0, 50, 100)


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
    if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
        return True
    else:
        return False


def startingCoordinates():
    playerOne = [random.choice([150, 300, 450, 600]), (random.choice([100, 200, 300, 400]))]
    playerTwo = [random.choice([150, 300, 450, 600]), random.choice([100, 200, 300, 400])]
    while playerTwo == playerOne:
        playerTwo = [random.choice([150, 300, 450, 600]), random.choice([100, 200, 300, 400])]
    stone = [random.choice([150, 300, 450, 600]), random.choice([100, 200, 300, 400])]
    while stone == playerOne or stone == playerTwo:
        stone = [random.choice([150, 300, 450, 600]), random.choice([100, 200, 300, 400])]
    return playerOne, playerTwo, stone

def createBoard():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(COLOUR)

    # vertical lines
    pygame.draw.line(screen, COLOUR_LINE, (150, 0), (150, 500), 5)
    pygame.draw.line(screen, COLOUR_LINE, (300, 0), (300, 500), 5)
    pygame.draw.line(screen, COLOUR_LINE, (450, 0), (450, 500), 5)
    pygame.draw.line(screen, COLOUR_LINE, (600, 0), (600, 500), 5)

    # horizontal lines
    pygame.draw.line(screen, COLOUR_LINE, (0, 100), (750, 100), 5)
    pygame.draw.line(screen, COLOUR_LINE, (0, 200), (750, 200), 5)
    pygame.draw.line(screen, COLOUR_LINE, (0, 300), (750, 300), 5)
    pygame.draw.line(screen, COLOUR_LINE, (0, 400), (750, 400), 5)

    # smallfont = pygame.font.SysFont('Corbel',20) 
    # text = smallfont.render('quit' , True , (100, 100, 100))
    # pygame.draw.rect(screen, BUTTON_COLOUR, [50, 550, 50, 25])
    # screen.blit(text , (55, 550))

    return screen

def checkCollision(playerOne, playerTwo, stone):
    if playerOne == playerTwo or playerOne == stone or playerTwo == stone:
        return True
    if playerOne[0] > 600 or playerOne[1] > 400 or playerOne[0] < 150 or playerOne[1] < 100:
        return True
    if playerTwo[0] > 600 or playerTwo[1] > 400 or playerTwo[0] < 150 or playerTwo[1] < 100:
        return True
    return False

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouse over and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

class Player():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * 3), int(height * 3)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, direction):
        if direction == 'left':
            self.rect.x -= 150
            if checkCollision([self.rect.x, self.rect.y], playerTwoCoordinates, stoneCoordinates):
                self.rect.x += 150
        elif direction == 'right':
            self.rect.x += 150
            if checkCollision([self.rect.x, self.rect.y], playerTwoCoordinates, stoneCoordinates):
                self.rect.x -= 150
        elif direction == 'up':
            self.rect.y -= 100
            if checkCollision([self.rect.x, self.rect.y], playerTwoCoordinates, stoneCoordinates):
                self.rect.y += 100
        elif direction == 'down':
            self.rect.y += 100
            if checkCollision([self.rect.x, self.rect.y], playerTwoCoordinates, stoneCoordinates):
                self.rect.y -= 100
        
    def get_image(self):
        return (self.image)
    
    def get_position(self):
        return (self.rect.topleft)
        

pygame.init()
# note that 0, 0 is the top left of the screen

screen = createBoard()
playerOneCoordinates, playerTwoCoordinates, stoneCoordinates = startingCoordinates()

playerOne = Player(playerOneCoordinates[0], playerOneCoordinates[1], pygame.image.load("Terry.png"), 3)

# playerOne = pygame.draw.circle(screen, PLAYER_ONE_COLOUR, playerOneCoordinates, 10)
playerTwo = pygame.draw.circle(screen, PLAYER_TWO_COLOUR, playerTwoCoordinates, 10)
#blue
playerThree = pygame.draw.circle(screen, STONE_COLOUR, stoneCoordinates, 10)
#green
title = check_interception(playerOneCoordinates, playerTwoCoordinates, stoneCoordinates)
pygame.display.set_caption(str(title))

exit_img = pygame.image.load('exit.png').convert_alpha()
exit_button = Button(150, 500, exit_img, 2)

run = True
while run:
    if exit_button.draw():
        pygame.quit()
        sys.exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                playerOne.move('down')
            elif event.key == pygame.K_UP:
                playerOne.move('up')
            elif event.key == pygame.K_RIGHT:
                playerOne.move('right')
            elif event.key == pygame.K_LEFT:
                playerOne.move('left')
            screen = createBoard()
    playerTwo = pygame.draw.circle(screen, PLAYER_TWO_COLOUR, playerTwoCoordinates, 10)
    playerThree = pygame.draw.circle(screen, STONE_COLOUR, stoneCoordinates, 10)
    screen.blit(playerOne.get_image(), playerOne.get_position())
    pygame.display.flip()
    pygame.display.update()

pygame.quit()
sys.exit()
