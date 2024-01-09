import pygame

# COINS

class Coins(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(f"../Graphics/powerups/coin.png").convert_alpha()  # making a standard square surface
        self.image = pygame.transform.scale(self.image, (50,50))

        self.rect = self.image.get_rect(topleft=pos)
