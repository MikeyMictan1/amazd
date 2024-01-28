import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player,groups):
        super().__init__(groups)
        self.sprite_type = "weapon"
        direction = player.player_direction
        print(direction)
        sword_sound = pygame.mixer.Sound("../Audio/sword_swing.mp3")
        sword_sound.play()
        sword_sound.set_volume(0.1)

        # graphic
        self.image = pygame.Surface((40, 40))

        # graphic
        full_path = f'../Graphics/weapon/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()


        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0))