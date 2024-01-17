import pygame, sys, os
from level import Level
from settings import *
from debug import debug
from maze import *
from sys import exit
from menu import OptionPress
import time

width = 7  # Must be an odd number (21 BASE)
height = 7  # Must be an odd number (21 BASE)

# creation of the maze as a list
depth_first_maze = df_maze_generation(width, height)
depth_first_maze.main_code()
maze_list = depth_first_maze.create_maze()
maze_list_2 = depth_first_maze.create_maze()


# fonts and colours
font = pygame.font.Font("../Fonts/Pixel.ttf", 100)
white = (255,255,255)

for row in maze_list:
    print(row)

#keys = pygame.key.get_pressed()
# ----------------------------------------
        # pygame setup
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width,screen_height))
        pygame.display.set_caption("Amaz'd")
        self.clock = pygame.time.Clock()
        self.level = Level(maze_list)  # creates a level imported from the file "level"
        self.level_2 = Level(maze_list_2)
        self.game_on = False
        self.in_menu = True

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # in-game menu
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    print("tryna quit")

            self.screen.fill("black")


            if self.game_on == True:
                self.level.run()  # running level command in level.py

            if self.in_menu == True:
                self.menu()


            if self.level.level_active == False:
                print("exit reached level is over")
                self.game_on = False
                self.level_2.run()

            pygame.display.update()
            self.clock.tick(FPS)

    # code for starting menu
    def menu(self):
        # initialising needed variables
        keys = pygame.key.get_pressed()
        frame = 0
        frame_speed = 0.1
        enter_maze_sound = pygame.mixer.Sound("../Audio/enter_maze_music.mp3") # undertale
        menu_music = pygame.mixer.Sound("../Audio/maze_music.mp3")
        menu_music.play()
        menu_music.set_volume(0.1)

        while self.in_menu == True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            # menu visuals
            background = pygame.transform.scale(pygame.image.load("../Graphics/menu/menubackground.png"),(screen_width, screen_height))
            self.screen.blit(background, (0, 0))

            title = font.render("Amaz'd", 1, white)
            self.screen.blit(title, (screen_width//2 - title.get_width() // 2, screen_height//20))

            menu_txt = font.render("Main Menu", 1, white)
            self.screen.blit(menu_txt, (screen_width//2 - menu_txt.get_width() // 2, screen_height//5))

            # animated character on menu screen
            player_path = ('../Graphics/character/idle_down/')

            file_lst = []
            for file in os.listdir(player_path):
                file_lst.append(file)

            frame += frame_speed

            if frame >= len(file_lst):
                frame = 0
            player_image = pygame.image.load(f"{player_path}{file_lst[int(frame)]}").convert_alpha()
            player_image = pygame.transform.scale(player_image, (200*3, 160*3))
            self.screen.blit(player_image, (screen_width//2.2, screen_height//3.5))

            # play menu text
            self.play_txt_white = pygame.image.load("../Graphics/menu/play_white.png")
            self.play_txt_yellow = pygame.image.load("../Graphics/menu/play_yellow.png")
            self.play_txt_pos = (screen_width//10, screen_height//2.5)

            self.play_option = OptionPress(self.play_txt_white, self.play_txt_yellow, self.play_txt_pos)
            self.play_option.draw(pygame.display.get_surface())

            # plays the game if "play" pressed
            if self.play_option.pressed == True:
                menu_music.stop()
                enter_maze_sound.play()
                self.game_on = True
                self.in_menu = False



            # quit menu text
            self.quit_txt_white = pygame.image.load("../Graphics/menu/quit_white.png")
            self.quit_txt_yellow = pygame.image.load("../Graphics/menu/quit_yellow.png")
            self.quit_txt_pos = (screen_width//10, screen_height//1.7)

            self.quit_option = OptionPress(self.quit_txt_white, self.quit_txt_yellow, self.quit_txt_pos)
            self.quit_option.draw(pygame.display.get_surface())

            # quits the game if "quit" is pressed
            if self.quit_option.pressed == True:
                pygame.quit()
                sys.exit()

            pygame.display.update()
            self.clock.tick(FPS)


# ----------------------------------
# running the game
game = Game()

while True:
    game.run()
