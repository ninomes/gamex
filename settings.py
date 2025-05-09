# settings.py
import os
import pygame

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

# Scale factor based on height to ensure height matches SCREEN_HEIGHT
scale_factor_y = SCREEN_HEIGHT / BACKGROUND_ORIGINAL_HEIGHT # 600 / 160 = 3.75

# Target scaled dimensions for most layers (width fills/exceeds SCREEN_WIDTH, height matches SCREEN_HEIGHT)
BACKGROUND_SCALED_WIDTH = int(BACKGROUND_ORIGINAL_WIDTH * scale_factor_y) # 272 * 3.75 = 1020
BACKGROUND_SCALED_HEIGHT = int(BACKGROUND_ORIGINAL_HEIGHT * scale_factor_y) # 160 * 3.75 = 600

# Target scaled dimensions for Layers 3 and 4 (keep original width, scale height to SCREEN_HEIGHT)
TILED_LAYER_SCALED_WIDTH = BACKGROUND_ORIGINAL_WIDTH # 272
TILED_LAYER_SCALED_HEIGHT = SCREEN_HEIGHT # 600


# File paths
LAYER_FOLDER = 'layer'
PLAYER_IMAGE_PATH = 'girl_sprite.png'

# Background layer paths in drawing order (furthest to nearest)
BACKGROUND_LAYER_PATHS = [
    os.path.join(LAYER_FOLDER, 'parallax-mountain-bg.png'),             # Layer 0: Sky
    os.path.join(LAYER_FOLDER, 'parallax-mountain-montain-far.png'), # Layer 1: Far Mountains
    os.path.join(LAYER_FOLDER, 'parallax-mountain-mountains.png'),    # Layer 2: Closer Mountains
    os.path.join(LAYER_FOLDER, 'parallax-mountain-trees.png'),        # Layer 3: Middle Trees (User identified as ground, will be tiled)
    os.path.join(LAYER_FOLDER, 'parallax-mountain-foreground-trees.png') # Layer 4: Foreground (Will be tiled)
]

# Game mechanics constants
FPS = 60
GRAVITY = .35
PLAYER_SPEED = 5
PLAYER_JUMP_POWER = 10

# --- Crucial Constant for Ground Alignment ---
# This is the Y coordinate on the screen where the player visually stands
# and where the ground in the main ground layer (Layer 3) should align.
VISIBLE_GROUND_Y = SCREEN_HEIGHT - 50 # Example value: 600 - 50 = 550

# --- Background Positioning Constants ---
# These define the Y offset from the TOP of the screen for layers 0-2 and 4.
BG_Y = 0 # Layer 0 Y
FAR_MOUNTAIN_Y = 50 # Layer 1 Example Y
MOUNTAINS_Y = 150 # Layer 2 Example Y

# Offset from the TOP of the SCALED Layer 3 (Middle Trees) image (scaled to 272x600) to its ground line.
MIDDLE_TREES_GROUND_Y_OFFSET_SCALED = 570 # Example value (from previous turn)

# Y position for Layer 4 (Foreground) - Position it visually below the main ground layer (Layer 3)
FOREGROUND_Y = VISIBLE_GROUND_Y + 20 # Example: 20 pixels below the visible ground line (550 + 20 = 570)


# Keyboard mappings
KEY_LEFT = pygame.K_LEFT
KEY_RIGHT = pygame.K_RIGHT
KEY_JUMP = pygame.K_SPACE # Or pygame.K_UP
KEY_QUIT = pygame.QUIT
