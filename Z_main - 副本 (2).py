# Imports
import pygame
import sys
import os

# Game initialization
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600 # Screen size where the game is displayed

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Background original size
BACKGROUND_ORIGINAL_WIDTH = 272
BACKGROUND_ORIGINAL_HEIGHT = 160

# Background target scaled size to cover 800x600 while maintaining aspect ratio
# Scale factor = max(800/272, 600/160) = max(2.94, 3.75) = 3.75
BACKGROUND_SCALED_WIDTH = int(BACKGROUND_ORIGINAL_WIDTH * 3.75) # Should be 1020
BACKGROUND_SCALED_HEIGHT = int(BACKGROUND_ORIGINAL_HEIGHT * 3.75) # Should be 600

# Define background image paths and their visual order (from furthest to nearest)
# Ensure 'layer' folder is in the same directory as the script
# Using the corrected filename 'montain'
BACKGROUND_LAYER_PATHS = [
    os.path.join('layer', 'parallax-mountain-bg.png'),             # Layer 0: Sky (Furthest)
    os.path.join('layer', 'parallax-mountain-montain-far.png'), # Layer 1: Far Mountains
    os.path.join('layer', 'parallax-mountain-mountains.png'),    # Layer 2: Closer Mountains
    os.path.join('layer', 'parallax-mountain-trees.png'),        # Layer 3: Middle Trees
    os.path.join('layer', 'parallax-mountain-foreground-trees.png') # Layer 4: Foreground Trees/Ground (Nearest)
]

# List to hold loaded and scaled background image Surfaces
background_layers = []

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        """ Initialize player """
        super().__init__()

        # Attempt to load player image
        try:
            # Assume player image is 'girl_sprite.png' in the same directory as the script
            self.image = pygame.image.load("girl_sprite.png").convert_alpha()
            # Adjust rect based on image size
            self.rect = self.image.get_rect()
        except pygame.error:
             # Fallback to a simple red square if image loading fails
             print("Warning: Player image 'girl_sprite.png' not found. Using a red square placeholder.")
             self.image = pygame.Surface([40, 50])
             self.image.fill(RED)
             self.rect = self.image.get_rect()

        # Player movement variables
        self.change_x = 0 # Horizontal velocity
        self.change_y = 0 # Vertical velocity

        # Player state
        self.on_ground = False # Flag to check if player is on the ground

    def update(self):
        """ Update player position and state """
        # Apply gravity
        self.gravity()

        # Apply horizontal movement
        self.rect.x += self.change_x

        # --- Horizontal collision handling would go here ---

        # Apply vertical movement
        self.rect.y += self.change_y

        # --- Vertical collision handling (simple ground) ---
        # This is a simplification; proper collision needs actual platform/ground objects
        # The ground level should align with the visual ground in the foreground layer.
        # Assuming the bottom of the foreground layer is the ground
        ground_level = SCREEN_HEIGHT # Simplified: bottom of screen is ground for now
        # Or if foreground is positioned at y_foreground (calculated in draw),
        # ground_level = y_foreground + foreground_height - small_offset

        # For now, let's use a fixed level relative to screen bottom
        simulated_ground_y = SCREEN_HEIGHT - 50 # Example level for placeholder ground logic

        if self.rect.bottom >= simulated_ground_y:
             self.rect.bottom = simulated_ground_y
             self.change_y = 0 # Stop falling
             self.on_ground = True # Player is on the ground
        else:
             # If player is above the simulated ground, they are not on the ground
             if self.rect.bottom < simulated_ground_y:
                 self.on_ground = False


    def gravity(self):
        """ Apply gravity (increase vertical speed) """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35 # Gravity acceleration

    # Player movement control methods
    def go_left(self):
        """ Move player left """
        self.change_x = -5

    def go_right(self):
        """ Move player right """
        self.change_x = 5

    def stop(self):
        """ Stop horizontal movement """
        # This method is called, but the actual stopping is done by setting change_x in the event loop
        pass


    def jump(self):
        """ Make the player jump """
        # Simple jump: only allow jumping if on the ground
        if self.on_ground:
            self.change_y = -10 # Apply upward velocity for jump
            # on_ground flag is set False in update if they leave the ground


