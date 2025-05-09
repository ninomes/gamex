# background.py
import pygame
import settings
import os
import math

class BackgroundManager:
    def __init__(self):
        """ Initialize Background Manager """
        # List to store (image_surface, y_position) tuples for drawing
        # Y position is calculated based on which layer is the ground or example offsets
        self.positioned_layers = []
        self.load_layers() # Automatically load layers on initialization

    def load_layers(self):
        """ Load, scale, and calculate position for background layers """
        self.positioned_layers = [] # Clear previous layers

        # Iterate through background layer paths defined in settings
        for i, layer_path in enumerate(settings.BACKGROUND_LAYER_PATHS):
            layer_img = None # Initialize image variable
            y_pos = 0 # Default Y position

            try:
                # Load image
                img = pygame.image.load(layer_path)
                # Convert with alpha for transparency
                img = img.convert_alpha()

                # --- Scale based on layer index ---
                # Layers 3 and 4 are scaled differently for tiling
                if i in [3, 4]: # Layer 3 (Trees) and Layer 4 (Foreground)
                     img = pygame.transform.scale(img, (settings.TILED_LAYER_SCALED_WIDTH, settings.TILED_LAYER_SCALED_HEIGHT))
                else: # Other layers (0, 1, 2) - Scale to fill/exceed screen width/height
                     img = pygame.transform.scale(img, (settings.BACKGROUND_SCALED_WIDTH, settings.BACKGROUND_SCALED_HEIGHT))

                layer_img = img # Assign scaled image

            except pygame.error as e:
                print(f"Error loading or scaling background layer {layer_path}: {e}")
                # Append None so indices are consistent even if a layer fails to load
                self.positioned_layers.append((None, y_pos)) # Append None image with default Y
                continue # Skip positioning calculation if loading failed

            # --- Calculate Y position for drawing based on layer index and settings ---
            # Using example Ys and aligning the main ground layer (Layer 3)
            if i == 0: # Layer 0 (Sky)
                y_pos = settings.BG_Y # Which is 0
            elif i == 1: # Layer 1 (Far Mountains)
                y_pos = settings.FAR_MOUNTAIN_Y # Example Y
            elif i == 2: # Layer 2 (Closer Mountains)
                y_pos = settings.MOUNTAINS_Y # Example Y
            elif i == 3: # Layer 3 (Middle Trees - User identified as ground)
                # Calculate Y so its ground line (offset from its top) aligns with VISIBLE_GROUND_Y
                # Use the scaled height of this specific layer (TILED_LAYER_SCALED_HEIGHT)
                y_pos = settings.VISIBLE_GROUND_Y - settings.MIDDLE_TREES_GROUND_Y_OFFSET_SCALED
            elif i == 4: # Layer 4 (Foreground)
                # Position this layer visually below the main ground layer (Layer 3)
                # Use its specific example Y constant
                y_pos = settings.FOREGROUND_Y


            # Append the loaded image and its calculated Y position
            self.positioned_layers.append((layer_img, y_pos))


    def draw(self, surface):
        """ Draw background layers onto the given surface """
        if self.positioned_layers: # Check if any layers were loaded
            # Draw layers in the correct visual order (from furthest to nearest)
            # Indices: 0=bg, 1=far-mtn, 2=mtn, 3=trees (tiled), 4=foreground (tiled)

            # Draw layers 0, 1, 2 (scaled to 1020x600)
            for i in range(3): # Layers 0, 1, 2
                 if len(self.positioned_layers) > i and self.positioned_layers[i][0] is not None:
                      layer_img, y_pos = self.positioned_layers[i]
                      surface.blit(layer_img, (0, y_pos))

            # Draw Layer 3 (Middle Trees - Tiled Horizontally)
            if len(self.positioned_layers) > 3 and self.positioned_layers[3][0] is not None:
                 trees_img, y_pos = self.positioned_layers[3]
                 # Calculate how many times to tile horizontally
                 tile_width = trees_img.get_width() # Should be TILED_LAYER_SCALED_WIDTH (272)
                 num_tiles = math.ceil(settings.SCREEN_WIDTH / tile_width) # Ensure it covers screen width

                 # Tile horizontally at the calculated Y position
                 for j in range(num_tiles):
                      surface.blit(trees_img, (j * tile_width, y_pos))

                 # --- Optional: Tile Layer 3 vertically below the ground line ---
                 # This is an interpretation of "纵向 复制延伸" below the main ground level.
                 # If you only want a single horizontal strip, comment out this block.
                 try:
                     # Get the portion of the image *below* the ground line
                     # This portion starts at settings.MIDDLE_TREES_GROUND_Y_OFFSET_SCALED pixels from the top of the (272x600) image
                     # Its height is the total scaled height minus the offset to the ground line
                     # Ensure offset is not larger than height
                     if settings.MIDDLE_TREES_GROUND_Y_OFFSET_SCALED < trees_img.get_height():
                          height_below_ground_line = trees_img.get_height() - settings.MIDDLE_TREES_GROUND_Y_OFFSET_SCALED # 600 - 570 = 30 (example)
                     else:
                          height_below_ground_line = 0 # No portion below if offset is invalid or at/above height

                     if height_below_ground_line > 0:
                         # Define the rectangular area of the image below the ground line
                         portion_rect = (0, settings.MIDDLE_TREES_GROUND_Y_OFFSET_SCALED, tile_width, height_below_ground_line)
                         portion_below_ground = trees_img.subsurface(portion_rect)

                         vertical_tile_height = portion_below_ground.get_height()
                         # Start vertical tiling from the VISIBLE_GROUND_Y line downwards
                         start_y_for_vertical_tile = settings.VISIBLE_GROUND_Y

                         if vertical_tile_height > 0: # Avoid division by zero
                              # Calculate how many times to tile vertically down to SCREEN_HEIGHT
                              remaining_screen_height_below_ground = settings.SCREEN_HEIGHT - start_y_for_vertical_tile
                              if remaining_screen_height_below_ground > 0:
                                   # Add a buffer just in case
                                   num_vertical_tiles = math.ceil(remaining_screen_height_below_ground / vertical_tile_height)

                                   for k in range(num_vertical_tiles):
                                        # Tile horizontally for each vertical position
                                        current_vertical_y = start_y_for_vertical_tile + k * vertical_tile_height

                                        # Only draw if the tile is at least partially on screen
                                        # Check if the top of the tile is above the screen bottom
                                        if current_vertical_y < settings.SCREEN_HEIGHT:
                                            # Check if the bottom of the tile is below the screen top (0) - shouldn't happen if start_y is > 0
                                            if current_vertical_y + vertical_tile_height > 0:
                                                 for j in range(num_tiles): # Tile horizontally
                                                      surface.blit(portion_below_ground, (j * tile_width, current_vertical_y))

                 except pygame.error as e:
                      print(f"Error creating or tiling vertical portion of Layer 3: {e}")
                 except Exception as e:
                      print(f"An unexpected error occurred during Layer 3 vertical tiling: {e}")


            # Draw Layer 4 (Foreground) - Tiled Horizontally
            if len(self.positioned_layers) > 4 and self.positioned_layers[4][0] is not None:
                 foreground_img, y_pos = self.positioned_layers[4]
                 # Calculate how many times to tile horizontally
                 tile_width = foreground_img.get_width() # Should be TILED_LAYER_SCALED_WIDTH (272)
                 num_tiles = math.ceil(settings.SCREEN_WIDTH / tile_width) # Ensure it covers screen width

                 # Tile horizontally at the calculated Y position (settings.FOREGROUND_Y)
                 for j in range(num_tiles):
                      surface.blit(foreground_img, (j * tile_width, y_pos))
