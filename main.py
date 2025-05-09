# main.py
import pygame
import sys
import settings # Import settings module
import sprites # Import sprites module
import background # Import background module

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Simple Side Scroller with Layers")

# Create game objects
# Background Manager
bg_manager = background.BackgroundManager()
# Loading happens automatically in __init__

# Player sprite
player = sprites.Player()

# Create sprite group(s)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Set initial player position
# Position the player's bottom on the visible ground level
player.rect.x = settings.SCREEN_WIDTH // 4 # Start player near the left side
player.rect.bottom = settings.VISIBLE_GROUND_Y # Align player bottom to ground

# Game clock
clock = pygame.time.Clock()

# --- Main Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == settings.KEY_QUIT: # Check for window close button
            running = False

        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == settings.KEY_LEFT:
                player.go_left()
            elif event.key == settings.KEY_RIGHT:
                player.go_right()
            elif event.key == settings.KEY_JUMP:
                 player.jump()

        # Check for key releases
        if event.type == pygame.KEYUP:
            # Stop horizontal movement if the released key matches the current direction
            if event.key == settings.KEY_LEFT and player.change_x < 0:
                 player.stop()
            elif event.key == settings.KEY_RIGHT and player.change_x > 0:
                 player.stop()

    # --- Update Game State ---
    # Call update method for all sprites in the group
    all_sprites.update() # This updates player's position based on movement and gravity

    # --- Drawing ---
    # 1. Clear the screen
    screen.fill(settings.BLACK)

    # 2. Draw background layers using the BackgroundManager
    bg_manager.draw(screen)

    # 3. Draw player and any other sprites
    all_sprites.draw(screen)

    # --- Update Display ---
    # Display everything drawn to the screen
    pygame.display.flip() # Or pygame.display.update()

    # --- Control Frame Rate ---
    # Limit the game to the specified FPS
    clock.tick(settings.FPS)

# --- Game End ---
pygame.quit()
sys.exit()