import pygame
import random
import math
from pygame import mixer

# Initialising PyGame
pygame.init()

# Creating the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Galaxy Invader")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
background = pygame.image.load("background.png")


def back_ground():
    screen.blit(background, (0, 0))


# Player Info
playerImage = pygame.image.load("spaceship.png")
playerX = 368
playerY = 480
player_changeX = 0


def player(x, y):
    screen.blit(playerImage, (x, y))


# Enemy Info
enemyImage = []
enemyX = []
enemyY = []
enemy_changeX = []
enemy_changeY = []
enemies = 4
for i in range(enemies + 1):
    enemyImage.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 200))
    enemy_changeX.append(1)
    enemy_changeY.append(20)


def enemy(x, y, enemy_num):
    screen.blit(enemyImage[enemy_num], (x, y))


# Bullet Info
bulletImage = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bullet_changeY = 1
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))


# Score
score = 0
text = pygame.font.Font('Gameplay.ttf', 20)
finish = pygame.font.Font('Gameplay.ttf', 100)


def score_display():
    print_score = text.render(f"Score - {score}", True, (255, 255, 255))
    screen.blit(print_score, (5, 5))


def game_over():
    global score
    game_over_display = finish.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_display, (85, 200))


# Check Collision
def is_collision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    if distance <= 25:
        return True


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    back_ground()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_changeX = -0.5
            if event.key == pygame.K_RIGHT:
                player_changeX = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    shoot = mixer.Sound('laser.wav')
                    shoot.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_changeX = 0
    playerX += player_changeX
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(enemies + 1):
        if enemyY[i] >= 440:
            game_over()
            break
        enemyX[i] += enemy_changeX[i]
        if enemyX[i] <= 0:
            enemy_changeX[i] = 0.4
            enemyY[i] += enemy_changeY[i]
        elif enemyX[i] >= 736:
            enemy_changeX[i] = -0.4
            enemyY[i] += enemy_changeY[i]

        if is_collision(bulletX, bulletY, enemyX[i], enemyY[i]):
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 200)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_changeY

    player(playerX, playerY)
    score_display()
    pygame.display.update()
