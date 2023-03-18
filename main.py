import pygame
import random
import math
from pygame import mixer

# init
pygame.init()

# set screen
right_boundary = 800
lower_boundary = 600
screen = pygame.display.set_mode((right_boundary, lower_boundary))

# title and logo
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerChange = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyChangeX = []
enemyChangeY = []
enemyNum =6

for i in range(enemyNum):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, right_boundary - 64))
    enemyY.append(random.randint(50, 150))
    enemyChangeX.append(0.75)
    enemyChangeY.append(40)

# bullett
bulletImg = pygame.image.load('bullet.png')
bulletX = random.randint(0, right_boundary)
bulletY = 480
bulletChangeX = 0
bulletChangeY = 1.3
bulletState = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# functions
def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 150))


def score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    return False


running = True
while running:
    screen.fill((128, 128, 128))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerChange = -0.3
            if event.key == pygame.K_RIGHT:
                playerChange = 0.3
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerChange = 0

    # checking boundaries
    playerX += playerChange
    if playerX <= 0:
        playerX = 0
    elif playerX >= right_boundary - 64:
        playerX = right_boundary - 64

    for i in range(enemyNum):
        if enemyY[i] > 440:
            for j in range(enemyNum):
                enemyY[j] = 2000
            game_over()
            break
        enemyX[i] += enemyChangeX[i]
        if enemyX[i] <= 0:
            enemyChangeX[i] = -enemyChangeX[i]
            enemyY[i] += enemyChangeY[i]
        elif enemyX[i] >= right_boundary - 64:
            enemyChangeX[i] = -enemyChangeX[i]
            enemyY[i] += enemyChangeY[i]
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bulletState = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, right_boundary - 64)
            enemyY[i] = random.randint(50, 150)
            print(score)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"
    if bulletState == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletChangeY


    player(playerX, playerY)
    score(scoreX, scoreY)

    pygame.display.update()
