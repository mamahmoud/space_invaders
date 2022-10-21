"""
Space game
"""
import sys
import random
import winsound
import pygame


WIDTH = 800
HEIGHT = 600
ENEMY_SPEED_X = 4
ENEMY_SPEED_Y = 20
PLAYER_SPEED = 10
BULLET_SPEED = 10
PLAYER_INIT_X = 370
PLAYER_INIT_Y = 500
ENEMY_MULTIPLIER = 3
N_BULLETS = 3
ALIENS = ["alien-1.png", "alien-2.png", "alien-3.png", "alien-4.png", "alien-5.png"]
INTIAL_ENEMY_POS_Y = list(range(10, 101, 10))


class Player:
    """
    Player class
    """

    def __init__(self, window_surface, player_img, x_axis, y_axis):
        """
        Init Method
        """
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.window_surface = window_surface
        self.player_img = player_img
        self.alive = True
        self.on_move_right = False
        self.on_move_left = False
        self.score = 0

    def move(self, right, left):
        """
        Move Method
        """
        if right and self.x_axis < 720:
            self.x_axis += PLAYER_SPEED
        elif left and self.x_axis > 20:
            self.x_axis -= PLAYER_SPEED

    def draw(self):
        """
        Draw Method
        """
        self.window_surface.blit(self.player_img, (self.x_axis, self.y_axis))

    def check_dead(self, enemy):
        """
        check if dead
        """
        if (abs(self.x_axis - enemy.x_axis) < 25) and (
            abs(self.y_axis - enemy.y_axis) < 25
        ):
            self.alive = False
        elif enemy.y_axis >= self.y_axis:
            self.alive = False

    def is_alive(self):
        """
        check if alive
        """
        return self.alive


class Enemy:
    """
    Enemy class
    """

    def __init__(self, window_surface, enemy_img):
        """
        Init Method
        """
        self.x_axis = random.randint(100, 700)
        self.y_axis = random.choice(INTIAL_ENEMY_POS_Y)
        self.window_surface = window_surface
        self.enemy_img = enemy_img
        self.dir = random.choice([-1, 1])

    def move(self):
        """
        Move Method
        """
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

    def check_dead(self, incoming_bullets, player):
        """
        check if dead
        """
        for incoming_bullet in incoming_bullets:
            if incoming_bullet.is_alive():
                if (abs(self.x_axis - incoming_bullet.x_axis) < 25) and (
                    abs(self.y_axis - incoming_bullet.y_axis) < 25
                ):

                    incoming_bullet.alive = False
                    player.score += 1
                    Bullet.max_bullets += 1
                    self.x_axis = random.randint(100, 700)
                    self.y_axis = random.choice(INTIAL_ENEMY_POS_Y) + player.score
                    winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
                    break

    def draw(self):
        """
        Draw Method
        """
        self.window_surface.blit(self.enemy_img, (self.x_axis, self.y_axis))


class Bullet:
    """
    Bullet class
    """

    max_bullets = N_BULLETS

    def __init__(self, window_surface, bullet_img, x_axis, y_axis):
        """
        Init Method
        """
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.window_surface = window_surface
        self.bullet_img = bullet_img
        self.alive = True
        Bullet.max_bullets -= 1

    def move(self):
        """
        Move Method
        """
        if self.y_axis >= 20:
            self.y_axis -= BULLET_SPEED
        else:
            self.alive = False
            Bullet.max_bullets += 1

    def draw(self):
        """
        Draw Method
        """
        self.window_surface.blit(self.bullet_img, (self.x_axis, self.y_axis))

    def is_alive(self):
        """
        check if alive
        """
        return self.alive


def print_score(window_surface, player, font):
    """
    print score
    """
    text_score = font.render(f"score is {player.score}", True, (255, 255, 255))
    window_surface.blit(text_score, (10, 10))


def print_game_over(window_surface, font):
    """
    print score
    """
    text_score = font.render("Game Over", True, (255, 255, 255))
    window_surface.blit(text_score, (285, 300))


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
    # player image
    player_image = pygame.image.load("space-invaders.png")
    # enemy_images
    enemy_images = [pygame.image.load(alien) for alien in ALIENS]
    # background image
    background_image = pygame.image.load("background.jpg")
    # bullets image
    bullet_image = pygame.image.load("bullet.png")
    # create player
    player_1 = Player(game_screen, player_image, PLAYER_INIT_X, PLAYER_INIT_Y)
    # create font for score
    score_font = pygame.font.Font("freesansbold.ttf", 32)
    # create font for game over
    game_over_font = pygame.font.Font("freesansbold.ttf", 40)
    # list of bullets
    bullets = []
    # create list of enemies enemies
    enemies = [
        Enemy(game_screen, enemy_images[random.randint(0, 4)])
        for _ in range(ENEMY_MULTIPLIER * 5)
    ]
    # create battle sounds.
    pygame.mixer.music.load("battle.wav")
    pygame.mixer.music.play(-1)
    # game loop
    while True:
        # background
        game_screen.blit(background_image, (0, 0))
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                # right
                if event.key == pygame.K_RIGHT and player_1.is_alive():
                    player_1.on_move_right = True
                    player_1.on_move_left = False
                # left
                elif event.key == pygame.K_LEFT and player_1.is_alive():
                    player_1.on_move_right = False
                    player_1.on_move_left = True

            elif event.type == pygame.KEYUP:
                if (
                    event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT
                ) and player_1.is_alive():
                    player_1.on_move_right = False
                    player_1.on_move_left = False
            # fire
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_a):
                if Bullet.max_bullets > 0:
                    bullets.append(
                        Bullet(
                            game_screen,
                            bullet_image,
                            player_1.x_axis + 24,
                            player_1.y_axis,
                        )
                    )
                    winsound.PlaySound("game-gun.wav", winsound.SND_ASYNC)

        # moving player
        if player_1.on_move_right:
            player_1.move(True, False)
        elif player_1.on_move_left:
            player_1.move(False, True)

        # moving bullets
        if len(bullets) > 0:
            for bullet in bullets:
                if bullet.is_alive():
                    bullet.move()
        # moving enemies
        for enemy in enemies:
            enemy.move()
        # draw a player
        if player_1.is_alive():
            player_1.draw()
        # draw enemy
        for enemy in enemies:
            enemy.draw()
        # draw bullets
        for bullet in bullets:
            if bullet.is_alive():
                bullet.draw()
        # check for collisions
        for enemy in enemies:
            enemy.check_dead(bullets, player_1)
            player_1.check_dead(enemy)

        # remove dead bullets
        n_bull = len(bullets)
        if n_bull > N_BULLETS:
            bullets = bullets[n_bull - N_BULLETS : n_bull]
        # Print score

        print_score(game_screen, player_1, score_font)
        if not player_1.is_alive():
            print_game_over(game_screen, game_over_font)
        # update animation
        pygame.display.update()
        clock.tick(60)
