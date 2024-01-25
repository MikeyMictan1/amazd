import pygame, sys, os
from level import Level
from settings import *
from debug import debug
from maze import *
from sys import exit
from menu import OptionPress
import time

width = 5  # Must be an odd number (21 BASE)
height = 5  # Must be an odd number (21 BASE)

# creation of the maze as a list
depth_first_maze = df_maze_generation(width, height)
depth_first_maze.main_code()
maze_list = depth_first_maze.create_maze()

# fonts and colours
font = pygame.font.Font("../Fonts/Pixel.ttf", 100)
tutorial_font = pygame.font.Font("../Fonts/Pixel.ttf", 20)
white = (255,255,255)

tutorial = ["XYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYXX", "XP       C     U           E      OX", "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"]

print(maze_list)
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
        #self.level = Level(maze_list)  # creates a level imported from the file "level"
        self.level = Level(tutorial)
        self.game_on = False
        self.in_menu = True
        self.first_run = True
        self.num_of_levels = 4

        self.create_levels()


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
                tutorial_coin_txt = tutorial_font.render("Coin (pickup for 20 points)", 1, white)
                tutorial_controls_txt = tutorial_font.render("WASD To move, LSHIFT to sprint, SPACE to attack", 1, white)
                tutorial_stamina_txt = tutorial_font.render("Stamina bar (sprint)", 1, white)
                tutorial_point_txt_1 = tutorial_font.render("Points (goes down as time passes,", 1, white)
                tutorial_point_txt_2 = tutorial_font.render("coins and enemy hits to increase)", 1, white)
                tutorial_health_txt = tutorial_font.render("Health Bar (Enemies can attack to lower it)", 1, white)

                self.screen.blit(tutorial_health_txt, (screen_width // 14, screen_height // 8))
                self.screen.blit(tutorial_stamina_txt, (screen_width // 14, screen_height // 5))
                self.screen.blit(tutorial_point_txt_1, (screen_width // 2, screen_height // 8))
                self.screen.blit(tutorial_point_txt_2, (screen_width // 2, screen_height // 6))

                self.screen.blit(tutorial_coin_txt, (screen_width // 20, screen_height // 1.1))
                self.screen.blit(tutorial_controls_txt, (screen_width // 2, screen_height // 1.1))





            if self.in_menu == True:
                self.menu()

            self.run_levels(self.all_levels[0], self.level)  # inital second level

            for i in range(self.num_of_levels-1):  # runs 10 levels
                self.run_levels(self.all_levels[i+1], self.all_levels[i])


            pygame.display.update()
            self.clock.tick(FPS)


    def run_levels(self, current_level, previous_level):  # currently does nothing
        if not previous_level.level_active and current_level.level_active:  # if previous level is not active, and current level is active then run the current level
            self.game_on = False
            current_level.run()

            if self.first_run:  # if this is the first loop of this function for the current level, then carryover player data
                current_level.player_level_carryover(previous_level.player.points, previous_level.player.health)

            self.first_run = False  # makes sure all other loops of the function don't carryover player data

            if not current_level.level_active:  # if the game isn't active, set first run to true again for the next level
                self.first_run = True

    def create_levels(self):  # creates all the levels to play (customize later)
        self.all_mazes = []
        self.all_levels = []

        maze_width = 7
        maze_height = 7

        for i in range(self.num_of_levels):
            if i % 2 == 0:
                maze_height += i  # makes the mazes bigger every 2 levels
                maze_width += i

            depth_first_maze = df_maze_generation(maze_width, maze_height)
            depth_first_maze.main_code()
            self.all_mazes.append(depth_first_maze.create_maze())
            self.all_levels.append(Level(self.all_mazes[i]))



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
