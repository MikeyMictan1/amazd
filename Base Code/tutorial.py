from globalfunctions import *
from mazelevel import MazeLevel
class TutorialLevel(MazeLevel):
    def __init__(self, maze_lst):
        super().__init__(maze_lst)
        self.level_type = "tutorial"

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.coin_txt = tutorial_font.render("Coin (pickup for 20 points)", 1, white)
        self.stamina_txt = tutorial_font.render("Stamina bar (sprint)", 1, white)
        self.tip_txt_1 = tutorial_font.render("Points (start at 500, they go down as time", 1, white)
        self.tip_txt_2 = tutorial_font.render("passes, coins and enemy hits increase points)", 1, white)
        self.tip_txt_3 = tutorial_font.render("Press 'C' to see all controls, press again to close menu", 1,
                                              white)
        self.health_txt = tutorial_font.render("Health Bar (Enemies can attack to lower it)", 1, white)
        self.objective_txt = tutorial_font.render(
            "REACH THE PORTAL AT THE END OF THE MAZE WITH AS MANY POINTS AS POSSIBLE!", 1, white)
        self.death_txt = tutorial_font.render(
            "RUNNING OUT OF HEARTS ENDS THE GAME", 1, white)

        self.coin_image = pygame.image.load(f"../Graphics/powerups/coin.png").convert_alpha()
        self.coin_image = pygame.transform.scale(self.coin_image, (70, 70))

    def tutorial_hud(self):
        # images
        self.screen.blit(self.coin_image,
                         (img_centre(self.coin_image)[0], screen_height // 1.13))
        self.screen.blit(self.coin_txt,
                         (img_centre(self.coin_txt)[0], screen_height // 1.03))

        # text
        self.screen.blit(self.health_txt, (screen_width // 14, screen_height // 8))
        self.screen.blit(self.stamina_txt, (screen_width // 14, screen_height // 5))
        self.screen.blit(self.tip_txt_1, (screen_width // 2, screen_height // 8))
        self.screen.blit(self.tip_txt_2, (screen_width // 2, screen_height // 6))
        self.screen.blit(self.tip_txt_3,
                         (img_centre(self.tip_txt_3)[0], screen_height // 1.2))

    def tutorial_two_hud(self):
        self.screen.blit(self.objective_txt,
                         (img_centre(self.objective_txt)[0], screen_height // 1.2))

        self.screen.blit(self.death_txt,
                         (img_centre(self.death_txt)[0], screen_height // 1.1))


