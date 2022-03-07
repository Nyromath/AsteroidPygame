import pygame
from sys import exit
import random

FPS = 60
PLAYER_SPEED = 5
ASTEROID_SPEED = 10
ASTEROID_DELAY = 30
BULLET_SPEED = 10

PLAYER_HIT = pygame.USEREVENT + 1

pygame.init()

#Initialize Window
WIDTH, HEIGHT = 480, 640
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#Importing images
PLAYER_IMAGE = pygame.image.load('Assets/player.png')
BACKGROUND = pygame.image.load('Assets/background.png')
ASTEROID_IMG = pygame.image.load('Assets/asteroid.png')
BULLET_IMG = pygame.image.load('Assets/bullet.png')
LIFE_IMG = pygame.image.load('Assets/heart.png')

#Importing SFX
BULLET_SOUND = pygame.mixer.Sound('Assets/laser_shoot.wav')
ASTEROID_HIT_SOUND = pygame.mixer.Sound('Assets/explosion.wav')
PLAYER_HIT_SOUND = pygame.mixer.Sound('Assets/explosion2.wav')

def draw_window(player, asteroids, bullets, lives):
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(PLAYER_IMAGE, (player.x, player.y)) #blit = Block Image Transfer
    for asteroid in asteroids:
        WIN.blit(ASTEROID_IMG, (asteroid.x, asteroid.y))
    for bullet in bullets:
        WIN.blit(BULLET_IMG, (bullet.x, bullet.y))
    for i in range(0, lives + 1):
        x_pos = WIDTH + (-40 * i)
        WIN.blit(LIFE_IMG, (x_pos, 10))
    pygame.display.update()

#Player Movement
def handle_player_movement(keys_pressed, player):
    if keys_pressed[pygame.K_a] and player.x - PLAYER_SPEED > 0:
        player.x -= PLAYER_SPEED
    if keys_pressed[pygame.K_d] and player.x + PLAYER_SPEED < 430:
        player.x += PLAYER_SPEED
    if keys_pressed[pygame.K_s] and player.y + PLAYER_SPEED < 540:
        player.y += PLAYER_SPEED
    if keys_pressed[pygame.K_w] and player.y - PLAYER_SPEED > 0:
        player.y -= PLAYER_SPEED

def handle_asteroid_movement(asteroids, player):
    for asteroid in asteroids:
        asteroid.y += ASTEROID_SPEED
        if asteroid.colliderect(player):
            asteroids.remove(asteroid)
            pygame.event.post(pygame.event.Event(PLAYER_HIT))
            PLAYER_HIT_SOUND.play()

        if asteroid.y > HEIGHT:
            asteroids.remove(asteroid)

def handle_bullet_movement(bullets, asteroids):
    for bullet in bullets:
        bullet.y -= BULLET_SPEED

        for asteroid in asteroids:
            if asteroid.colliderect(bullet):
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                ASTEROID_HIT_SOUND.play()

        if bullet.y < 0:
            bullets.remove(bullet)

def create_asteroid():
    #Get Random x position
    x_pos = random.randint(0, WIDTH)
    asteroid = pygame.Rect(x_pos, -50, 50, 50)
    return asteroid

#Main Function
def main():
    player = pygame.Rect(215, 480, 50, 50) #Rect = Define rectangle on screen. (x coord, y coord, width, height)
    asteroids = []
    asteroid_timer = 0
    bullets = []
    clock = pygame.time.Clock()
    lives = 3

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bullet = pygame.Rect(player.x, player.y, 10, 10)
                    bullets.append(bullet)
                    BULLET_SOUND.play()

            if event.type == PLAYER_HIT:
                lives -= 1

        if lives <= 0:
            break

        if asteroid_timer >= ASTEROID_DELAY:
            asteroids.append(create_asteroid())
            asteroid_timer = 0
        asteroid_timer += 1

        keys_pressed = pygame.key.get_pressed()
        handle_player_movement(keys_pressed, player)
        handle_asteroid_movement(asteroids, player)
        handle_bullet_movement(bullets, asteroids)
        draw_window(player, asteroids, bullets, lives)

        pygame.display.update()

main()