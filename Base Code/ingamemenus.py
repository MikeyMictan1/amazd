from gamechange import GameChange
from globalfunctions import *
from buttons import OptionPress
import sys
class InGameMenu(GameChange):
    def __init__(self):
        super().__init__()
        self.in_game_menu_state = False

        self.in_game_menu_graphics_dict = {"continue":[], "overlay":[]}
        self.in_game_menu_graphics_dict = import_graphics_dict("ingamemenu", self.in_game_menu_graphics_dict, "../Graphics")

        self.menu_txt_pos = (img_centre(self.menu_txt_white)[0], screen_height // 2.6)
        self.menu_option = OptionPress(self.menu_txt_white, self.menu_txt_yellow, self.menu_txt_pos)
        self.quit_txt_pos = (img_centre(self.quit_txt_white)[0], screen_height // 1.3)
        self.quit_option = OptionPress(self.quit_txt_white, self.quit_txt_yellow, self.quit_txt_pos)

        self.continue_txt_white = self.in_game_menu_graphics_dict["continue"][0]
        self.continue_txt_yellow = self.in_game_menu_graphics_dict["continue"][1]
        self.continue_txt_pos = (img_centre(self.continue_txt_white)[0], screen_height // 1.75)
        self.continue_option = OptionPress(self.continue_txt_white, self.continue_txt_yellow, self.continue_txt_pos)

        self.menu_overlay = self.in_game_menu_graphics_dict["overlay"][0]
        self.menu_overlay = pygame.transform.scale(self.menu_overlay, (1100, 800))

        self.in_game_menu_txt = font.render("IN-GAME MENU", 1, white)
        self.in_game_menu_sound = pygame.mixer.Sound("../Audio/open_maze_menu1.mp3")

        self.escape_counter = 0

    def run_menu(self):
        self.in_game_menu_sound.play()
        self.in_game_menu_sound.set_volume(0.1)
        self.escape_counter += 1
        self.in_game_menu_state = True

    def display_menu(self):
        if self.escape_counter % 2 == 0:  # makes sure esc will open AND close the in game menu
            self.in_game_menu_state = False

        self.screen.blit(self.menu_overlay, (img_centre(self.menu_overlay)[0], img_centre(self.menu_overlay)[1]))
        self.screen.blit(self.in_game_menu_txt, (img_centre(self.in_game_menu_txt)[0], screen_height // 10))

        self.menu_option.draw(pygame.display.get_surface())
        self.continue_option.draw(pygame.display.get_surface())
        self.quit_option.draw(pygame.display.get_surface())

        if self.continue_option.pressed:
            self.escape_counter += 1
            self.in_game_menu_state = False
            self.continue_option.pressed = False

        if self.menu_option.pressed:
            self.escape_counter += 1
            self.menu_option.pressed = False
            self.in_game_menu_state = False
            return True  # so we know that the menu option has been pressed

        if self.quit_option.pressed:  # quits the game if "quit" is pressed
            pygame.quit()
            sys.exit()



class ControlsMenu(InGameMenu):
    def __init__(self):
        super().__init__()
        self.control_set_image = pygame.image.load("../Graphics/controls/control_set.png")
        self.control_set_image = pygame.transform.scale(self.control_set_image, (500, 600))

    def display_menu(self):
        if self.escape_counter % 2 == 0:
            self.in_game_menu_state = False

        self.screen.blit(self.menu_overlay, (img_centre(self.menu_overlay)[0], img_centre(self.menu_overlay)[1]))
        self.screen.blit(self.control_set_image, (img_centre(self.control_set_image)[0], img_centre(self.control_set_image)[1]))



