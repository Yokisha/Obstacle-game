#Code by Yokisha Poudel 
#computer graphics project 5th semester
import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 700
screen_height = 512

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fruits in the Basket")

# Load images
background_image = pygame.image.load('sky.png')
apple_image = pygame.image.load('apple.png')
mango_image = pygame.image.load('mango.png')
peach_image = pygame.image.load('peach.png')
basket_image = pygame.image.load('basket.png')
stone_image = pygame.image.load('stone.png')

# Resize images
apple_image = pygame.transform.scale(apple_image, (40, 40))
mango_image = pygame.transform.scale(mango_image, (40, 40))
peach_image = pygame.transform.scale(peach_image, (40, 40))
basket_image = pygame.transform.scale(basket_image, (80, 80))
stone_image = pygame.transform.scale(stone_image, (40, 40))

# Basket properties
basket_width = 80
basket_height = 80
basket_x = (screen_width // 2) - (basket_width // 2)
basket_y = screen_height - basket_height
basket_speed = 8

# Fruit properties
fruit_width = 40
fruit_height = 40
fruit_types = [apple_image, mango_image, peach_image]
fruits = []

# Stone properties
stone_width = 40
stone_height = 40
stone_x = random.randint(0, screen_width - stone_width)
stone_y = -stone_height  # Start stone off-screen initially
stone_speed = 4

# Score
score = 0

# Font
font = pygame.font.Font(None, 36)

# Game over flag
game_over = False

# Clock
clock = pygame.time.Clock()

# Function to create new fruits
def create_fruit():
    fruit_type = random.choice(fruit_types)
    fruit_x = random.randint(0, screen_width - fruit_width)
    fruit_y = -fruit_height
    fruit_speed = random.randint(2, 5)
    fruits.append({'image': fruit_type, 'x': fruit_x, 'y': fruit_y, 'speed': fruit_speed})

# Function to create new stone
def create_stone():
    global stone_x, stone_y
    stone_x = random.randint(0, screen_width - stone_width)
    stone_y = -stone_height

# Function to reset game state
def reset_game():
    global score, fruits, game_over
    score = 0
    fruits = []
    game_over = False
    create_stone()

# Initial stone spawn
create_stone()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                restart_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50)
                if restart_button_rect.collidepoint(mouse_x, mouse_y):
                    reset_game()

    if not game_over:
        # Basket movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < screen_width - basket_width:
            basket_x += basket_speed

        # Create new fruits
        if len(fruits) < 3:
            create_fruit()

        # Move fruits
        for fruit in fruits:
            fruit['y'] += fruit['speed']
            if fruit['y'] > screen_height:
                fruits.remove(fruit)
                continue

            # Collision detection for fruits
            if (basket_x < fruit['x'] < basket_x + basket_width or basket_x < fruit['x'] + fruit_width < basket_x + basket_width) and (
                    basket_y < fruit['y'] < basket_y + basket_height or basket_y < fruit['y'] + fruit_height < basket_y + basket_height):
                score += 1
                fruits.remove(fruit)

        # Stone movement
        stone_y += stone_speed
        if stone_y > screen_height:
            create_stone()

        # Collision detection for stone
        if (basket_x < stone_x < basket_x + basket_width or basket_x < stone_x + stone_width < basket_x + basket_width) and (
                basket_y < stone_y < basket_y + basket_height or basket_y < stone_y + stone_height < basket_y + basket_height):
            game_over = True

    # Drawing
    screen.blit(background_image, (0, 0))
    for fruit in fruits:
        screen.blit(fruit['image'], (fruit['x'], fruit['y']))
    screen.blit(basket_image, (basket_x, basket_y))
    screen.blit(stone_image, (stone_x, stone_y))

    # Display score
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    # Display game over message and restart button
    if game_over:
        game_over_text = font.render("Game Over", True, white)
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(game_over_text, game_over_rect)

        restart_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50)
        pygame.draw.rect(screen, red, restart_button_rect)
        restart_text = font.render("Restart", True, white)
        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
        screen.blit(restart_text, restart_text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


#SOURCE: CODE NUST (https://www.youtube.com/watch?v=qVVIFy_36S8)
