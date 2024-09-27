import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
COLUMNS = SCREEN_WIDTH // BLOCK_SIZE
ROWS = SCREEN_HEIGHT // BLOCK_SIZE
PARTICLE_RADIUS = 3  # Size of the particles for the explosion
PARTICLE_LIFETIME = 1000  # Lifetime of each particle in milliseconds

# Time intervals for block falling (in milliseconds)
NORMAL_SPEED = 500   # Normal speed: block moves down every 500ms
FAST_SPEED = 100     # Fast speed: block moves down every 100ms
MOVE_SPEED = 100     # Time interval for continuous left/right movement (in milliseconds)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (50, 50, 50)
PARTICLE_COLOR = (255, 255, 0)  # Yellow for particles

# Define the shapes of the tetris blocks
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
]

# Game screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Define a class for particles
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = PARTICLE_RADIUS
        self.color = color
        self.lifetime = PARTICLE_LIFETIME
        self.vx = random.uniform(-2, 2)  # Horizontal velocity
        self.vy = random.uniform(-4, -2)  # Initial vertical velocity (arc upwards)
        self.gravity = 0.1  # Simulated gravity

    def update(self, delta_time):
        self.vy += self.gravity  # Gravity pulls the particle down
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= delta_time

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def is_alive(self):
        return self.lifetime > 0 and self.y < SCREEN_HEIGHT

# Define a function to create new blocks
def new_block():
    shape = random.choice(SHAPES)
    block = {
        'shape': shape,
        'x': COLUMNS // 2 - len(shape[0]) // 2,
        'y': 0,
        'x_offset': 0.0,  # Horizontal offset for smooth movement
        'y_offset': 0.0   # Vertical offset for smooth movement
    }
    return block

# Rotate the block shape by 90 degrees
def rotate_block(block):
    rotated_shape = [list(row) for row in zip(*block['shape'][::-1])]
    rotated_block = {
        'shape': rotated_shape,
        'x': block['x'],
        'y': block['y'],
        'x_offset': block['x_offset'],
        'y_offset': block['y_offset']
    }
    return rotated_block

# Define a function to draw the grid and blocks
def draw_grid(blocks, current_block, particles):
    screen.fill(BLACK)

    # Draw all landed blocks
    for y in range(ROWS):
        for x in range(COLUMNS):
            if blocks[y][x]:
                pygame.draw.rect(
                    screen,
                    GREEN,  # Use green color for landed blocks
                    pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )

    # Draw the current block with smooth movement
    shape = current_block['shape']
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                # Add smooth horizontal and vertical interpolation using offsets
                draw_x = (current_block['x'] + x + current_block['x_offset']) * BLOCK_SIZE
                draw_y = (current_block['y'] + y + current_block['y_offset']) * BLOCK_SIZE
                pygame.draw.rect(
                    screen,
                    RED,  # Use red color for falling block
                    pygame.Rect(draw_x, draw_y, BLOCK_SIZE, BLOCK_SIZE)
                )

    # Draw particles
    for particle in particles:
        particle.draw(screen)

    pygame.display.update()

# Define a function to check for collision
def collision(block, blocks):
    for y, row in enumerate(block['shape']):
        for x, cell in enumerate(row):
            x_pos = block['x'] + x
            y_pos = block['y'] + y
            if cell and (x_pos < 0 or x_pos >= COLUMNS or y_pos >= ROWS or blocks[y_pos][x_pos]):
                return True
    return False

# Define a function to clear full lines and move blocks down
def clear_lines(blocks, particles):
    new_blocks = [row for row in blocks if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_blocks)

    if lines_cleared > 0:
        # Create particles for the disappearing blocks
        for y in range(ROWS - lines_cleared, ROWS):
            for x in range(COLUMNS):
                if blocks[y][x]:
                    for _ in range(5):  # Create multiple particles per block
                        particles.append(Particle(x * BLOCK_SIZE + BLOCK_SIZE // 2,
                                                  y * BLOCK_SIZE + BLOCK_SIZE // 2,
                                                  PARTICLE_COLOR))

    new_blocks = [[0] * COLUMNS for _ in range(lines_cleared)] + new_blocks
    return new_blocks, particles

# Define a function to check if blocks have reached the top, i.e., game over condition
def check_game_over(blocks):
    return any(blocks[0])  # Game over if there are any blocks in the top row

