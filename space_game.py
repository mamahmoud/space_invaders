"""
Space game
"""
import sys
import random
from tkinter import Y
import pygame


WIDTH = 800
HEIGHT = 600
ENEMY_SPEED_X = 4
ENEMY_SPEED_Y = 20
PLAYER_SPEED = 10
BULLET_SPEED = 10
PLAYER_INIT_X = 370
PLAYER_INIT_Y = 500


class Player:
    def __init__(self, window_surface, player_img, x_axis, y_axis):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.window_surface = window_surface
        self.player_img = player_img
        self.alive = True

    def move(self, right, left):
        if right and self.x_axis < 720:
            self.x_axis += PLAYER_SPEED
        elif left and self.x_axis > 20:
            self.x_axis -= PLAYER_SPEED

    def draw(self):
        self.window_surface.blit(self.player_img, (self.x_axis, self.y_axis))

    def is_alive(self):
        return self.alive


class Enemy:
    def __init__(self, window_surface, enemy_img):
        self.x_axis = random.randint(100, 700)
        self.y_axis = 20
        self.window_surface = window_surface
        self.enemy_img = enemy_img
        self.alive = True
        self.dir = 1
        self.rect = self.enemy_img.get_rect()

    def move(self):
        if self.x_axis > 740:
            self.dir *= -1
            self.x_axis -= ENEMY_SPEED_X
            self.y_axis += ENEMY_SPEED_Y

        elif self.x_axis < 10:
            self.dir *= -1
            self.x_axis += ENEMY_SPEED_X
            self.y_axis += ENEMY_SPEED_Y
        elif self.y_axis > 500:
            pass
        else:
            self.x_axis += self.dir * ENEMY_SPEED_X

    def check_dead(self, bs):
        for bu in bs:
            if bu.is_alive():
                if (abs(self.x_axis - bu.x_axis) < 25) and (
                    abs(self.y_axis - bu.y_axis) < 25
                ):
                    self.alive = False
                    bu.alive = False
                    break

    def draw(self):
        self.window_surface.blit(self.enemy_img, (self.x_axis, self.y_axis))

    def is_alive(self):
        return self.alive


class Bullet:
    def __init__(self, window_surface, bullet_img, x_axis, y_axis):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.window_surface = window_surface
        self.bullet_img = bullet_img
        self.alive = True

    def move(self):
        if self.y_axis >= 20:
            self.y_axis -= BULLET_SPEED
        else:
            self.alive = False

    def draw(self):
        self.window_surface.blit(self.bullet_img, (self.x_axis, self.y_axis))

    def is_alive(self):
        return self.alive


if __name__ == "__main__":
    # initialize
    pygame.init()
    # create window
    game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # setting clock
    clock = pygame.time.Clock()
    # title
    pygame.display.set_caption("Space Game v2 by mohamed")
    # adding image icon
    game_icon = pygame.image.load("startup.png")
    player_image = pygame.image.load("space-invaders.png")
    enemy_image = pygame.image.load("alien.png")
    background_image = pygame.image.load("background.jpg")
    bullet_image = pygame.image.load("bullet.png")
    player_1 = Player(game_screen, player_image, PLAYER_INIT_X, PLAYER_INIT_Y)
    enemy_1 = Enemy(game_screen, enemy_image)
    bullets = []
    # game loop
    while True:
        # background
        game_screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                # right
                if event.key == pygame.K_RIGHT and player_1.is_alive():
                    player_1.move(True, False)
                # left
                elif event.key == pygame.K_LEFT and player_1.is_alive():
                    player_1.move(False, True)
            # fire
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_a):
                bullets.append(
                    Bullet(
                        game_screen, bullet_image, player_1.x_axis + 24, player_1.y_axis
                    )
                )
        # moving bullets
        if len(bullets) > 0:
            for bullet in bullets:
                if bullet.is_alive():
                    bullet.move()
        # moving enemy
        if enemy_1.is_alive():
            enemy_1.move()
            enemy_1.check_dead(bullets)
        # draw a player
        if player_1.is_alive():
            player_1.draw()
        # draw enemy
        if enemy_1.is_alive():
            enemy_1.draw()
        if len(bullets) > 0:
            for bullet in bullets:
                if bullet.is_alive():
                    bullet.draw()

        # update animation
        pygame.display.update()
        clock.tick(60)
