import pygame
from globalfunctions import *

class OptionPress:
    def __init__(self, image1, image2, position):
        # initialising
        self.option_image = image1
        self.position = position
        self.image1 = image1
        self.image2 = image2

        self.button_rect = self.option_image.get_rect(topleft = self.position)
        self.pressed = False

    def MousePress(self):
        pos = pygame.mouse.get_pos()
        option_hover_sound = pygame.mixer.Sound("../Audio/option_hover_music.mp3") # terraria
        # if hovering mouse over option, play sound and change image to yellow text image
        if self.button_rect.collidepoint(pos):
            option_hover_sound.play()
            self.option_image = self.image2
            # if button clicked, set pressed to true
            if pygame.mouse.get_pressed()[0] == 1 and not self.pressed:
                self.pressed = True

        else:
            self.option_image = self.image1

    def draw(self, screen):
        self.MousePress()
        screen.blit(self.option_image, self.position)
