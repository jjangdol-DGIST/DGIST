import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Define font
font = pygame.font.SysFont(None, 25)

# Define the snake and its initial position
snake_block = 10
snake_speed = 15
x1 = 300
y1 = 300
x1_change = 0       
y1_change = 0
snake_List = []
Length_of_snake = 1

# Define the food
foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

# Define the game loop
game_over = False
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change = -snake_block
                y1_change = 0
            elif event.key == pygame.K_RIGHT:
                x1_change = snake_block
                y1_change = 0
            elif event.key == pygame.K_UP:
                y1_change = -snake_block
                x1_change = 0
            elif event.key == pygame.K_DOWN:
                y1_change = snake_block
                x1_change = 0
    
    # Check for collision with wall
    if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
        game_over = True
    
    # Update snake position
    x1 += x1_change
    y1 += y1_change
    
    # Draw the snake and food on the screen
    screen.fill(black)
    pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block])
    snake_Head = []
    snake_Head.append(x1)
    snake_Head.append(y1)
    snake_List.append(snake_Head)
    if len(snake_List) > Length_of_snake:
        del snake_List[0]
    for x in snake_List[:-1]:
        if x == snake_Head:
            game_over = True
    for x in snake_List:
        pygame.draw.rect(screen, white, [x[0], x[1], snake_block, snake_block])
    
    # Update the score
    score = Length_of_snake - 1
    score_font = font.render("Score: " + str(score), True, red)
    screen.blit(score_font, [0, 0])
    
    # Update the display
    pygame.display.update()
    
    # Check if the snake has eaten the food
    if x1 == foodx and y1 == foody:
        foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0,
