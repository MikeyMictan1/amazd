import pygame
from globalfunctions import *

class GameCamera(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.character_movement_offset = pygame.math.Vector2()
        self.character_image_offset = (-75, -50)

    def draw_camera_offset(self, character):
        # getting the offset
        self.character_movement_offset.x = character.rect.centerx - (screen_width // 2)
        self.character_movement_offset.y = character.rect.centery - (screen_height // 2)

        for sprite in self.sprites():
            # we can add a vector to sprite.rect (an offset that effects where the sprite will be drawn)
            # draw the sprite image in the same place as the rectangle
            character_movement_offset_pos = sprite.rect.topleft - self.character_movement_offset

            if sprite == character:
                self.screen.blit(sprite.image, character_movement_offset_pos + self.character_image_offset)

            else:
                self.screen.blit(sprite.image, character_movement_offset_pos)

            if hasattr(sprite, "enemy_name"):
                sprite.enemy_character_state(character)

