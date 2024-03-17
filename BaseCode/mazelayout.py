import pygame
import random
import os


class WallVisible(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(
            f"../Graphics/wall/crackedbrick.png").convert_alpha()  # making a visible wall surface
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(topleft=pos)


class WallHidden(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(
            f"../Graphics/wall/crackedbrickhidden.png").convert_alpha()  # making a hidden wall surface
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(topleft=pos)


class Floor(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.images = os.listdir("../Graphics/floor")
        self.image = pygame.image.load(
            f"../Graphics/floor/{random.choice(self.images)}").convert_alpha()  # making a floor surface
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(topleft=pos)
