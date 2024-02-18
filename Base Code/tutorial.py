from globalfunctions import *
from mazelevel import MazeLevel
class TutorialClass(MazeLevel):
    def __init__(self, maze_lst):
        super().__init__(maze_lst)
        self.level_type = "tutorial"

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.tutorial_coin_txt = tutorial_font.render("Coin (pickup for 20 points)", 1, white)
        self.tutorial_stamina_txt = tutorial_font.render("Stamina bar (sprint)", 1, white)
        self.tutorial_point_txt_1 = tutorial_font.render("Points (start at 500, they go down as time", 1, white)
        self.tutorial_point_txt_2 = tutorial_font.render("passes, coins and enemy hits increase points)", 1, white)
        self.tutorial_point_txt_3 = tutorial_font.render("Press 'C' to see all controls, press again to close menu", 1,
                                                         white)
        self.tutorial_health_txt = tutorial_font.render("Health Bar (Enemies can attack to lower it)", 1, white)
        self.tutorial_objective_txt = tutorial_font.render(
            "REACH THE PORTAL AT THE END OF THE MAZE WITH AS MANY POINTS AS POSSIBLE!", 1, white)
        self.tutorial_death_txt = tutorial_font.render(
            "RUNNING OUT OF HEARTS ENDS THE GAME", 1, white)

        self.tutorial_coin_image = pygame.image.load(f"../Graphics/powerups/coin.png").convert_alpha()
        self.tutorial_coin_image = pygame.transform.scale(self.tutorial_coin_image, (70, 70))

    def tutorial_hud(self):
        # images
        self.screen.blit(self.tutorial_coin_image,
                         (img_centre(self.tutorial_coin_image)[0], screen_height // 1.13))
        self.screen.blit(self.tutorial_coin_txt,
                         (img_centre(self.tutorial_coin_txt)[0], screen_height // 1.03))

        # text
        self.screen.blit(self.tutorial_health_txt, (screen_width // 14, screen_height // 8))
        self.screen.blit(self.tutorial_stamina_txt, (screen_width // 14, screen_height // 5))
        self.screen.blit(self.tutorial_point_txt_1, (screen_width // 2, screen_height // 8))
        self.screen.blit(self.tutorial_point_txt_2, (screen_width // 2, screen_height // 6))
        self.screen.blit(self.tutorial_point_txt_3,
                         (img_centre(self.tutorial_point_txt_3)[0], screen_height // 1.2))

    def tutorial_two_hud(self):
        self.screen.blit(self.tutorial_objective_txt,
                         (img_centre(self.tutorial_objective_txt)[0], screen_height // 1.2))

        self.screen.blit(self.tutorial_death_txt,
                         (img_centre(self.tutorial_death_txt)[0], screen_height // 1.1))


