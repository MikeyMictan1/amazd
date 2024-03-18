import pygame


class Powerups(pygame.sprite.Sprite):
    """
    Description:
        Class for speed powerup sprites

    Inherits:
        pygame.sprite.Group: Inherits from pygame's sprite class to make sprite interactions and functions easier to
        handle.

    Attributes:
        __frame (float): the current frame for animating the powerup
        __powerup_frame_speed (float): The speed at which the animation for the powerup will play
        __num_of_images (int): The number of different images needed to animate the powerup
        __image1 (pygame.Surface): The first of 2 possible images the powerup can be
        __image2 (pygame.Surface): The second of 2 possible images the powerup can be
        rect (pygame.Rect): the rectangular area of the powerup on the screen
        image (pygame.Surface): The current image of the powerup
    """
    def __init__(self, pos: tuple, groups: list):
        """
        Description:
            Initialises the powerup class, with frame information, and animation images.

        Parameters:
            pos (tuple): The screen co-ordinates of where the powerup will be drawn
            groups (list): a list of pygame sprite groups that the class belongs to
        """
        super().__init__(groups)
        self.__frame = 0
        self.__powerup_frame_speed = 0.01
        self.__num_of_images = 2

        self.__image1 = pygame.image.load(
            f"../Graphics/powerups/speedpowerup1.png").convert_alpha()  # making a standard square surface
        self.__image1 = pygame.transform.scale(self.__image1, (50, 50))

        self.__image2 = pygame.image.load(f"../Graphics/powerups/speedpowerup2.png").convert_alpha()
        self.__image2 = pygame.transform.scale(self.__image2, (50, 50))
        self.image = self.__image1
        self.rect = self.__image1.get_rect(topleft=pos)

    def powerup_animation_speed(self):
        """
        Description:
            Animates the powerup image to flicker between 2 images every few seconds
        """
        self.__frame += self.__powerup_frame_speed  # fps for powerup animation

        if self.__frame >= self.__num_of_images:  # sets frame back to 0 if we ever reach 2
            self.__frame = 0

        if self.__frame < 1:  # load first image if in 0th frame
            self.image = self.__image1

        if self.__frame >= 1:  # load second image if in 1st frame
            self.image = self.__image2

    def update(self):
        """
        Description:
            Updates the powerups animation
        """
        self.powerup_animation_speed()


class HealthPot(pygame.sprite.Sprite):
    """
    Description:
        Class for health potion sprites

    Inherits:
        pygame.sprite.Group: Inherits from pygame's sprite class to make sprite interactions and functions easier to
        handle.

    Attributes:
        image (pygame.Surface): The image of the health potion
        rect (pygame.Rect):  the rectangular area of the health potion on the screen
    """
    def __init__(self, pos: tuple, groups: list):
        """
        Description:
            Initialises the health potion class, with the image of the health potion, and its rect at the objects
            specified position.

        Parameters:
            pos (tuple): The screen co-ordinates of where the health potion will be drawn
            groups (list): a list of pygame sprite groups that the class belongs to
        """
        super().__init__(groups)
        self.image = pygame.image.load(
            f"../Graphics/powerups/healthpot.png").convert_alpha()  # making a standard square surface
        self.image = pygame.transform.scale(self.image, (50, 70))

        self.rect = self.image.get_rect(topleft=pos)


class Coins(pygame.sprite.Sprite):
    """
    Description:
        Class for coin sprites

    Inherits:
        pygame.sprite.Group: Inherits from pygame's sprite class to make sprite interactions and functions easier to
        handle.

    Attributes:
        image (pygame.Surface): The image of the coin
        rect (pygame.Rect):  the rectangular area of the coin on the screen
    """
    def __init__(self, pos: tuple, groups: list):
        """
        Description:
            Initialises the coin class, with the image of the coin, and its rect at the objects specified position.

        Parameters:
            pos (tuple): The screen co-ordinates of where the coin will be drawn
            groups (list): a list of pygame sprite groups that the class belongs to
        """
        super().__init__(groups)
        self.image = pygame.image.load(
            f"../Graphics/powerups/coin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect(topleft=pos)


class Exit(pygame.sprite.Sprite):
    """
    Description:
        Class for exit sprites

    Inherits:
        pygame.sprite.Group: Inherits from pygame's sprite class to make sprite interactions and functions easier to
        handle.

    Attributes:
        image (pygame.Surface): The image of the exit
        rect (pygame.Rect):  the rectangular area of the exit portal on the screen
    """
    def __init__(self, pos: tuple, groups: list):
        """
        Description:
            Initialises the exit portal class, with the image of the exit portal, and its rect at the objects specified
            position.

        Parameters:
            pos (tuple): The screen co-ordinates of where the exit portal will be drawn
            groups (list): a list of pygame sprite groups that the class belongs to
        """
        super().__init__(groups)
        self.image = pygame.image.load(
            f"../Graphics/exit/portal.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))

        self.rect = self.image.get_rect(topleft=pos)
