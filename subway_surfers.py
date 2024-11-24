import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Subway Surfers 2D")

# Load assets
player_image = pygame.image.load(r"D:\72 projects of python\subway_surfers\runner.png")  # Replace with your player sprite
obstacle_image = pygame.image.load(r"D:\72 projects of python\subway_surfers\obstacle.png")  # Replace with an obstacle sprite
coin_image = pygame.image.load(r"D:\72 projects of python\subway_surfers\coin.png")  # Replace with a coin sprite
background_image = pygame.image.load(r"D:\72 projects of python\subway_surfers\background.png")  # Optional: scrolling background

# Scale assets
player_image = pygame.transform.scale(player_image, (50, 100))
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))
coin_image = pygame.transform.scale(coin_image, (30, 30))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Game variables
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
player_x, player_y = WIDTH // 2 - 25, HEIGHT - 150
player_width, player_height = player_image.get_width(), player_image.get_height()
lane_positions = [WIDTH // 4, WIDTH // 2, 3 * WIDTH // 4]
player_lane = 1  # Start in the middle lane
score = 0
game_over = False

# Obstacles and coins
obstacles = []
coins = []
obstacle_spawn_time = 0
coin_spawn_time = 0

# Background scrolling
bg_y1, bg_y2 = 0, -HEIGHT
scroll_speed = 5


def spawn_obstacle():
    """Spawns an obstacle in a random lane."""
    lane = random.choice(lane_positions)
    obstacles.append(pygame.Rect(lane - 25, -50, obstacle_image.get_width(), obstacle_image.get_height()))


def spawn_coin():
    """Spawns a coin in a random lane."""
    lane = random.choice(lane_positions)
    coins.append(pygame.Rect(lane - 15, -50, coin_image.get_width(), coin_image.get_height()))


def draw_game():
    """Draws all game elements."""
    # Draw background
    screen.blit(background_image, (0, bg_y1))
    screen.blit(background_image, (0, bg_y2))

    # Draw player
    screen.blit(player_image, (player_x, player_y))

    # Draw obstacles
    for obstacle in obstacles:
        screen.blit(obstacle_image, (obstacle.x, obstacle.y))

    # Draw coins
    for coin in coins:
        screen.blit(coin_image, (coin.x, coin.y))

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Game Over message
    if game_over:
        over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(over_text, (WIDTH // 4, HEIGHT // 2))


# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_lane > 0:
                player_lane -= 1
            if event.key == pygame.K_RIGHT and player_lane < 2:
                player_lane += 1
            if event.key == pygame.K_r and game_over:
                # Restart the game
                game_over = False
                player_lane = 1
                obstacles.clear()
                coins.clear()
                score = 0

    # Update player position
    player_x = lane_positions[player_lane] - player_width // 2

    # Scroll background
    bg_y1 += scroll_speed
    bg_y2 += scroll_speed
    if bg_y1 >= HEIGHT:
        bg_y1 = -HEIGHT
    if bg_y2 >= HEIGHT:
        bg_y2 = -HEIGHT

    # Spawn obstacles and coins
    obstacle_spawn_time += 1
    coin_spawn_time += 1

    if obstacle_spawn_time > 90:
        spawn_obstacle()
        obstacle_spawn_time = 0

    if coin_spawn_time > 120:
        spawn_coin()
        coin_spawn_time = 0

    # Move obstacles
    for obstacle in obstacles[:]:
        obstacle.y += scroll_speed
        if obstacle.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
            game_over = True
        if obstacle.y > HEIGHT:
            obstacles.remove(obstacle)

    # Move coins
    for coin in coins[:]:
        coin.y += scroll_speed
        if coin.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
            score += 10
            coins.remove(coin)
        if coin.y > HEIGHT:
            coins.remove(coin)

    # Draw everything
    draw_game()

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)
