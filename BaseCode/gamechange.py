import pygame, sys
from globalfunctions import *
from buttons import OptionPress
#

class GameChange:
    def __init__(self):
        pygame.init()
        self.game_change_state = True
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        # game change graphics
        self.game_change_graphics_dict = {"menu":[], "quit": []}
        self.game_change_graphics_dict = import_graphics_dict("gamechange", self.game_change_graphics_dict, "../Graphics")

        # menu text
        self.menu_txt_white = self.game_change_graphics_dict["menu"][0]
        self.menu_txt_yellow = self.game_change_graphics_dict["menu"][1]
        self.__menu_txt_pos = (screen_width // 10, screen_height // 1.5)
        self.__menu_option = OptionPress(self.menu_txt_white, self.menu_txt_yellow, self.__menu_txt_pos)

        # quit game text
        self.quit_txt_white = self.game_change_graphics_dict["quit"][0]
        self.quit_txt_yellow = self.game_change_graphics_dict["quit"][1]
        self.__quit_txt_pos = (screen_width // 1.4, screen_height // 1.5)
        self.__quit_option = OptionPress(self.quit_txt_white, self.quit_txt_yellow, self.__quit_txt_pos)

        self.game_change_font = pygame.font.Font("../Fonts/Pixel.ttf", 100)
        self.game_change_points_font = pygame.font.Font("../Fonts/Pixel.ttf", 60)

        self.frame = 0
        self.frame_speed = 0.1

    def event_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def display_menu(self):
        # draw buttons
        self.__menu_option.draw(pygame.display.get_surface())
        self.__quit_option.draw(pygame.display.get_surface())

        if self.__menu_option.pressed == True:  # returns player to the menu if "menu" pressed
            self.game_win_state = False
            self.game_over_state = False

        if self.__quit_option.pressed == True:  # quits the game if "quit" is pressed
            pygame.quit()
            sys.exit()

        pygame.display.update()
        self.clock.tick(FPS)


class GameOver(GameChange):
    def __init__(self):
        super().__init__()
        self.game_over_state = True


        # Graphics importing
        self.game_over_graphics_dict = {"background": [], "fallen_player":[]}
        self.game_over_graphics_dict = import_graphics_dict("gameover", self.game_over_graphics_dict, "../Graphics")

        self.background = self.game_over_graphics_dict["background"][0]
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

        # other text
        self.game_over_txt = self.game_change_font.render("GAME OVER!", 1, white)
        self.game_over_music = pygame.mixer.Sound("../Audio/game_over_music.mp3")

    def run(self, points):
        self.end_points = int(points)
        self.score_txt = self.game_change_points_font.render(f"POINTS BEFORE DEATH:{self.end_points}", 1, white)

        pygame.mixer.stop()
        self.game_over_music.play()
        self.game_over_music.set_volume(0.1)

        while self.game_over_state:
            self.event_quit()

            # game over visuals
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.game_over_txt, (img_centre(self.game_over_txt)[0], screen_height // 20))
            self.screen.blit(self.score_txt, (img_centre(self.score_txt)[0], screen_height // 4))

            self.frame += self.frame_speed
            if self.frame >= len(self.game_over_graphics_dict["fallen_player"]):
                self.frame = 0

            character_image = self.game_over_graphics_dict["fallen_player"][int(self.frame)]
            character_image = pygame.transform.scale(character_image, (200, 160))
            self.screen.blit(character_image, (img_centre(character_image)[0], img_centre(character_image)[1]))

            # draw buttons onto menu
            self.display_menu()


class GameWin(GameChange):
    def __init__(self):
        super().__init__()
        self.game_win_state = True

        # Graphics
        self.game_win_graphics_dict = {"background": [], "victory_slime":[]}
        self.game_win_graphics_dict = import_graphics_dict("gamewin", self.game_win_graphics_dict, "../Graphics")

        self.background = self.game_win_graphics_dict["background"][0]
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.logo_image = pygame.transform.scale(pygame.image.load(f"../Graphics/amazd_logo.png"), (140, 280))

        # other text
        self.game_win_txt = self.game_change_font.render("VICTORY!", 1, white)
        self.amazd_txt = self.game_change_points_font.render("(You Have Amaz'd Me)", 1, white)
        self.game_win_music = pygame.mixer.Sound("../Audio/victory_music.mp3")

    def run(self, points):
        self.end_points = int(points)
        self.score_txt = self.game_change_points_font.render(f"POINTS:{self.end_points}", 1, white)

        pygame.mixer.stop()
        self.game_win_music.play()
        self.game_win_music.set_volume(0.1)

        while self.game_win_state:
            self.event_quit()

            # game over visuals
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.game_win_txt, (img_centre(self.game_win_txt)[0], screen_height // 20))
            self.screen.blit(self.amazd_txt, (img_centre(self.amazd_txt)[0], screen_height // 6))
            self.screen.blit(self.score_txt, (img_centre(self.score_txt)[0], screen_height // 3))
            self.screen.blit(self.logo_image, (img_centre(self.logo_image)[0], screen_height // 1.5))

            self.frame += self.frame_speed
            if self.frame >= len(self.game_win_graphics_dict["victory_slime"]):
                self.frame = 0

            character_image = self.game_win_graphics_dict["victory_slime"][int(self.frame)]
            character_image = pygame.transform.scale(character_image, (200, 160))
            self.screen.blit(character_image, (img_centre(character_image)[0], img_centre(character_image)[1]))

            # draw buttons onto menu
            self.display_menu()


