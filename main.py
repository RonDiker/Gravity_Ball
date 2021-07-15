import pygame
import math
import time
import random

SCREEN_LENGTH = 1200
SCREEN_WIDTH = 800

BALL_LENGTH = 50
BALL_WIDTH = 50
BALL_MAX_Y = 728

COIN_LENGTH = 75
COIN_WIDTH = 75

LINE_WIDTH = 3

GRAVITY = 9
FRICTION = 0.9

# Colors
BLUE = (0, 62, 81)
WHITE_GREY = (250, 250, 250)

# Initialize the pygame
pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, -16, 1, 512)

# Fonts
B_FONT = pygame.font.SysFont('Comic Sans MS', 45)

# Create the screen
screen = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_WIDTH))

# Icon and title
pygame.display.set_caption("Gravity Ball")
programIcon = pygame.image.load('images/ball.png')
pygame.display.set_icon(programIcon)


# Player
class Player:
    def __init__(self):
        self.img = pygame.transform.scale(
            pygame.image.load('images/ball.png').convert_alpha(), (BALL_LENGTH, BALL_WIDTH))
        self.x = 600
        self.y = BALL_MAX_Y
        self.is_ready = True
        self.mass = 1
        self.velX = 0
        self.velY = 0
        self.last = pygame.time.get_ticks()
        self.cool_down = 1000
        self.is_set_timer = False
        self.coins = 0

    def movement(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos_x = mouse_pos[0]
        mouse_pos_y = mouse_pos[1]
        hit_sound = pygame.mixer.Sound('sounds/select.ogg')
        hit_sound.set_volume(0.1)

        distance = math.sqrt((mouse_pos_x - self.x) ** 2 +
                             (self.y - mouse_pos_y) ** 2)  # Distance between the ball and the mouse

        if mouse_pos_x < self.x:
            distance = -distance

        # Draw a line from the ball to the mouse
        lineX_start = self.x + 25
        lineY_start = self.y + 25
        lineX_end = mouse_pos_x
        lineY_end = mouse_pos_y

        # Stop the line when hitting the ground
        if lineY_end >= BALL_MAX_Y + 25:
            lineY_end = BALL_MAX_Y + 25

        # When the ball is stopped and ready for the next move, draw a line
        if self.is_ready:
            pygame.draw.line(screen, WHITE_GREY, (lineX_start, lineY_start), (lineX_end, lineY_end), LINE_WIDTH)

        # Move the ball to the destination
        if pygame.mouse.get_pressed(3)[0] is True and self.is_ready is True:
            self.is_ready = False
            srcX = lineX_start
            srcY = lineY_start
            dstX = lineX_end
            dstY = lineY_end
            self.velX = (dstX - srcX) / 5
            self.velY = (srcY - dstY) / 5

        # While the ball is moving
        if self.is_ready is False:
            self.x += self.velX
            self.y -= self.velY

            # Lower the x speed
            if self.velX > 1:
                self.velX -= FRICTION * self.mass
            elif self.velX < -1:
                self.velX += FRICTION * self.mass
            elif 1 > self.velX > -1:
                self.velX = 0

            # If the ball touches the ground
            if self.y < BALL_MAX_Y:
                self.velY -= self.mass * GRAVITY
            if self.y > BALL_MAX_Y:
                hit_sound.play()
                self.velY = -self.velY - self.mass * GRAVITY
                self.y = BALL_MAX_Y

            # If the ball touches one of the x borders
            if self.x <= 20 or self.x >= 1150:  # Borders of the x board
                hit_sound.play()
                self.velX = -self.velX

            # Check if the ball stopped in the ground
            if self.y == BALL_MAX_Y and self.velX == 0 and self.velY < 1:
                if self.is_set_timer is False:
                    self.last = pygame.time.get_ticks()
                    self.cool_down = 1000  # 1 Second timer
                self.is_set_timer = True
                if self.is_set_timer is True:
                    now = pygame.time.get_ticks()
                    if now - self.last >= self.cool_down:
                        self.last = now
                        self.is_ready = True
                        self.is_set_timer = False
                        hit_sound.stop()

    def update_score(self):
        score_txt = B_FONT.render('Score is: ' + str(self.coins), False, WHITE_GREY)
        screen.blit(score_txt, (5, 5))


class Coin:
    def __init__(self):
        self.img = pygame.transform.scale(
            pygame.image.load('images/coin.png').convert_alpha(), (COIN_LENGTH, COIN_WIDTH))
        self.x = random.randrange(100, 1100)
        self.y = random.randrange(100, BALL_MAX_Y - 100)
        self.is_taken = False

    def coin_master(self, player):
        # Draw a box collider on the player sprite
        player_col = pygame.Rect(player.x, player.y, BALL_LENGTH, BALL_WIDTH)
        pygame.draw.rect(screen, [0, 0, 0, 255], player_col, 1)
        # Draw a box collider on the coin sprite
        coin_col = pygame.Rect(self.x, self.y, COIN_LENGTH, COIN_WIDTH)
        pygame.draw.rect(screen, [0, 0, 0, 255], coin_col, 1)

        if self.is_taken and player.is_ready:
            self.x = random.randrange(100, 1100)
            self.y = random.randrange(100, BALL_MAX_Y - 100)
            self.is_taken = False

        elif player_col.colliderect(coin_col):
            player.coins += 1
            self.is_taken = True
            self.x = -100

        screen.blit(self.img, (self.x, self.y))


def init_background():
    screen.fill(BLUE)  # Set the background color to blue
    ground = pygame.transform.scale(pygame.image.load('images/ground.png').convert_alpha(), (1200, 600))
    screen.blit(ground, (0, 200))  # Make the ground visible in the display


def main_menu():
    result = 2
    select_sound = pygame.mixer.Sound('sounds/got_coin.wav')
    select_sound.set_volume(0.1)

    main_menu_start_button = pygame.Rect(400, 200, 400, 75)
    main_menu_quit_button = pygame.Rect(400, 300, 400, 75)

    start_txt = B_FONT.render('Start', False, WHITE_GREY)
    quit_txt = B_FONT.render('Quit', False, WHITE_GREY)

    # Start button
    if main_menu_start_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, [70, 101, 99], main_menu_start_button)
        if pygame.mouse.get_pressed(3)[0]:
            select_sound.play()
            result = 1
    else:
        pygame.draw.rect(screen, [60, 91, 89], main_menu_start_button)

    if main_menu_quit_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, [70, 101, 99], main_menu_quit_button)
        if pygame.mouse.get_pressed(3)[0]:
            select_sound.play()
            result = 0
    else:
        pygame.draw.rect(screen, [60, 91, 89], main_menu_quit_button)

    screen.blit(start_txt, (550, 200))
    screen.blit(quit_txt, (555, 300))

    return result


def main():
    is_running = True
    is_menu = True
    player = Player()
    coin = Coin()

    # Game loop
    while is_running is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        # Basic initializing to the world
        init_background()  # Draw the background
        screen.blit(player.img, (player.x, player.y))  # Make the player visible in the display

        if is_menu:  # Main menu
            if main_menu() == 1:  # Start
                is_menu = False
                time.sleep(0.2)  # little delay before we start the game
            elif main_menu() == 2:  # None
                is_menu = True
            else:  # Quit
                is_running = False

        else:  # Game
            player.movement()  # Movement
            player.update_score()  # Update the score
            coin.coin_master(player)  # Coin

        pygame.display.update()  # updates the display


if __name__ == "__main__":
    main()
