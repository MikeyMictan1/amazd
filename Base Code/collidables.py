import pygame

class Powerups(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.frame = 0
        self.powerup_frame_speed = 0.01
        self.num_of_images = 2

        self.image1 = pygame.image.load(f"../Graphics/powerups/speedpowerup1.png").convert_alpha()  # making a standard square surface
        self.image1 = pygame.transform.scale(self.image1, (50,50))

        self.image2 = pygame.image.load(f"../Graphics/powerups/speedpowerup2.png").convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, (50,50))
        self.image = self.image1
        self.rect = self.image1.get_rect(topleft=pos)


    def powerup_animation_speed(self):
        self.frame += self.powerup_frame_speed  # fps for powerup animation

        if self.frame >= self.num_of_images:  # sets frame back to 0 if we ever reach 2
            self.frame = 0

        if self.frame < 1:  # load first image if in 0th frame
            self.image = self.image1

        if self.frame >= 1:  # load second image if in 1st frame
            self.image = self.image2


    def update(self):
        self.powerup_animation_speed()


class HealthPot(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(f"../Graphics/powerups/healthpot.png").convert_alpha()  # making a standard square surface
        self.image = pygame.transform.scale(self.image, (50,70))

        self.rect = self.image.get_rect(topleft=pos)


class Coins(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(f"../Graphics/powerups/coin.png").convert_alpha()  # making a standard square surface
        self.image = pygame.transform.scale(self.image, (50,50))

        self.rect = self.image.get_rect(topleft=pos)


class Exit(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(f"../Graphics/exit/portal.png").convert_alpha()  # making a standard square surface
        self.image = pygame.transform.scale(self.image, (150,150))

        self.rect = self.image.get_rect(topleft=pos)