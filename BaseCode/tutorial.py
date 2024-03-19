import pygame

import globalfunctions as gf
from mazelevel import MazeLevel


class TutorialLevel(MazeLevel):
    """
    Description:
        Class that handles the tutorial levels for the game.

    Inherits:
        MazeLevel: Inherits maze levels, are the tutorial levels just add specific cases the level class.

    Attributes:
        __screen (pygame.Surface): The screen for which the tutorial HUD's are drawn onto
        __coin_txt (pygame.font.Render): Text drawn onto the screen that explains coins
        __stamina_txt (pygame.font.Render): Text drawn onto the screen that explains stamina
        __tip_txt_1 (pygame.font.Render): Text drawn onto the screen that explains points
        __tip_txt_2 (pygame.font.Render): Text drawn onto the screen that explains points
        __tip_txt_3 (pygame.font.Render): Text drawn onto the screen that explains controls menu

        __health_txt (pygame.font.Render): Text drawn onto the screen that explains the health bar
        __objective_txt (pygame.font.Render): Text drawn onto the screen that explains the objective of the game
        __death_txt (pygame.font.Render): Text drawn onto the screen that explains how the character can die
        __coin_image (pygame.Surface): Image of the coin to be drawn on the screen
    """

    def __init__(self, maze_lst: list):
        """
        Description:
            Initialisation function for the tutorial level class

        Parameters:
            maze_lst (list): The depth-first maze as a list
        """
        super().__init__(maze_lst)
        self.level_type = "tutorial"
        # --- TUTORIAL GRAPHICS SETUP ---
        self.__screen = pygame.display.set_mode((gf.screen_width, gf.screen_height))
        self.__coin_txt = gf.tutorial_font.render("Coin (pickup for 20 points)", 1, gf.white)
        self.__stamina_txt = gf.tutorial_font.render("Stamina bar (sprint)", 1, gf.white)
        self.__tip_txt_1 = gf.tutorial_font.render("Points (start at 500, they go down as time", 1, gf.white)
        self.__tip_txt_2 = gf.tutorial_font.render("passes, coins and enemy hits increase points)", 1, gf.white)
        self.__tip_txt_3 = gf.tutorial_font.render("Press 'C' to see all controls, press again to close menu", 1,
                                                   gf.white)
        self.__health_txt = gf.tutorial_font.render("Health Bar (Enemies can attack to lower it)", 1, gf.white)
        self.__objective_txt = gf.tutorial_font.render(
            "REACH THE PORTAL AT THE END OF THE MAZE WITH AS MANY POINTS AS POSSIBLE!", 1, gf.white)
        self.__death_txt = gf.tutorial_font.render(
            "RUNNING OUT OF HEARTS ENDS THE GAME", 1, gf.white)

        self.__coin_image = pygame.image.load(f"../Graphics/powerups/coin.png").convert_alpha()
        self.__coin_image = pygame.transform.scale(self.__coin_image, (70, 70))

    def tutorial_hud(self):
        """
        Description:
            Adds extra elements to the level HUD, in order to explain certain aspects to a new player.
            Runs in the first tutorial level.
        """
        # --- GRAPHICS FOR THE FIRST TUTORIAL LEVEL ---
        # images
        self.__screen.blit(self.__coin_image,
                           (gf.img_centre(self.__coin_image)[0], gf.screen_height // 1.13))
        self.__screen.blit(self.__coin_txt,
                           (gf.img_centre(self.__coin_txt)[0], gf.screen_height // 1.03))

        # text
        self.__screen.blit(self.__health_txt, (gf.screen_width // 14, gf.screen_height // 8))
        self.__screen.blit(self.__stamina_txt, (gf.screen_width // 14, gf.screen_height // 5))
        self.__screen.blit(self.__tip_txt_1, (gf.screen_width // 2, gf.screen_height // 8))
        self.__screen.blit(self.__tip_txt_2, (gf.screen_width // 2, gf.screen_height // 6))
        self.__screen.blit(self.__tip_txt_3,
                           (gf.img_centre(self.__tip_txt_3)[0], gf.screen_height // 1.2))

    def tutorial_two_hud(self):
        """
        Description:
            Adds extra elements to the level HUD, in order to explain certain aspects to a new player.
            Runs in the second tutorial level.
        """
        # --- GRAPHICS FOR THE SECOND TUTORIAL LEVEL ---
        self.__screen.blit(self.__objective_txt,
                           (gf.img_centre(self.__objective_txt)[0], gf.screen_height // 1.2))

        self.__screen.blit(self.__death_txt,
                           (gf.img_centre(self.__death_txt)[0], gf.screen_height // 1.1))
