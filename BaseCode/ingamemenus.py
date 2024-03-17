import sys
import pygame

import gamechange as g_change
import globalfunctions as gf
import buttons as btn


class InGameMenu(g_change.GameChange):
    def __init__(self):
        super().__init__()
        self.in_game_menu_state = False

        self.__in_game_menu_graphics_dict = {"continue": [], "overlay": []}
        self.__in_game_menu_graphics_dict = gf.import_graphics_dict("ingamemenu", self.__in_game_menu_graphics_dict,
                                                                 "../Graphics")

        self.__menu_txt_pos = (gf.img_centre(self.menu_txt_white)[0], gf.screen_height // 2.6)
        self.__menu_option = btn.OptionPress(self.menu_txt_white, self.menu_txt_yellow, self.__menu_txt_pos)
        self.__quit_txt_pos = (gf.img_centre(self.quit_txt_white)[0], gf.screen_height // 1.3)
        self.__quit_option = btn.OptionPress(self.quit_txt_white, self.quit_txt_yellow, self.__quit_txt_pos)

        self.__continue_txt_white = self.__in_game_menu_graphics_dict["continue"][0]
        self.__continue_txt_yellow = self.__in_game_menu_graphics_dict["continue"][1]
        self.__continue_txt_pos = (gf.img_centre(self.__continue_txt_white)[0], gf.screen_height // 1.75)
        self.__continue_option = btn.OptionPress(self.__continue_txt_white, self.__continue_txt_yellow,
                                             self.__continue_txt_pos)

        self.menu_overlay = self.__in_game_menu_graphics_dict["overlay"][0]
        self.menu_overlay = pygame.transform.scale(self.menu_overlay, (1100, 800))

        self.__in_game_menu_txt = gf.font.render("IN-GAME MENU", 1, gf.white)
        self.__in_game_menu_sound = pygame.mixer.Sound("../Audio/open_maze_menu1.mp3")

        self.escape_counter = 0

    def run_menu(self):
        self.__in_game_menu_sound.play()
        self.__in_game_menu_sound.set_volume(0.1)
        self.escape_counter += 1
        self.in_game_menu_state = True

    def display_menu(self):
        if self.escape_counter % 2 == 0:  # makes sure esc will open AND close the in game menu
            self.in_game_menu_state = False

        self.screen.blit(self.menu_overlay, (gf.img_centre(self.menu_overlay)[0], gf.img_centre(self.menu_overlay)[1]))
        self.screen.blit(self.__in_game_menu_txt, (gf.img_centre(self.__in_game_menu_txt)[0], gf.screen_height // 10))

        self.__menu_option.draw(pygame.display.get_surface())
        self.__continue_option.draw(pygame.display.get_surface())
        self.__quit_option.draw(pygame.display.get_surface())

        if self.__continue_option.pressed:
            self.escape_counter += 1
            self.in_game_menu_state = False
            self.__continue_option.pressed = False

        if self.__menu_option.pressed:
            self.escape_counter += 1
            self.__menu_option.pressed = False
            self.in_game_menu_state = False
            return True  # so we know that the menu option has been pressed

        if self.__quit_option.pressed:  # quits the game if "quit" is pressed
            pygame.quit()
            sys.exit()


class ControlsMenu(InGameMenu):
    def __init__(self):
        super().__init__()
        self.__control_set_image = pygame.image.load("../Graphics/controls/control_set.png")
        self.__control_set_image = pygame.transform.scale(self.__control_set_image, (500, 600))

    def display_menu(self):
        if self.escape_counter % 2 == 0:
            self.in_game_menu_state = False

        self.screen.blit(self.menu_overlay, (gf.img_centre(self.menu_overlay)[0], gf.img_centre(self.menu_overlay)[1]))
        self.screen.blit(self.__control_set_image,
                         (gf.img_centre(self.__control_set_image)[0], gf.img_centre(self.__control_set_image)[1]))
