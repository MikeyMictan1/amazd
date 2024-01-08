import pygame
import random
import os

class Exit(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(f"../Graphics/exit/portal.png").convert_alpha()  # making a standard square surface
        self.image = pygame.transform.scale(self.image, (150,150))

        self.rect = self.image.get_rect(topleft=pos)
