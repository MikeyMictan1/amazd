import pygame


# clear code inspired class
class Sword(pygame.sprite.Sprite):
    """
    Description:
        The class for the sword, that the character uses when attacking an enemy.

    Inherits:
        pygame.sprite.Group: Inherits from pygame sprite class to make sprite interactions and functions easier.

    Attributes:
        image (pygame.Surface): Image of the sword sprite
        rect (pygame.Rect): Rectangular area of the sword sprite in a certain location.
    """

    def __init__(self, character_direction: str, character_positions: list, groups: list):
        """
        Description:
            Initialises the sword sprite.

        Parameters:
            character_direction (str): The current direction the character is facing
            character_positions (list): The different locations to place the sword, depending on the way the character
            is facing
            groups (list):
        """
        super().__init__(groups)
        sword_sound = pygame.mixer.Sound("../Audio/sword_swing.mp3")
        sword_sound.play()
        sword_sound.set_volume(0.1)

        # graphic
        self.image = pygame.image.load(f'../Graphics/weapon/{character_direction}.png').convert_alpha()

        # placement in the direction the character is facing
        if character_direction == 'right':
            self.rect = self.image.get_rect(midleft=character_positions[0] + pygame.math.Vector2(0, 16))
        elif character_direction == 'left':
            self.rect = self.image.get_rect(midright=character_positions[1] + pygame.math.Vector2(0, 16))
        elif character_direction == 'down':
            self.rect = self.image.get_rect(midtop=character_positions[2] + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom=character_positions[3] + pygame.math.Vector2(-10, 0))
