import pygame

import globalfunctions as gf
from mazelevel import MazeLevel


class TutorialLevel(MazeLevel):
    def __init__(self, maze_lst):
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
        self.death_txt = gf.tutorial_font.render(
            "RUNNING OUT OF HEARTS ENDS THE GAME", 1, gf.white)

        self.coin_image = pygame.image.load(f"../Graphics/powerups/coin.png").convert_alpha()
        self.coin_image = pygame.transform.scale(self.coin_image, (70, 70))

    def tutorial_hud(self):
        # --- GRAPHICS FOR THE FIRST TUTORIAL LEVEL ---
        # images
        self.__screen.blit(self.coin_image,
                           (gf.img_centre(self.coin_image)[0], gf.screen_height // 1.13))
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
        # --- GRAPHICS FOR THE SECOND TUTORIAL LEVEL ---
        self.__screen.blit(self.__objective_txt,
                           (gf.img_centre(self.__objective_txt)[0], gf.screen_height // 1.2))

        self.__screen.blit(self.death_txt,
                           (gf.img_centre(self.death_txt)[0], gf.screen_height // 1.1))
