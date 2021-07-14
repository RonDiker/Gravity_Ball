import pygame

SCREEN_LENGTH = 1200
SCREEN_WIDTH = 800

BALL_LENGTH = 50
BALL_WIDTH = 50
BALL_MAX_Y = 728

# Colors
BLUE = (0, 62, 81)

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_WIDTH))

# Icon and title
pygame.display.set_caption("Gravity Ball")


# Player
class Player:
    def __init__(self):
        self.img = pygame.transform.scale(pygame.image.load('images/ball.png').convert_alpha(), (BALL_LENGTH, BALL_WIDTH))
        self.x = 600
        self.y = BALL_MAX_Y


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
        
        pygame.display.update()  # updates the display


if __name__ == "__main__":
    main()
