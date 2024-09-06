import pygame
import sys
import random
import time
import math
from tkinter import messagebox

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
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

def checkDistance(objectOne, objectTwo):
    result = math.sqrt((objectTwo[0] - objectOne[0]) ** 2 + (objectTwo[1] - objectOne[1]) ** 2)
    if result > 150:
        return False
    return True

def startingCoordinates():
    playerOne = [random.choice([150, 300, 450, 600, 750, 900]), (random.choice([100, 200, 300, 400, 500, 600]))]
    playerTwo = [random.choice([150, 300, 450, 600, 750, 900]), random.choice([100, 200, 300, 400, 500, 600])]
    while playerTwo == playerOne:
        playerTwo = [random.choice([150, 300, 450, 600, 750, 900]), random.choice([100, 200, 300, 400, 500, 600])]
    stone = [random.choice([300, 450]), random.choice([200, 300])]
    while stone == playerOne or stone == playerTwo:
        stone = [random.choice([300, 450]), random.choice([200, 300])]
    stoneTwo = [random.choice([600, 750]), random.choice([400, 500])]
    while stoneTwo == playerOne or stoneTwo == playerTwo or stone == stoneTwo:
        stoneTwo = [random.choice([600, 750]), random.choice([400, 500])]
    return playerOne, playerTwo, stone, stoneTwo

def createBoard():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(COLOUR)

    # vertical lines
    pygame.draw.line(screen, COLOUR_LINE, (150, 100), (150, 600), 5)
    pygame.draw.line(screen, COLOUR_LINE, (300, 100), (300, 600), 5)
    pygame.draw.line(screen, COLOUR_LINE, (450, 100), (450, 600), 5)
    pygame.draw.line(screen, COLOUR_LINE, (600, 100), (600, 600), 5)
    pygame.draw.line(screen, COLOUR_LINE, (750, 100), (750, 600), 5)
    pygame.draw.line(screen, COLOUR_LINE, (900, 100), (900, 600), 5)

    # horizontal lines
    pygame.draw.line(screen, COLOUR_LINE, (150, 100), (900, 100), 5)
    pygame.draw.line(screen, COLOUR_LINE, (150, 200), (900, 200), 5)
    pygame.draw.line(screen, COLOUR_LINE, (150, 300), (900, 300), 5)
    pygame.draw.line(screen, COLOUR_LINE, (150, 400), (900, 400), 5)
    pygame.draw.line(screen, COLOUR_LINE, (150, 500), (900, 500), 5)
    pygame.draw.line(screen, COLOUR_LINE, (150, 600), (900, 600), 5)

    # smallfont = pygame.font.SysFont('Corbel',20) 
    # text = smallfont.render('quit' , True , (100, 100, 100))
    # pygame.draw.rect(screen, BUTTON_COLOUR, [50, 550, 50, 25])
    # screen.blit(text , (55, 550))

    return screen

def checkCollision(movingPlayer, stationaryPlayer, stone, stoneTwo):
    if movingPlayer == stationaryPlayer or movingPlayer == stone or movingPlayer == stoneTwo:
        return True
    if movingPlayer[0] > 900 or movingPlayer[1] > 600 or movingPlayer[0] < 150 or movingPlayer[1] < 100:
        return True
    return False

def showRadius(coordinates):
    pygame.draw.circle(screen, (255, 0, 0), coordinates, 150)
    playerOne.draw()
    pygame.display.update()
    time.sleep(3)
    createBoard()
    
class displayText():
    def __init__(self, x, y, colour):
        self.text = ''
        self.colour = colour
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.position = [x, y]

    def draw(self, text):
        self.text = self.font.render(text, True, self.colour)
        screen.blit(self.text, self.position)

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
    
    def get_image_pos(self):
        return self.rect

