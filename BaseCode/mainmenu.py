import sys
import pygame

import buttons as btn
import globalfunctions as gf


class MainMenu:
    def __init__(self):
        self.in_menu = True  # in the menu?
        self.tutorial_on = False  # tutorial option pressed?
        self.game_on = False  # play option pressed?

        # loading logo graphics
        self.__screen = pygame.display.set_mode((gf.screen_width, gf.screen_height))
        self.__logo_image = pygame.image.load(f"../Graphics/amazd_logo.png")
        pygame.display.set_icon(self.__logo_image)
        self.__logo_image = pygame.transform.scale(self.__logo_image, (140, 280))

        # sound effects
        self.__menu_music = pygame.mixer.Sound("../Audio/maze_music.mp3")
        self.__maze_music = pygame.mixer.Sound("../Audio/in_maze_music.mp3")  # undertale

        # The rest of the menu graphics
        self.__character_dict = {"idle_down": []}
        self.__character_dict = gf.import_graphics_dict("character", self.__character_dict, "../Graphics")

        self.__menu_graphics_dict = {"background": [], "high_score": [], "play": [], "quit": [], "tutorial": []}
        self.__menu_graphics_dict = gf.import_graphics_dict("menu", self.__menu_graphics_dict, "../Graphics")

        # menu titles and background
        self.__game_title = gf.font.render("Amaz'd", 1, gf.white)
        self.__main_menu_title = gf.font.render("Main Menu", 1, gf.white)
        self.__background = self.__menu_graphics_dict["background"][0]
        self.__background = pygame.transform.scale(self.__background, (gf.screen_width, gf.screen_height))

        # menu buttons graphics
        self.__reset_score_white = self.__menu_graphics_dict["high_score"][0]
        self.__reset_score_yellow = self.__menu_graphics_dict["high_score"][1]
        self.__reset_score_pos = (gf.screen_width // 10, gf.screen_height // 1.25)

        self.__play_txt_white = self.__menu_graphics_dict["play"][0]
        self.__play_txt_yellow = self.__menu_graphics_dict["play"][1]
        self.__play_txt_pos = (gf.screen_width // 10, gf.screen_height // 2.7)

        self.__tutorial_txt_white = self.__menu_graphics_dict["tutorial"][0]
        self.__tutorial_txt_yellow = self.__menu_graphics_dict["tutorial"][1]
        self.__tutorial_txt_pos = (gf.screen_width // 10, gf.screen_height // 1.93)

        self.__quit_txt_white = self.__menu_graphics_dict["quit"][0]
        self.__quit_txt_yellow = self.__menu_graphics_dict["quit"][1]
        self.__quit_txt_pos = (gf.screen_width // 10, gf.screen_height // 1.5)

    def __game_option_pressed(self):
        self.__menu_music.stop()
        self.__maze_music.play(999)
        self.__maze_music.set_volume(0.05)
        self.in_menu = False

    # code for starting menu
    def menu(self):
        # initialising needed variables
        pygame.mixer.stop()

        frame = 0
        frame_speed = 0.1

        self.__menu_music.play(999)
        self.__menu_music.set_volume(0.1)

        while self.in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # menu visuals
            self.__screen.blit(self.__background, (0, 0))
            self.__screen.blit(self.__logo_image,
                               (gf.img_centre(self.__logo_image)[0], gf.img_centre(self.__logo_image)[1]))

            self.__screen.blit(self.__game_title, (gf.img_centre(self.__game_title)[0], gf.screen_height // 20))
            self.__screen.blit(self.__main_menu_title,
                               (gf.img_centre(self.__main_menu_title)[0], gf.screen_height // 5))

            # drawing high-score onto the screen
            with open("high_score.txt", "r") as high_score_file:  # reads the file for the high score
                self.high_score = int(high_score_file.read())

            high_score_txt = gf.high_score_font.render(f"High Score: {self.high_score}", 1, gf.white)
            self.__screen.blit(high_score_txt,
                               (gf.screen_width // 2 - high_score_txt.get_width() // 2, gf.screen_height // 1.2))

            # drawing animated character onto the screen
            frame += frame_speed
            if frame >= len(self.__character_dict["idle_down"]):
                frame = 0

            character_image = self.__character_dict["idle_down"][int(frame)]
            character_image = pygame.transform.scale(character_image, (200 * 3, 160 * 3))
            self.__screen.blit(character_image, (gf.screen_width // 2.2, gf.screen_height // 3.5))

            # drawing buttons onto the screen
            self.handle_menu_buttons()

            pygame.display.update()

    def handle_menu_buttons(self):
        # play menu option
        self.__play_option = btn.OptionPress(self.__play_txt_white, self.__play_txt_yellow, self.__play_txt_pos)
        self.__play_option.draw(pygame.display.get_surface())

        if self.__play_option.pressed:  # plays the game if "play" pressed
            self.__game_option_pressed()
            self.game_on = True

        # tutorial menu option
        self.__tutorial_option = btn.OptionPress(self.__tutorial_txt_white, self.__tutorial_txt_yellow,
                                             self.__tutorial_txt_pos)
        self.__tutorial_option.draw(pygame.display.get_surface())

        if self.__tutorial_option.pressed:
            self.__game_option_pressed()
            self.tutorial_on = True

        # quit menu option
        self.__quit_option = btn.OptionPress(self.__quit_txt_white, self.__quit_txt_yellow, self.__quit_txt_pos)
        self.__quit_option.draw(pygame.display.get_surface())

        if self.__quit_option.pressed:
            pygame.quit()
            sys.exit()

        # reset high score option
        self.__reset_score_option = btn.OptionPress(self.__reset_score_white, self.__reset_score_yellow,
                                                self.__reset_score_pos)
        self.__reset_score_option.draw(pygame.display.get_surface())

        if self.__reset_score_option.pressed:
            with open("high_score.txt", "w") as high_score_file:
                high_score_file.write("0")
