import pygame
import random

pygame.init()

# Uses all uppercase to signal that this variable should not change.
# No constants in python for some reason
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

isRunning = True

playerScore = 0
enemyScore = 0

ballSpeedX = 5
ballSpeedY = 5

delayChange = False

enemySpeedY = 5

newRound = False

# Sending the ball in a somewhat random direction based on the speed I would like the ball to change at
match random.randint(1, 2):
    case 1:
        ballSpeedX *= 1
    case 2:
        ballSpeedX *= -1
match random.randint(1, 2):
    case 1:
        ballSpeedY *= 1
    case 2:
        ballSpeedY *= -1

# Setting the main screen for the game.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Visual for the player's paddle
player = pygame.Rect((0, 255, 15, 125)) # (left, top, width, height)
# Visual for the ball
ball = pygame.Rect((493, 300, 15, 15))
# Visual for the enemy
enemy = pygame.Rect((785, 255, 15, 125))
# Visual for center line
centerLine = pygame.Rect((400, 0, 1, 800))

frameRate = pygame.time.Clock()

font = pygame.font.SysFont('georgia', 24, italic = False, bold = False)
playerText = font.render(str(playerScore), True, (255, 255, 255))

while isRunning == True:
    # Checks for when the user wants to exit the game.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

    font = pygame.font.SysFont('georgia', 24, italic = False, bold = False)
    playerText = font.render(str(playerScore), True, (255, 255, 255))
    enemyText = font.render(str(enemyScore), True, (255, 255, 255))

    # Fills the screen again to avoid any artifacts from moving objects
    screen.fill((25, 25, 25))

    screen.blit(playerText, (370, 0))
    screen.blit(enemyText, (418, 0))

    pygame.draw.rect(screen, (107, 192, 239), player) # RGB Values (Red, Green, Blue)
    pygame.draw.rect(screen, (239, 107, 116), enemy)
    pygame.draw.rect(screen, (250, 250, 250), centerLine)
    pygame.draw.rect(screen, (173, 150, 178), ball)

    # Checks if the a new round has started, which is only trigged when the ball reaches the left or right side of the screen 
    if newRound == True:
        pygame.display.update() # Updates the screen before pausing to ensure that the user is actually aware of the change that had happened to the ball
        pygame.time.delay(1000)
        newRound = False

    keyPressed = pygame.key.get_pressed()

    if (keyPressed[pygame.K_w] == True or keyPressed[pygame.K_UP] == True) and player.y >= 5:
        player.y += -5
    elif (keyPressed[pygame.K_s] == True or keyPressed[pygame.K_DOWN] == True) and player.y <= 470:
        player.y += 5


    if enemy.y <= 470 or enemy.y >= 5:
        if ballSpeedY > 0 and delayChange == False:
            enemy.y += enemySpeedY
        elif ballSpeedY < 0 and delayChange == False:
            enemy.y -= enemySpeedY
        
        if delayChange == True:
            delayChange = False
        elif ball.x >= 750:
            delayChange = True

    
    if enemy.top <= 0 or enemy.bottom >= SCREEN_HEIGHT:
        enemySpeedY *= -1

    # Movement for the ball
    ball.x += ballSpeedX
    ball.y += ballSpeedY

    # Changes the direction of the ball if it reaches the edge of the screen so that it stays on screen
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT: # Top and bottom of the screen
        ballSpeedY *= -1
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH: # Sides of the screen
        ballSpeedX *= -1
        if ball.left <= 0:
            enemyScore += 1
        elif ball.right >= SCREEN_WIDTH:
            playerScore += 1
        newRound = True
        player.y = 255
        enemy.y = 255

    if ball.colliderect(player) or ball.colliderect(enemy):
        ballSpeedX *= -1

    # Changes the ball so that it's back in the center, which should only happen when the ball reaches the left or right border of the screen
    if newRound == True:
        ball.x = 393
        ball.y = 300

    # This updates the screen with whatever has changed before repeating the loop.
    pygame.display.update()
    
    # Controlling the framerate like this allows for having a more consistent movement. If I just allowed the framerate to run wild, then the game runs much
    # faster than I would intend for it to
    frameRate.tick(60)

# Ends the process.
pygame.quit()