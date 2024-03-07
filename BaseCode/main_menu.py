import sys
from buttons import *

class MainMenu:
    def __init__(self):
        self.in_menu = True  # in the menu?
        self.tutorial_on = False  # tutorial option pressed?
        self.game_on = False  # play option pressed?

        # loading logo graphics
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.logo_image = pygame.image.load(f"../Graphics/amazd_logo.png")
        pygame.display.set_icon(self.logo_image)
        self.logo_image = pygame.transform.scale(self.logo_image, (140, 280))

        # sound effects
        self.menu_music = pygame.mixer.Sound("../Audio/maze_music.mp3")
        self.maze_music = pygame.mixer.Sound("../Audio/in_maze_music.mp3")  # undertale

        # The rest of the menu graphics
        self.character_dict = {"idle_down": []}
        self.character_dict = import_graphics_dict("character", self.character_dict, "../Graphics")

        self.menu_graphics_dict = {"background": [], "high_score": [], "play": [], "quit": [], "tutorial": []}
        self.menu_graphics_dict = import_graphics_dict("menu", self.menu_graphics_dict, "../Graphics")

        # menu titles and background
        self.game_title = font.render("Amaz'd", 1, white)
        self.main_menu_title = font.render("Main Menu", 1, white)
        self.background = self.menu_graphics_dict["background"][0]
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

        # menu buttons graphics
        self.reset_score_white = self.menu_graphics_dict["high_score"][0]
        self.reset_score_yellow = self.menu_graphics_dict["high_score"][1]
        self.reset_score_pos = (screen_width // 10, screen_height // 1.25)

        self.play_txt_white = self.menu_graphics_dict["play"][0]
        self.play_txt_yellow = self.menu_graphics_dict["play"][1]
        self.play_txt_pos = (screen_width // 10, screen_height // 2.7)

        self.tutorial_txt_white = self.menu_graphics_dict["tutorial"][0]
        self.tutorial_txt_yellow = self.menu_graphics_dict["tutorial"][1]
        self.tutorial_txt_pos = (screen_width // 10, screen_height // 1.93)

        self.quit_txt_white = self.menu_graphics_dict["quit"][0]
        self.quit_txt_yellow = self.menu_graphics_dict["quit"][1]
        self.quit_txt_pos = (screen_width // 10, screen_height // 1.5)

    def game_option_pressed(self):
        self.menu_music.stop()
        self.maze_music.play(999)
        self.maze_music.set_volume(0.05)
        self.in_menu = False

    # code for starting menu
    def menu(self):
        # initialising needed variables
        pygame.mixer.stop()

        frame = 0
        frame_speed = 0.1

        self.menu_music.play(999)
        self.menu_music.set_volume(0.1)

        while self.in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # menu visuals
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.logo_image,
                             (img_centre(self.logo_image)[0], img_centre(self.logo_image)[1]))

            self.screen.blit(self.game_title, (img_centre(self.game_title)[0], screen_height // 20))
            self.screen.blit(self.main_menu_title, (img_centre(self.main_menu_title)[0], screen_height // 5))

            # drawing high-score onto the screen
            with open("high_score.txt", "r") as high_score_file:  # reads the file for the high score
                self.high_score = int(high_score_file.read())

            high_score_txt = high_score_font.render(f"High Score: {self.high_score}", 1, white)
            self.screen.blit(high_score_txt,
                             (screen_width // 2 - high_score_txt.get_width() // 2, screen_height // 1.2))

            # drawing animated character onto the screen
            frame += frame_speed
            if frame >= len(self.character_dict["idle_down"]):
                frame = 0

            character_image = self.character_dict["idle_down"][int(frame)]
            character_image = pygame.transform.scale(character_image, (200 * 3, 160 * 3))
            self.screen.blit(character_image, (screen_width // 2.2, screen_height // 3.5))

            # drawing buttons onto the screen
            self.handle_menu_buttons()

            pygame.display.update()

    def handle_menu_buttons(self):
        # play menu option
        self.play_option = OptionPress(self.play_txt_white, self.play_txt_yellow, self.play_txt_pos)
        self.play_option.draw(pygame.display.get_surface())

        if self.play_option.pressed:  # plays the game if "play" pressed
            self.game_option_pressed()
            self.game_on = True

        # tutorial menu option
        self.tutorial_option = OptionPress(self.tutorial_txt_white, self.tutorial_txt_yellow, self.tutorial_txt_pos)
        self.tutorial_option.draw(pygame.display.get_surface())

        if self.tutorial_option.pressed:
            self.game_option_pressed()
            self.tutorial_on = True

        # quit menu option
        self.quit_option = OptionPress(self.quit_txt_white, self.quit_txt_yellow, self.quit_txt_pos)
        self.quit_option.draw(pygame.display.get_surface())

        if self.quit_option.pressed:
            pygame.quit()
            sys.exit()

        # reset high score option
        self.reset_score_option = OptionPress(self.reset_score_white, self.reset_score_yellow, self.reset_score_pos)
        self.reset_score_option.draw(pygame.display.get_surface())

        if self.reset_score_option.pressed:
            with open("high_score.txt", "w") as high_score_file:
                high_score_file.write("0")

