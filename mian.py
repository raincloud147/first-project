import pygame
import math
import random
from pygame import mixer

pygame.init()

# creates gam window
screen = pygame.display.set_mode((700, 651))

# background
background = pygame.image.load('space background.png')

# background sound
mixer.music.load('background.wav')
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# icon and text top left
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# gives us the play.png and gives it coordinates
playerImg = pygame.image.load('player.png')
playerX = 310
playerY = 587
playerX_change = 0

# creating different positions for each enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_Of_Enemies = 3

# makes multiple enemies .append allows values to be added to a list
for i in range(num_Of_Enemies):
    # puts enemy.png into main gives
    enemyImg.append(pygame.image.load('enemy.png'))
    # randomizes enemy spawn
    enemyX.append(random.randint(1, 630))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(30)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 587
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score
score_value = 0
# font color
white = (255, 255, 255)
black = (0, 0, 0)
font = pygame.font.Font('Boulder Dash 6128.ttf', 30)
textX = 10
textY = 10

# Game Over
over_Font = pygame.font.Font('Boulder Dash 6128.ttf', 80)


# displays score
def score(x, y):
    score = font.render("Score :" + str(score_value), True, white)
    screen.blit(score, (x, y))


def game_over_screen():
    over_Text = over_Font.render("Game Over", True, black)
    screen.blit(over_Text, (20, 300))


# loads player on to screen
def player(x, y):
    screen.blit(playerImg, (x, y))


# loads enemy on to screen
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# bullet shows up on screen
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 15, y))


# this clacs dis between bullet and enemy and returns true if enemy was hit
def isHit(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 50:
        return True
    else:
        return False


running = True
while running:

    # background fill
    screen.fill((0, 0, 0))

    # background image load & coordinates
    screen.blit(background, (0, 0))

    # checks for things happening in game
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # checks if a key is pressed
        if event.type == pygame.KEYDOWN:

            # pause music
            if event.key == pygame.K_s:
                pygame.mixer.music.pause()

            # play music
            if event.key == pygame.K_a:
                pygame.mixer.music.unpause()

            # ship movement left
            if event.key == pygame.K_LEFT:
                playerX_change = -5

            # ship movement right
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # checks if the key has been released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # ship bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 636:
        playerX = 636

    for i in range(num_Of_Enemies):

        # game over
        if enemyY[i] > 480:
            for j in range(num_Of_Enemies):
                enemyY[j] = 700
            game_over_screen()
            break

        # enemy bounds + movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 630:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = -2

            # hit enemy
        hit = isHit(enemyX[i], enemyY[i], bulletX, bulletY)
        if hit:
            # explosion sound
            explosion_Sound = mixer.Sound('explosion.wav')
            mixer.music.set_volume(0.1)
            explosion_Sound.play()

            # "reloads" bullet
            bulletY = 600
            bullet_state = "ready"
            # increase score
            score_value += 1
            # respawns enemy
            enemyX[i] = random.randint(0, 630)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 600
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    score(textX, textY)
    pygame.display.update()