class Player():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 100
        self.can_fire = True
        self.moves_left = 3

    def draw(self):
        screen.blit(self.image, self.image.get_rect(center = (self.rect.x, self.rect.y)))

    def move(self, direction):
        if direction == 'left':
            self.rect.x -= 150
            if checkCollision([self.rect.x, self.rect.y], computer.getComputerCoordinates(), stoneCoordinates, stoneTwoCoordinates):
                self.rect.x += 150
            elif self.moves_left > 0:
                self.moves_left -= 1 
        elif direction == 'right':
            self.rect.x += 150
            if checkCollision([self.rect.x, self.rect.y], computer.getComputerCoordinates(), stoneCoordinates, stoneTwoCoordinates):
                self.rect.x -= 150
            elif self.moves_left > 0:
                self.moves_left -= 1
        elif direction == 'up':
            self.rect.y -= 100
            if checkCollision([self.rect.x, self.rect.y], computer.getComputerCoordinates(), stoneCoordinates, stoneTwoCoordinates):
                self.rect.y += 100
            elif self.moves_left > 0:
                self.moves_left -= 1
        elif direction == 'down':
            self.rect.y += 100
            if checkCollision([self.rect.x, self.rect.y], computer.getComputerCoordinates(), stoneCoordinates, stoneTwoCoordinates):
                self.rect.y -= 100
            elif self.moves_left > 0:
                self.moves_left -= 1
        
    def get_moves(self):
        return self.moves_left
    
    def reset_moves(self):
        self.moves_left = 3

    def get_coordinates(self):
        return [self.rect.x, self.rect.y]

    def fire(self):
        if not check_interception([self.rect.x, self.rect.y], computer.getComputerCoordinates(), stoneCoordinates) and checkDistance([self.rect.x, self.rect.y], computer.getComputerCoordinates()):
            computer.hit()
        if computer.health < 10:
            messagebox.showinfo(title = 'Winner!', message = 'You Win!')
            time.sleep(3)
            pygame.quit()
            sys.exit()
        self.can_fire = False
    
    def hit(self):
        self.health -= 10

class Computer():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 100
        self.can_fire = True
        self.moves_left = 3

    def draw(self):
        screen.blit(self.image, self.image.get_rect(center = (self.rect.x, self.rect.y)))

    def move(self, playerOnePosition, stonePosition):
        self.can_fire = True
        moves = ['l', 'r', 'u', 'd']
        moving = 3
        while moving > 0:
            next_move = random.choice(moves)
            if next_move == 'l':
                if not checkCollision([(self.rect.x-150), self.rect.y], playerOnePosition, stonePosition, stoneTwoCoordinates):
                    self.rect.x -= 150
                    moving -= 1
                    moves = ['l', 'r', 'u', 'd']
                else:
                    moves.remove('l') 
            elif next_move == 'r':
                if not checkCollision([(self.rect.x+150), self.rect.y], playerOnePosition, stonePosition, stoneTwoCoordinates):
                    self.rect.x += 150
                    moving -= 1
                    moves = ['l', 'r', 'u', 'd']
                else:
                    moves.remove('r')
            elif next_move == 'u':
                if not checkCollision([self.rect.x, (self.rect.y-100)], playerOnePosition, stonePosition, stoneTwoCoordinates):
                    self.rect.y -= 100
                    moving -= 1
                    moves = ['l', 'r', 'u', 'd']
                else:
                    moves.remove('u')
            elif next_move == 'd':
                if not checkCollision([self.rect.x, (self.rect.y+100)], playerOnePosition, stonePosition, stoneTwoCoordinates):
                    self.rect.y += 100
                    moving -= 1
                    moves = ['l', 'r', 'u', 'd']
                else:
                    moves.remove('d')
            createBoard()
            playerOneHealthIndicator.draw(str(playerOne.health))
            computerHealthIndicator.draw(str(computer.health))
            if exit_button.draw():
                pygame.quit()
                sys.exit()
            fire_button.draw()
            self.draw()
            playerOne.draw()
            pygame.draw.circle(screen, STONE_COLOUR, stonePosition, 10)
            pygame.draw.circle(screen, STONE_COLOUR, stoneTwoCoordinates, 10)
            pygame.display.update()
            if not check_interception([self.rect.x, self.rect.y], playerOnePosition, stonePosition) and self.can_fire == True and checkDistance([self.rect.x, self.rect.y], playerOnePosition):
                self.fire(playerOnePosition)
                playerOneHealthIndicator.draw(str(playerOne.health))
            time.sleep(1)
        createBoard()
        pygame.event.clear()
        playerOne.reset_moves()
        playerOne.can_fire = True

    def getComputerCoordinates(self):
        return [self.rect.x, self.rect.y]

    def fire(self, playerOnePosition):
        if checkDistance([self.rect.x, self.rect.y], playerOnePosition):
            playerOne.hit()
        if playerOne.health < 10:
            messagebox.showinfo(title = 'Lost!', message = 'You Lose!')
            time.sleep(3)
            pygame.quit()
            sys.exit()
        self.can_fire = False
    
    def hit(self):
        self.health -= 10

