import pygame
import random

# Initialize pygame
pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Screen size
width, height = 600, 600
screen = pygame.display.set_mode((width, height))

# Clock and speed
clock = pygame.time.Clock()
snake_speed = 10  # Reduced speed for better control
snake_block = 20

# Font style
font_style = pygame.font.SysFont("bahnschrift", 25)

# Function to display game messages
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])

def gameLoop():
    game_over = False
    game_close = False

    # Snake initial position (start away from edges)
    x1 = width / 4
    y1 = height / 4

    # Initial movement direction
    x1_change = 0
    y1_change = 0

    # Snake body
    snake_List = []
    Length_of_snake = 1

    # Food
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            screen.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

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
                elif event.key == pygame.K_q:
                    game_over = True  # Quit game when 'q' is pressed

        # Detect if snake hits the boundary
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        # Update snake position
        x1 += x1_change
        y1 += y1_change

        # Fill background
        screen.fill(black)

        # Draw food
        pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block])

        # Snake movement
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Detect if snake hits itself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Draw the snake
        for x in snake_List:
            pygame.draw.rect(screen, white, [x[0], x[1], snake_block, snake_block])

        # Check if snake eats food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        # Update the screen and control frame rate
        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
