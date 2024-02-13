import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Runner")

# Load images
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (50, 50))
obstacle_img = pygame.image.load("obstacle.png")
obstacle_img = pygame.transform.scale(obstacle_img, (50, 50))
coin_img = pygame.image.load("coin.png")
coin_img = pygame.transform.scale(coin_img, (30, 30))

# Define player properties
player_x, player_y = WIDTH // 2 - player_img.get_width() // 2, HEIGHT - player_img.get_height() - 20
player_speed = 5

# Define obstacle properties
obstacle_speed = 5
obstacle_spawn_rate = 0.05  # Adjust the spawn rate of obstacles
obstacles = []

# Define coin properties
coin_spawn_rate = 0.1  # Adjust the spawn rate of coins
coins = []

# Define lives
lives = 3
font = pygame.font.SysFont(None, 36)

# Define coin counter
coins_collected = 0

# Function to create obstacles
def create_obstacle():
    x = random.randint(0, WIDTH - obstacle_img.get_width())
    y = -obstacle_img.get_height()
    obstacles.append([x, y])

# Function to create coins
def create_coin():
    x = random.randint(0, WIDTH - coin_img.get_width())
    y = -coin_img.get_height()
    coins.append([x, y])

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(30)  # Cap the frame rate

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Spawn obstacles
    if random.random() < obstacle_spawn_rate:
        create_obstacle()

    # Spawn coins
    if random.random() < coin_spawn_rate:
        create_coin()

    # Move obstacles
    for obstacle in obstacles:
        obstacle[1] += obstacle_speed

    # Move coins
    for coin in coins:
        coin[1] += obstacle_speed  # Coins move with the same speed as obstacles

    # Check for collisions between player and obstacles
    player_rect = pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_img.get_width(), obstacle_img.get_height())
        if player_rect.colliderect(obstacle_rect):
            obstacles.remove(obstacle)
            lives -= 1
            if lives == 0:
                running = False

    # Check for collisions between player and coins
    for coin in coins:
        coin_rect = pygame.Rect(coin[0], coin[1], coin_img.get_width(), coin_img.get_height())
        if player_rect.colliderect(coin_rect):
            coins.remove(coin)
            coins_collected += 1

    # Fill the background
    win.fill((255, 255, 255))

    # Draw the player
    win.blit(player_img, (player_x, player_y))

    # Draw the obstacles
    for obstacle in obstacles:
        win.blit(obstacle_img, (obstacle[0], obstacle[1]))

    # Draw the coins
    for coin in coins:
        win.blit(coin_img, (coin[0], coin[1]))

    # Display lives
    lives_text = font.render("Lives: " + str(lives), True, (0, 0, 0))
    win.blit(lives_text, (WIDTH - 10 - lives_text.get_width(), 10))

    # Display coins collected
    coins_text = font.render("Coins: " + str(coins_collected), True, (0, 0, 0))
    win.blit(coins_text, (10, 10))

    # Update the display
    pygame.display.flip()

# Game over screen
win.fill((255, 255, 255))
game_over_text = font.render("Game Over! Coins collected: " + str(coins_collected), True, (0, 0, 0))
win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
pygame.display.flip()

# Wait for a moment before quitting
pygame.time.delay(2000)
pygame.quit()
sys.exit()
