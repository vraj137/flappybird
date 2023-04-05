import pygame
import random

pygame.init()

# Game window dimensions
screen_width = 288
screen_height = 512

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Game objects dimensions
player_width = 34
player_height = 24
pipe_width = 45

# Load game assets
background = pygame.image.load("assets/background.png")
player_image = pygame.image.load("assets/bluebird.png")
pipe_image = pygame.image.load("assets/pipe.png")
pass_sound = pygame.mixer.Sound("assets/point.mp3")
pass_swoosh = pygame.mixer.Sound("assets/flap.mp3")


# Set up the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird - By VB")

# Set up the game clock
clock = pygame.time.Clock()


# Game loop
def game_loop():
    # Player properties
    player_x = 50
    player_y = 200
    player_y_change = 0
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Pipe properties
    pipe_x = screen_width
    pipe_gap = 100
    pipe_height = random.randint(100, 300)
    pipe_passed = False
    pipe_top_rect = pygame.Rect(pipe_x, 0 - (pipe_height + pipe_gap), pipe_width, pipe_height)
    pipe_bottom_rect = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, screen_height - pipe_height - pipe_gap)

    # Score
    score = 0
    font = pygame.font.Font(None, 32)

    # Game loop flag
    game_over = False

    # Main game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass_swoosh.play()
                    player_y_change = -7   

        # Update pipe position
        pipe_x -= 3
        if pipe_x < -pipe_width:
            pipe_x = screen_width
            pipe_height = random.randint(100, 300)
            pipe_passed = False
            pipe_top_rect = pygame.Rect(pipe_x, 0 - (pipe_height + pipe_gap), pipe_width, pipe_height)
            pipe_bottom_rect = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, screen_height - pipe_height - pipe_gap)

        # Update player position
        player_y += player_y_change
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        if player_y < 0:
            player_y = 0
        elif player_y >= screen_height - player_height:
            game_over = True
        player_y_change += 0.5

        # Stop player at point of collision
        if (player_rect.colliderect(pipe_top_rect) or player_rect.colliderect(pipe_bottom_rect)) and player_rect.centerx in range(pipe_x, pipe_x + pipe_width):
            if player_rect.colliderect(pipe_top_rect):
                player_y = pipe_top_rect.bottom
            else: 
                player_y = pipe_bottom_rect.top - player_height
                game_over = True
                player_y_change = 0


        # Check for score
        if pipe_x + pipe_width < player_x:
            if not pipe_passed:
                score += 1
                pipe_passed = True
                pass_sound.play()

        # Draw game objects
        screen.blit(background, (0, 0))
        screen.blit(player_image, (player_x, player_y))
        screen.blit(pipe_image, (pipe_x, 0 - (pipe_height + pipe_gap)))
        screen.blit(pipe_image, (pipe_x, pipe_height + pipe_gap))
        score_text = font.render("Score: " + str(score), True, black)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.update()

        # Set the frame rate
        clock.tick(60)
    

# Start the game loop
game_loop()
