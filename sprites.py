# sprites.py
import pygame
import settings # Import settings module

class Player(pygame.sprite.Sprite):
    def __init__(self):
        """ Initialize player sprite """
        super().__init__()

        # Attempt to load player image from settings
        try:
            self.image = pygame.image.load(settings.PLAYER_IMAGE_PATH).convert_alpha()
            self.rect = self.image.get_rect()
        except pygame.error:
             # Fallback to a simple red square if image loading fails
             print(f"Warning: Player image '{settings.PLAYER_IMAGE_PATH}' not found. Using a red square placeholder.")
             self.image = pygame.Surface([40, 50])
             self.image.fill(settings.RED)
             self.rect = self.image.get_rect()

        # Player movement variables (velocity)
        self.change_x = 0
        self.change_y = 0

        # Player state
        self.on_ground = False # True if player is currently on the ground

    def update(self):
        """ Update player position and state each frame """
        # Apply gravity
        self.apply_gravity()

        # Apply vertical movement
        self.rect.y += self.change_y

        # --- Vertical collision with the ground ---
        # Check if player's bottom has reached or passed the visible ground level
        if self.rect.bottom >= settings.VISIBLE_GROUND_Y:
             self.rect.bottom = settings.VISIBLE_GROUND_Y # Snap player bottom to ground level
             self.change_y = 0 # Stop vertical movement
             self.on_ground = True # Player is on the ground

        # Apply horizontal movement
        self.rect.x += self.change_x

        # --- Horizontal collision handling would go here ---

        # Update on_ground state if player moves off the ground (and isn't falling due to jump)
        # Note: This is a simplified check. More robust logic involves checking platforms below.
        # If the player was on the ground but is now above it due to vertical movement (e.g. falling off edge)
        if self.on_ground and self.change_y == 0 and self.rect.bottom < settings.VISIBLE_GROUND_Y:
             self.on_ground = False


    def apply_gravity(self):
        """ Apply gravity to the player's vertical speed """
        if self.change_y == 0:
            self.change_y = 1 # Small initial fall speed
        else:
            self.change_y += settings.GRAVITY # Increase vertical speed by gravity constant

    # Player movement control methods
    def go_left(self):
        """ Set horizontal speed to move left """
        self.change_x = -settings.PLAYER_SPEED

    def go_right(self):
        """ Set horizontal speed to move right """
        self.change_x = settings.PLAYER_SPEED

    def stop(self):
        """ Stop horizontal movement (set speed to 0) """
        self.change_x = 0

    def jump(self):
        """ Make the player jump (apply upward velocity) """
        # Only allow jumping if the player is currently on the ground
        if self.on_ground:
            self.change_y = -settings.PLAYER_JUMP_POWER # Apply upward velocity
            self.on_ground = False # Player is now in the air