import pygame
import sys
import random
import time

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
    stone = [random.choice([300, 450]), random.choice([200, 300])]
    while stone == playerOne or stone == playerTwo:
        stone = [random.choice([300, 450]), random.choice([200, 300])]
    return playerOne, playerTwo, stone

def createBoard():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(COLOUR)

    # vertical lines
    pygame.draw.line(screen, COLOUR_LINE, (150, 0), (150, 400), 5)
    pygame.draw.line(screen, COLOUR_LINE, (300, 0), (300, 400), 5)
    pygame.draw.line(screen, COLOUR_LINE, (450, 0), (450, 400), 5)
    pygame.draw.line(screen, COLOUR_LINE, (600, 0), (600, 400), 5)

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

def checkCollision(movingPlayer, stationaryPlayer, stone):
    if movingPlayer == stationaryPlayer or movingPlayer == stone or stationaryPlayer == stone:
        return True
    if movingPlayer[0] > 600 or movingPlayer[1] > 400 or movingPlayer[0] < 150 or movingPlayer[1] < 100:
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
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 100
        self.can_fire = False
        self.moves_left = 3
        self.bullet_amount = 1

    def draw(self):
        screen.blit(self.image, self.image.get_rect(center = (self.rect.x, self.rect.y)))

    def move(self, direction):
        if direction == 'left':
            self.rect.x -= 150
            if checkCollision([self.rect.x, self.rect.y], computer.getComputerCoordinates(), stoneCoordinates):
                self.rect.x += 150
            elif self.moves_left > 0:
                self.moves_left -= 1
        elif direction == 'right':
            self.rect.x += 150
            if checkCollision([self.rect.x, self.rect.y], computer.getComputerCoordinates(), stoneCoordinates):
                self.rect.x -= 150
            elif self.moves_left > 0:
                self.moves_left -= 1
        elif direction == 'up':
            self.rect.y -= 100
            if checkCollision([self.rect.x, self.rect.y], computer.getComputerCoordinates(), stoneCoordinates):
                self.rect.y += 100
            elif self.moves_left > 0:
                self.moves_left -= 1
        elif direction == 'down':
            self.rect.y += 100
            if checkCollision([self.rect.x, self.rect.y], computer.getComputerCoordinates(), stoneCoordinates):
                self.rect.y -= 100
            elif self.moves_left > 0:
                self.moves_left -= 1
        
    def get_moves(self):
        return self.moves_left
    
    def reset_moves(self):
        self.moves_left = 3

    def get_coordinates(self):
        return [self.rect.x, self.rect.y]

class Computer():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 100
        self.can_fire = False
        self.moves_left = 3
        self.bullet_amount = 1

    def draw(self):
        screen.blit(self.image, self.image.get_rect(center = (self.rect.x, self.rect.y)))

    def move(self, playerOnePosition, stonePosition):
        moves = ['l', 'r', 'u', 'd']
        moving = 3
        while moving > 0:
            next_move = random.choice(moves)
            if next_move == 'l':
                if not checkCollision([(self.rect.x-150), self.rect.y], playerOnePosition, stonePosition):
                    self.rect.x -= 150
                    moving -= 1
                    moves = ['l', 'r', 'u', 'd']
                else:
                    moves = ['r', 'u', 'd']
            elif next_move == 'r':
                if not checkCollision([(self.rect.x+150), self.rect.y], playerOnePosition, stonePosition):
                    self.rect.x += 150
                    moving -= 1
                    moves = ['l', 'r', 'u', 'd']
                else:
                    moves = ['l', 'u', 'd']
            elif next_move == 'u':
                if not checkCollision([self.rect.x, (self.rect.y-100)], playerOnePosition, stonePosition):
                    self.rect.y -= 100
                    moving -= 1
                    moves = ['l', 'r', 'u', 'd']
                else:
                    moves = ['l', 'r', 'd']
            elif next_move == 'd':
                if not checkCollision([self.rect.x, (self.rect.y+100)], playerOnePosition, stonePosition):
                    self.rect.y += 100
                    moving -= 1
                    moves = ['l', 'r', 'u', 'd']
                else:
                    moves = ['l', 'r', 'u']
            createBoard()
            if exit_button.draw():
                pygame.quit()
                sys.exit()
            self.draw()
            playerOne.draw()
            pygame.draw.circle(screen, STONE_COLOUR, stonePosition, 10)
            pygame.display.update()
            time.sleep(1)
        pygame.event.clear()
        playerOne.reset_moves()

    def getComputerCoordinates(self):
        return [self.rect.x, self.rect.y]

pygame.init()
# note that 0, 0 is the top left of the screen

screen = createBoard()
playerOneCoordinates, playerTwoCoordinates, stoneCoordinates = startingCoordinates()

playerOne = Player(playerOneCoordinates[0], playerOneCoordinates[1], pygame.image.load("Terry.png"), 3)

# playerOne = pygame.draw.circle(screen, PLAYER_ONE_COLOUR, playerOneCoordinates, 10)
# playerTwo = pygame.draw.circle(screen, PLAYER_TWO_COLOUR, playerTwoCoordinates, 10)
computer = Computer(playerTwoCoordinates[0], playerTwoCoordinates[1], pygame.image.load("Enemy.png"), 3)

#blue
stone = pygame.draw.circle(screen, STONE_COLOUR, stoneCoordinates, 10)
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
        if event.type == pygame.KEYDOWN and playerOne.get_moves() > 0:
            print("doing")
            if event.key == pygame.K_DOWN:
                playerOne.move('down')
            elif event.key == pygame.K_UP:
                playerOne.move('up')
            elif event.key == pygame.K_RIGHT:
                playerOne.move('right')
            elif event.key == pygame.K_LEFT:
                playerOne.move('left')
            screen = createBoard()
    computer.draw()
    stone = pygame.draw.circle(screen, STONE_COLOUR, stoneCoordinates, 10)
    playerOne.draw()
    if playerOne.get_moves() == 0:
        computer.move(playerOne.get_coordinates(), stoneCoordinates)
    pygame.display.flip()
    pygame.display.update()

pygame.quit()
sys.exit()
