import pygame

class Sword(pygame.sprite.Sprite):
    def __init__(self, character_direction, character_positions, groups):
        super().__init__(groups)
        sword_sound = pygame.mixer.Sound("../Audio/sword_swing.mp3")
        sword_sound.play()
        sword_sound.set_volume(0.1)

        # graphic
        self.image = pygame.image.load(f'../Graphics/weapon/{character_direction}.png').convert_alpha()

        # placement
        if character_direction == 'right':
            self.rect = self.image.get_rect(midleft=character_positions[0] + pygame.math.Vector2(0, 16))
        elif character_direction == 'left':
            self.rect = self.image.get_rect(midright=character_positions[1] + pygame.math.Vector2(0, 16))
        elif character_direction == 'down':
            self.rect = self.image.get_rect(midtop=character_positions[2] + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom=character_positions[3] + pygame.math.Vector2(-10, 0))

