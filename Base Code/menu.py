import pygame
from settings import *

class OptionPress(pygame.sprite.Sprite):
    def __init__(self, image1, image2, position):

        super().__init__()
        # initialising
        self.option_image = image1
        self.position = position
        self.image1 = image1
        self.image2 = image2

        self.button_rect = self.option_image.get_rect(topleft = self.position)
        self.pressed = False
        self.count = 0


    def MousePress(self):
        pos = pygame.mouse.get_pos()
        option_hover_sound = pygame.mixer.Sound("../Audio/option_hover_music.mp3") # terraria
        # if there is a mouse collision
        if self.button_rect.collidepoint(pos):  # change pos variable name bcz misleading
            option_hover_sound.play()
            self.option_image = self.image2

            if pygame.mouse.get_pressed()[0] == 1 and self.pressed == False:
                self.pressed = True

        else:
            self.option_image = self.image1
            self.count = 0


    def draw(self, screen):
        self.MousePress()
        screen.blit(self.option_image, self.position)