# Main game function
def main():
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple Side Scroller with Layers")

    # --- Load and Scale background images ---
    for layer_path in BACKGROUND_LAYER_PATHS:
        try:
            # Load image
            img = pygame.image.load(layer_path)
            # Convert with alpha for transparency
            img = img.convert_alpha()

            # Scale image to target size
            img = pygame.transform.scale(img, (BACKGROUND_SCALED_WIDTH, BACKGROUND_SCALED_HEIGHT))

            background_layers.append(img)
        except pygame.error as e:
            print(f"Error loading or scaling background layer {layer_path}: {e}")
            # Append None or handle error as needed if a layer fails
            background_layers.append(None) # Append None so indices are consistent


    # Create player instance
    player = Player()

    # Create a sprite group to manage all active sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Set initial player position (slightly above the simulated ground level)
    # Adjust this based on where the foreground ground visually is after scaling and positioning
    simulated_ground_y = SCREEN_HEIGHT - 50 # Match the player update logic
    player.rect.x = 50
    player.rect.bottom = simulated_ground_y # Start player on the simulated ground


    # Game clock to control frame rate
    clock = pygame.time.Clock()

    # Main game loop flag
    running = True

    # Main game loop
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                elif event.key == pygame.K_RIGHT:
                    player.go_right()
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                     player.jump()

            # Key releases
            if event.type == pygame.KEYUP:
                # Stop horizontal movement if the released key matches the current direction
                if event.key == pygame.K_LEFT and player.change_x < 0:
                     player.change_x = 0
                elif event.key == pygame.K_RIGHT and player.change_x > 0:
                     player.change_x = 0

        # --- Update Game State ---
        # Call update method for all sprites in the group
        all_sprites.update()

        # --- Drawing ---
        # 1. Clear the screen with the background color
        screen.fill(BLACK)

        # 2. Draw background layers (positioned vertically)
        # These Y coordinates are example visual offsets and may need fine-tuning
        # based on how the layers fit together visually when scaled.
        # Layers are in background_layers list: [bg, far-mountain, mountains, trees, foreground-trees]

        # Layer 0: Sky (Top aligned)
        if len(background_layers) > 0 and background_layers[0] is not None:
             screen.blit(background_layers[0], (0, 0)) # Y=0

        # Layer 1: Far Mountains (Example Y)
        if len(background_layers) > 1 and background_layers[1] is not None:
             screen.blit(background_layers[1], (0, 50)) # Example Y. Adjust as needed.

        # Layer 2: Closer Mountains (Example Y)
        if len(background_layers) > 2 and background_layers[2] is not None:
             screen.blit(background_layers[2], (0, 150)) # Example Y. Adjust as needed.

        # Layer 3: Middle Trees (Example Y)
        if len(background_layers) > 3 and background_layers[3] is not None:
             screen.blit(background_layers[3], (0, 300)) # Example Y. Adjust as needed.

        # Layer 4: Foreground (Bottom aligned)
        if len(background_layers) > 4 and background_layers[4] is not None:
             foreground_img = background_layers[4]
             # Calculate Y position so its bottom is at SCREEN_HEIGHT
             y_foreground = SCREEN_HEIGHT - foreground_img.get_height() # SCREEN_HEIGHT (600) - Scaled Height (600) = 0
             # This places the top of the foreground at Y=0 and bottom at Y=600.
             # Based on your screenshot showing it at the bottom, this is likely the correct visual placement.
             screen.blit(foreground_img, (0, y_foreground))


        # 3. Draw player and any other sprites after backgrounds
        all_sprites.draw(screen)

        # --- Update Display ---
        # Display everything drawn to the screen
        pygame.display.flip() # Or pygame.display.update()

        # --- Control Frame Rate ---
        # Limit the game to 60 frames per second
        clock.tick(60)

    # Game loop ends, exit Pygame
    pygame.quit()
    sys.exit()

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()