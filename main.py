import pygame
import math

SCREEN_LENGTH = 1200
SCREEN_WIDTH = 800

BALL_LENGTH = 50
BALL_WIDTH = 50
BALL_MAX_Y = 728

LINE_WIDTH = 3

GRAVITY = 9
FRICTION = 0.9

# Colors
BLUE = (0, 62, 81)
WHITE_GREY = (250, 250, 250)

# Initialize the pygame
pygame.init()
pygame.mixer.pre_init(44100, -16, 1, 512)

# Create the screen
screen = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_WIDTH))

# Icon and title
pygame.display.set_caption("Gravity Ball")


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


def init_background():
    screen.fill(BLUE)  # Set the background color to blue
    ground = pygame.transform.scale(pygame.image.load('images/ground.png').convert_alpha(), (1200, 600))
    screen.blit(ground, (0, 200))  # Make the ground visible in the display


def main():
    is_running = True
    player = Player()

    # Game loop
    while is_running is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        # Basic initializing to the world
        init_background()  # Draw the background
        screen.blit(player.img, (player.x, player.y))  # Make the player visible in the display

        # Movement
        player.movement()

        pygame.display.update()  # updates the display


if __name__ == "__main__":
    main()
