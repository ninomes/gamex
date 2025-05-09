# settings.py
import os
import pygame # Import pygame to use constants like K_LEFT, etc.

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Background original size
BACKGROUND_ORIGINAL_WIDTH = 272
BACKGROUND_ORIGINAL_HEIGHT = 160

# Background target scaled size to cover SCREEN_WIDTH x SCREEN_HEIGHT
# Scale factor = max(SCREEN_WIDTH/BACKGROUND_ORIGINAL_WIDTH, SCREEN_HEIGHT/BACKGROUND_ORIGINAL_HEIGHT)
scale_factor_x = SCREEN_WIDTH / BACKGROUND_ORIGINAL_WIDTH
scale_factor_y = SCREEN_HEIGHT / BACKGROUND_ORIGINAL_HEIGHT
scale_factor = max(scale_factor_x, scale_factor_y)

BACKGROUND_SCALED_WIDTH = int(BACKGROUND_ORIGINAL_WIDTH * scale_factor) # Should be >= SCREEN_WIDTH
BACKGROUND_SCALED_HEIGHT = int(BACKGROUND_ORIGINAL_HEIGHT * scale_factor) # Should be >= SCREEN_HEIGHT (exactly 600 in this case)

# File paths
# Ensure 'layer' folder is in the same directory as the script
LAYER_FOLDER = 'layer'
PLAYER_IMAGE_PATH = 'girl_sprite.png' # Player image file in main game folder

# Background layer paths in drawing order (furthest to nearest)
BACKGROUND_LAYER_PATHS = [
    os.path.join(LAYER_FOLDER, 'parallax-mountain-bg.png'),             # Layer 0: Sky
    os.path.join(LAYER_FOLDER, 'parallax-mountain-montain-far.png'), # Layer 1: Far Mountains (Corrected name)
    os.path.join(LAYER_FOLDER, 'parallax-mountain-mountains.png'),    # Layer 2: Closer Mountains
    os.path.join(LAYER_FOLDER, 'parallax-mountain-trees.png'),        # Layer 3: Middle Trees
    os.path.join(LAYER_FOLDER, 'parallax-mountain-foreground-trees.png') # Layer 4: Foreground Trees/Ground
]

# Game mechanics constants
FPS = 60
GRAVITY = .35
PLAYER_SPEED = 5
PLAYER_JUMP_POWER = 10 # Initial upward velocity for jump

# --- Crucial Constant for Ground Alignment ---
# This is the Y coordinate on the screen where the ground visually appears
# and where the player will collide. You might need to adjust this value
# after seeing how the background layers stack.
VISIBLE_GROUND_Y = SCREEN_HEIGHT - 50 # Example: 50 pixels from the bottom of the screen

# --- Background Positioning Constants ---
# These define the Y offset from the TOP of the screen for each background layer (except foreground)
# These are EXAMPLE values based on visual stacking. Adjust as needed.
BG_Y = 0
FAR_MOUNTAIN_Y = 50
MOUNTAINS_Y = 150
TREES_Y = 300

# Offset from the TOP of the SCALED foreground image to where the ground line is.
# This needs to be estimated from the scaled image.
# If scaled height is 600 and ground is 50px from bottom, ground is at 600-50 = 550 from top.
FOREGROUND_GROUND_Y_OFFSET_SCALED = 550 # Example value based on assumption

# Keyboard mappings (using pygame constants)
KEY_LEFT = pygame.K_LEFT
KEY_RIGHT = pygame.K_RIGHT
KEY_JUMP = pygame.K_SPACE # Or pygame.K_UP
KEY_QUIT = pygame.QUIT