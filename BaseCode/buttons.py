import pygame


class OptionPress:
    def __init__(self, image1, image2, position):
        # initialising
        self.__option_image = image1
        self.__position = position
        self.__image1 = image1
        self.__image2 = image2

        self.__button_rect = self.__option_image.get_rect(topleft = self.__position)
        self.pressed = False

    def __MousePress(self):
        __mouse_rect = pygame.mouse.get_pos()
        __option_hover_sound = pygame.mixer.Sound("../Audio/option_hover_music.mp3")
        # if hovering mouse over option, play sound and change image to yellow text image
        if self.__button_rect.collidepoint(__mouse_rect):
            __option_hover_sound.play()
            self.__option_image = self.__image2
            # if button clicked, set pressed to true
            if pygame.mouse.get_pressed()[0] == 1 and not self.pressed:
                self.pressed = True

        else:
            self.__option_image = self.__image1

    def draw(self, screen):  # draws button onto the screen in specified position
        self.__MousePress()
        screen.blit(self.__option_image, self.__position)