# Define the function to display "Game Over!" message and wait for a key press to restart
def game_over_screen():
    font_large = pygame.font.SysFont("comicsans", 50)
    font_small = pygame.font.SysFont("comicsans", 30)

    # Texts for game over and restart message
    game_over_text = font_large.render("Game Over!", True, WHITE)
    restart_text = font_small.render("Press any key to restart", True, WHITE)

    # Background for the messages
    text_background_width = max(game_over_text.get_width(), restart_text.get_width()) + 40
    text_background_height = game_over_text.get_height() + restart_text.get_height() + 40

    # Position for background and texts
    background_rect = pygame.Rect((SCREEN_WIDTH - text_background_width) // 2,
                                  (SCREEN_HEIGHT - text_background_height) // 2,
                                  text_background_width, text_background_height)

    pygame.draw.rect(screen, GRAY, background_rect)

    game_over_pos = ((SCREEN_WIDTH - game_over_text.get_width()) // 2,
                     (SCREEN_HEIGHT // 2) - 50)

    restart_pos = ((SCREEN_WIDTH - restart_text.get_width()) // 2,
                   (SCREEN_HEIGHT // 2) + 10)

    # Blit the texts on the screen
    screen.blit(game_over_text, game_over_pos)
    screen.blit(restart_text, restart_pos)

    pygame.display.update()

    # Wait for any key press to restart
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False  # Restart the game

# Define the main game loop
def tetris():
    blocks = [[0] * COLUMNS for _ in range(ROWS)]  # This grid holds the landed blocks
    particles = []  # List to hold all particles
    current_block = new_block()
    clock = pygame.time.Clock()
    running = True
    speed = NORMAL_SPEED  # Start with normal speed
    down_pressed = False  # Track if down arrow is pressed
    left_pressed = False  # Track if left arrow is pressed
    right_pressed = False  # Track if right arrow is pressed
    move_timer = 0         # Timer to control continuous left/right movement
    fall_timer = 0         # Timer to control vertical movement

    while running:
        delta_time = clock.tick(60)  # Run at 60 FPS for smooth animations
        move_timer += delta_time
        fall_timer += delta_time

        # Update and remove dead particles
        particles = [p for p in particles if p.is_alive()]
        for particle in particles:
            particle.update(delta_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_pressed = True
                if event.key == pygame.K_RIGHT:
                    right_pressed = True
                if event.key == pygame.K_UP:
                    rotated_block = rotate_block(current_block)
                    if not collision(rotated_block, blocks):
                        current_block = rotated_block  # Apply rotation if no collision
                if event.key == pygame.K_DOWN:
                    down_pressed = True  # Start moving faster
                if event.key == pygame.K_q:
                    running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    down_pressed = False  # Revert to normal speed when key is released
                if event.key == pygame.K_LEFT:
                    left_pressed = False  # Stop moving left when key is released
                if event.key == pygame.K_RIGHT:
                    right_pressed = False  # Stop moving right when key is released

        # Adjust the speed based on whether the down arrow is being held
        if down_pressed:
            speed = FAST_SPEED  # Faster falling when the down arrow is pressed
        else:
            speed = NORMAL_SPEED  # Normal speed when the down arrow is released

        # Continuous movement for left or right
        if move_timer >= MOVE_SPEED:
            if left_pressed:
                current_block['x'] -= 1
                if collision(current_block, blocks):
                    current_block['x'] += 1
            if right_pressed:
                current_block['x'] += 1
                if collision(current_block, blocks):
                    current_block['x'] -= 1
            move_timer = 0  # Reset timer for the next move

        # Vertical movement controlled by fall_timer
        if fall_timer >= speed:
            current_block['y'] += 1
            if collision(current_block, blocks):
                current_block['y'] -= 1
                for y, row in enumerate(current_block['shape']):
                    for x, cell in enumerate(row):
                        if cell:
                            blocks[current_block['y'] + y][current_block['x'] + x] = 1  # Mark block as landed
                blocks, particles = clear_lines(blocks, particles)  # Clear full lines and create particles

                # Check for game over
                if check_game_over(blocks):
                    draw_grid(blocks, current_block, particles)
                    game_over_screen()  # Display game over message
                    tetris()  # Restart the game after any key press

                current_block = new_block()
            fall_timer = 0  # Reset fall timer after moving down

        draw_grid(blocks, current_block, particles)

    pygame.quit()

# Run the game
tetris()
