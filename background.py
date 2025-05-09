# background.py
import pygame
import settings # Import settings module
import os

class BackgroundManager:
    def __init__(self):
        """ Initialize Background Manager """
        # List to store (image_surface, y_position) tuples for drawing
        self.positioned_layers = []
        self.load_layers() # Automatically load layers on initialization

    def load_layers(self):
        """ Load, scale, and position background layers """
        self.positioned_layers = [] # Clear previous layers

        # Iterate through background layer paths defined in settings
        for i, layer_path in enumerate(settings.BACKGROUND_LAYER_PATHS):
            layer_img = None # Initialize image variable

            try:
                # Load image
                img = pygame.image.load(layer_path)
                # Convert with alpha for transparency
                img = img.convert_alpha()

                # Scale image to target size
                img = pygame.transform.scale(img, (settings.BACKGROUND_SCALED_WIDTH, settings.BACKGROUND_SCALED_HEIGHT))
                layer_img = img # Assign scaled image

            except pygame.error as e:
                print(f"Error loading or scaling background layer {layer_path}: {e}")
                # Continue loop even if a layer fails, it will be None

            # --- Calculate Y position for drawing based on layer index and settings ---
            y_pos = 0 # Default Y position

            if layer_img is not None: # Only calculate Y if image loaded successfully
                if i == 0: # Layer 0 (Sky): Top aligned
                    y_pos = settings.BG_Y # Which is 0
                elif i == 4: # Layer 4 (Foreground): Position based on VISIBLE_GROUND_Y
                    # Calculate Y so the ground line within the scaled image aligns with VISIBLE_GROUND_Y
                    # y_pos = settings.VISIBLE_GROUND_Y - offset from top of image to ground line
                    y_pos = settings.VISIBLE_GROUND_Y - settings.FOREGROUND_GROUND_Y_OFFSET_SCALED
                else: # Intermediate layers (1, 2, 3): Use example Y offsets from settings
                    # Need to map index to the correct Y constant
                    if i == 1: # Far Mountains
                        y_pos = settings.FAR_MOUNTAIN_Y
                    elif i == 2: # Closer Mountains
                        y_pos = settings.MOUNTAINS_Y
                    elif i == 3: # Middle Trees
                        y_pos = settings.TREES_Y

            # Append the loaded image and its calculated Y position (or None and Y)
            self.positioned_layers.append((layer_img, y_pos))

        # Note: The list self.positioned_layers is already in drawing order (0 to 4)
        # as we iterated through BACKGROUND_LAYER_PATHS in that order.


    def draw(self, surface):
        """ Draw background layers onto the given surface """
        # Draw layers in the order they were loaded (0 to 4, back to front)
        for layer_img, y_pos in self.positioned_layers:
            if layer_img is not None: # Only draw if the image loaded successfully
                # Draw the layer at its calculated Y position (X is 0 for now)
                surface.blit(layer_img, (0, y_pos))

    # Optional: Method to get the ground Y for collision reference outside the player
    # def get_ground_y(self):
    #     return settings.VISIBLE_GROUND_Y