pygame.init()
# note that 0, 0 is the top left of the screen

screen = createBoard()
playerOneCoordinates, playerTwoCoordinates, stoneCoordinates, stoneTwoCoordinates = startingCoordinates()

playerOne = Player(playerOneCoordinates[0], playerOneCoordinates[1], pygame.image.load("Terry.png"), 3)

# playerOne = pygame.draw.circle(screen, PLAYER_ONE_COLOUR, playerOneCoordinates, 10)
# playerTwo = pygame.draw.circle(screen, PLAYER_TWO_COLOUR, playerTwoCoordinates, 10)
computer = Computer(playerTwoCoordinates[0], playerTwoCoordinates[1], pygame.image.load("Enemy.png"), 3)

#blue
stone = pygame.draw.circle(screen, STONE_COLOUR, stoneCoordinates, 10)
stoneTwo = pygame.draw.circle(screen, STONE_COLOUR, stoneTwoCoordinates, 10)
#green
title = check_interception(playerOneCoordinates, playerTwoCoordinates, stoneCoordinates)
pygame.display.set_caption(str(title))

exit_img = pygame.image.load('exit.png').convert_alpha()
fire_img = pygame.image.load('fire.png').convert_alpha()
distance_img = pygame.image.load('Distance.png').convert_alpha()
exit_button = Button(350, 635, exit_img, 2)
fire_button = Button(650, 635, fire_img, 2)
distance_button = Button(475, 20, distance_img, 2)

playerOneHealthIndicator = displayText(200, 700, (0, 0, 255))
computerHealthIndicator = displayText(200, 650, (255, 0, 0))
movesLeft = displayText(400, 720, (0, 0, 0))
shotsLeft = displayText(600, 720, (0, 0, 0))

# missedMessage = displayText(200, 200, (0, 0, 0))

run = True
while run:
    hovered = False
    playerOneHealthIndicator.draw(str(playerOne.health))
    computerHealthIndicator.draw(str(computer.health))
    movesLeft.draw(str(playerOne.moves_left))
    if playerOne.can_fire:
        shotsLeft.draw("1")
    else:
        shotsLeft.draw("0")
    if exit_button.draw():
        pygame.quit()
        sys.exit()
    if fire_button.draw() and playerOne.can_fire:
        playerOne.fire()
        playerOneHealthIndicator.draw(str(playerOne.health))
        screen = createBoard()
        pygame.display.update()
    if distance_button.draw():
        showRadius(playerOne.get_coordinates())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and playerOne.get_moves() > 0:
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
    stoneTwo = pygame.draw.circle(screen, STONE_COLOUR, stoneTwoCoordinates, 10)
    playerOne.draw()
    if playerOne.get_moves() == 0:
        computer.move(playerOne.get_coordinates(), stoneCoordinates)
    pygame.display.flip()
    pygame.display.update()

pygame.quit()
sys.exit()
