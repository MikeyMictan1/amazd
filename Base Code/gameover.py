import pygame, os, sys
from settings import screen_width, screen_height, FPS, white
from menu import OptionPress


class GameOver:
    def __init__(self, player):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.game_over_state = True
        self.player = player
        # Graphics
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
        self.game_over_font = pygame.font.Font("../Fonts/Pixel.ttf", 100)
        self.game_over_txt = self.game_over_font.render("GAME OVER!", 1, white)

        self.game_over_points_font = pygame.font.Font("../Fonts/Pixel.ttf", 60)

        self.game_over_music = pygame.mixer.Sound("../Audio/game_over_music.mp3")

        self.frame = 0
        self.frame_speed = 0.05


    def run(self):
        self.end_points = int(self.player.points)
        self.score_txt = self.game_over_points_font.render(f"POINTS BEFORE DEATH:{self.end_points}", 1, white)

        pygame.mixer.stop()
        self.game_over_music.play()
        self.game_over_music.set_volume(0.1)
        while self.game_over_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # game over visuals
            background = pygame.transform.scale(pygame.image.load("../Graphics/gameover/gameover_background.png"),(screen_width, screen_height))
            self.screen.blit(background, (0, 0))

            self.screen.blit(self.game_over_txt, (screen_width // 2 - self.game_over_txt.get_width() // 2, screen_height // 20))
            self.screen.blit(self.score_txt, (screen_width // 2 - self.score_txt.get_width() // 2, screen_height // 4))

            # fallen player visuals
            player_path = ('../Graphics/gameover/fallen_player/')

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
                self.game_over_state = False

            if self.quit_option.pressed == True:  # quits the game if "quit" is pressed
                pygame.quit()
                sys.exit()


            pygame.display.update()
            self.clock.tick(FPS)


