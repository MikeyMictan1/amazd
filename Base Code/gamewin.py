import pygame, os, sys
from settings import screen_width, screen_height, FPS, white
from menu import OptionPress


class GameWin:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.game_win_state = True

        # Graphics
        self.background = pygame.transform.scale(pygame.image.load("../Graphics/gamewin/background/game_win_background.png"),
                                            (screen_width, screen_height))
        self.logo_image = pygame.transform.scale(pygame.image.load(f"../Graphics/amazd_logo.png"), (140, 280))

        # menu text
        self.menu_txt_white = pygame.image.load("../Graphics/gameover/menu_white.png")
        self.menu_txt_yellow = pygame.image.load("../Graphics/gameover/menu_yellow.png")
        self.menu_txt_pos = (screen_width // 10, screen_height // 1.5)
        self.menu_option = OptionPress(self.menu_txt_white, self.menu_txt_yellow, self.menu_txt_pos)

        # quit game text
        self.quit_txt_white = pygame.image.load("../Graphics/menu/quit_white.png")
        self.quit_txt_yellow = pygame.image.load("../Graphics/menu/quit_yellow.png")
        self.quit_txt_pos = (screen_width // 1.4, screen_height // 1.5)
        self.quit_option = OptionPress(self.quit_txt_white, self.quit_txt_yellow, self.quit_txt_pos)

        # other text
        self.game_win_font = pygame.font.Font("../Fonts/Pixel.ttf", 100)
        self.game_win_txt = self.game_win_font.render("VICTORY!", 1, white)

        self.game_win_points_font = pygame.font.Font("../Fonts/Pixel.ttf", 60)
        self.amazd_txt = self.game_win_points_font.render("(You Have Amaz'd Me)", 1, white)

        # music
        self.game_win_music = pygame.mixer.Sound("../Audio/victory_music.mp3")

        self.frame = 0
        self.frame_speed = 0.1


    def run(self, points):
        self.end_points = int(points)
        self.score_txt = self.game_win_points_font.render(f"POINTS THIS RUN:{self.end_points}", 1, white)

        pygame.mixer.stop()
        self.game_win_music.play()
        self.game_win_music.set_volume(0.1)
        while self.game_win_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # game over visuals
            self.screen.blit(self.background, (0, 0))

            self.screen.blit(self.game_win_txt, (screen_width // 2 - self.game_win_txt.get_width() // 2, screen_height // 20))
            self.screen.blit(self.amazd_txt, (screen_width // 2 - self.amazd_txt.get_width() // 2, screen_height // 6))
            self.screen.blit(self.score_txt, (screen_width // 2 - self.score_txt.get_width() // 2, screen_height // 3))
            self.screen.blit(self.logo_image, (screen_width // 2 - self.logo_image.get_width() // 2, screen_height // 1.5))


            # fallen player visuals
            player_path = ('../Graphics/gamewin/victory_slime/')

            file_lst = []
            for file in os.listdir(player_path):
                file_lst.append(file)

            self.frame += self.frame_speed

            if self.frame >= len(file_lst):
                self.frame = 0

            player_image = pygame.image.load(f"{player_path}{file_lst[int(self.frame)]}").convert_alpha()
            player_image = pygame.transform.scale(player_image, (200, 160))
            self.screen.blit(player_image, (screen_width//2 - player_image.get_width()//2, screen_height//2 - player_image.get_height()//2))

            # draw buttons
            self.menu_option.draw(pygame.display.get_surface())
            self.quit_option.draw(pygame.display.get_surface())

            if self.menu_option.pressed == True:  # plays the game if "play" pressed
                self.game_win_state = False

            if self.quit_option.pressed == True:  # quits the game if "quit" is pressed
                pygame.quit()
                sys.exit()


            pygame.display.update()
            self.clock.tick(FPS)

