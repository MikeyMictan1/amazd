import pygame, sys, os
from level import Level
from settings import *
from debug import debug
from maze import *
from sys import exit
from menu import OptionPress
import time
from support import *
from customlevels import tutorial, boss_arena

width = 5  # Must be an odd number (21 BASE)
height = 5  # Must be an odd number (21 BASE)


# creates the tutorial maze
tutorial_maze = df_maze_generation(13, 13)
tutorial_maze.main_code()
tutorial_maze_list = tutorial_maze.create_maze()

# fonts and colours
font = pygame.font.Font("../Fonts/Pixel.ttf", 100)
high_score_font = pygame.font.Font("../Fonts/Pixel.ttf", 50)
tutorial_font = pygame.font.Font("../Fonts/Pixel.ttf", 20)
white = (255,255,255)

for row in tutorial_maze_list:
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

        self.tutorial = Level(tutorial)
        self.boss_level = Level(boss_arena)
        self.tutorial_maze = Level(tutorial_maze_list)

        self.game_on = False
        self.tutorial_on = False
        self.in_menu = True
        self.first_run = True
        self.num_of_levels = 10

        self.create_levels()

        # tutorial text and graphics
        self.tutorial_coin_txt = tutorial_font.render("Coin (pickup for 20 points)", 1, white)
        self.tutorial_controls_txt = tutorial_font.render("LSHIFT to sprint, WASD To move, SPACE to attack", 1, white)
        self.tutorial_stamina_txt = tutorial_font.render("Stamina bar (sprint)", 1, white)
        self.tutorial_point_txt_1 = tutorial_font.render("Points (start at 500, they go down as time", 1, white)
        self.tutorial_point_txt_2 = tutorial_font.render("passes, coins and enemy hits increase points)", 1, white)
        self.tutorial_health_txt = tutorial_font.render("Health Bar (Enemies can attack to lower it)", 1, white)
        self.tutorial_objective_txt = tutorial_font.render(
            "REACH THE PORTAL AT THE END OF THE MAZE WITH AS MANY POINTS AS POSSIBLE!", 1, white)
        self.tutorial_death_txt = tutorial_font.render(
            "RUNNING OUT OF HEARTS ENDS THE GAME", 1, white)

        self.tutorial_coin_image = pygame.image.load(f"../Graphics/powerups/coin.png").convert_alpha()
        self.tutorial_coin_image = pygame.transform.scale(self.tutorial_coin_image, (70, 70))

        self.menu_graphics = import_folder("../Graphics/menu/tutorial_keys")
        self.tutorial_w_key_image = pygame.transform.scale(self.menu_graphics[5], (40, 40))
        self.tutorial_a_key_image = pygame.transform.scale(self.menu_graphics[0], (40, 40))
        self.tutorial_s_key_image = pygame.transform.scale(self.menu_graphics[4], (40, 40))
        self.tutorial_d_key_image = pygame.transform.scale(self.menu_graphics[1], (40, 40))

        self.tutorial_lshift_key_image = pygame.transform.scale(self.menu_graphics[2], (70, 40))
        self.tutorial_space_key_image = pygame.transform.scale(self.menu_graphics[3], (70, 40))

        # self.log
        self.logo_image = pygame.image.load(f"../Graphics/amazd_logo.png")
        pygame.display.set_icon(self.logo_image)
        self.logo_image = pygame.transform.scale(self.logo_image, (140, 280))




    def run_tutorial(self):
        if self.tutorial_on:  # runs the game tutorial

            #with open("high_score.txt", "r+") as high_score_file:  # if file is empty, set score to 0
            #    if high_score_file.read() == "":
            #        high_score_file.write("0")

            #with open("high_score.txt", "r") as high_score_file:  # reads the file for the high score
            #    self.real_high_score = int(high_score_file.read())

            self.tutorial.run()
            self.tutorial.player.tutorial_mode = True
            # images
            self.screen.blit(self.tutorial_coin_image, (screen_width // 6, screen_height // 1.22))
            self.screen.blit(self.tutorial_space_key_image, (screen_width // 1.3, screen_height // 1.2))
            self.screen.blit(self.tutorial_lshift_key_image, (screen_width // 2, screen_height // 1.2))

            self.screen.blit(self.tutorial_w_key_image, (screen_width // 1.55, screen_height // 1.26))
            self.screen.blit(self.tutorial_a_key_image, (screen_width // 1.63, screen_height // 1.2))
            self.screen.blit(self.tutorial_s_key_image, (screen_width // 1.55, screen_height // 1.2))
            self.screen.blit(self.tutorial_d_key_image, (screen_width // 1.48, screen_height // 1.2))

            # text
            self.screen.blit(self.tutorial_health_txt, (screen_width // 14, screen_height // 8))
            self.screen.blit(self.tutorial_stamina_txt, (screen_width // 14, screen_height // 5))
            self.screen.blit(self.tutorial_point_txt_1, (screen_width // 2, screen_height // 8))
            self.screen.blit(self.tutorial_point_txt_2, (screen_width // 2, screen_height // 6))

            self.screen.blit(self.tutorial_coin_txt, (screen_width // 20, screen_height // 1.1))
            self.screen.blit(self.tutorial_controls_txt, (screen_width // 2, screen_height // 1.1))



        if not self.tutorial.level_active and not self.in_menu:  # after tutorial explanation ends, start tutorial maze
            self.tutorial_maze.run()
            self.tutorial_maze.player.tutorial_mode = True
            self.screen.blit(self.tutorial_objective_txt,
                             (screen_width // 2 - self.tutorial_objective_txt.get_width() // 2, screen_height // 1.2))

            self.screen.blit(self.tutorial_death_txt,
                             (screen_width // 2 - self.tutorial_death_txt.get_width() // 2, screen_height // 1.1))

            self.tutorial_on = False  # tutorial set to not be on


        if not self.tutorial.level_active and self.in_menu == False and not self.tutorial_maze.level_active:  # when you reach the end of the tutorial maze
            self.tutorial = Level(tutorial)  # resets tutorial after its beaten
            self.tutorial_maze = Level(tutorial_maze_list)
            self.in_menu = True  # user goes back to the menu

            # makes sure high score doesn't change as a result of the tutorial
            #with open("high_score.txt", "w") as high_score_file:
            #    high_score_file.write(str(self.real_high_score))



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
                self.all_levels[0].run()  # runs the first level

            self.run_tutorial()  # runs tutorial when needed

            if self.in_menu == True:
                print("in menu")
                self.menu()

            for i in range(self.num_of_levels-1):  # runs the rest of the levels
                self.run_levels(self.all_levels[i+1], self.all_levels[i])

            # after all levels, plays the boss level
            self.run_levels(self.boss_level, self.all_levels[self.num_of_levels-1])


            if not self.in_menu and not self.boss_level.level_active:  # when you reach the end of the maze
                self.boss_level.player.get_high_score()
                self.create_levels()  # resets all levels
                self.boss_level = Level(boss_arena)  # resets the boss fight
                self.in_menu = True

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

            self.screen.blit(self.logo_image,
                             (screen_width // 2 - self.logo_image.get_width() // 2, screen_height // 2 - self.logo_image.get_height() // 2))

            title = font.render("Amaz'd", 1, white)
            self.screen.blit(title, (screen_width//2 - title.get_width() // 2, screen_height//20))

            menu_txt = font.render("Main Menu", 1, white)
            self.screen.blit(menu_txt, (screen_width//2 - menu_txt.get_width() // 2, screen_height//5))

            # high score text
            with open("high_score.txt", "r") as high_score_file:  # reads the file for the high score
                self.high_score = int(high_score_file.read())

            high_score_txt = high_score_font.render(f"High Score: {self.high_score}", 1, white)
            self.screen.blit(high_score_txt, (screen_width // 2 - high_score_txt.get_width() // 2, screen_height // 1.2))



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

            # reset high score button
            self.reset_score_white = pygame.image.load("../Graphics/menu/high_score_white.png")
            self.reset_score_yellow = pygame.image.load("../Graphics/menu/high_score_yellow.png")
            self.reset_score_pos = (screen_width // 10, screen_height // 1.25)

            self.reset_score_option = OptionPress(self.reset_score_white, self.reset_score_yellow, self.reset_score_pos)
            self.reset_score_option.draw(pygame.display.get_surface())

            if self.reset_score_option.pressed:
                with open("high_score.txt", "w") as high_score_file:
                    high_score_file.write("0")


            # play menu text
            self.play_txt_white = pygame.image.load("../Graphics/menu/play_white.png")
            self.play_txt_yellow = pygame.image.load("../Graphics/menu/play_yellow.png")
            self.play_txt_pos = (screen_width//10, screen_height//2.7)

            self.play_option = OptionPress(self.play_txt_white, self.play_txt_yellow, self.play_txt_pos)
            self.play_option.draw(pygame.display.get_surface())

            if self.play_option.pressed == True:  # plays the game if "play" pressed
                menu_music.stop()
                enter_maze_sound.play()
                self.game_on = True
                self.in_menu = False
                print("PRESSED GAME")

            # tutorial code
            self.tutorial_txt_white = pygame.image.load("../Graphics/menu/tutorial_white.png")
            self.tutorial_txt_yellow = pygame.image.load("../Graphics/menu/tutorial_yellow.png")
            self.tutorial_txt_pos = (screen_width//10, screen_height//1.93)

            self.tutorial_option = OptionPress(self.tutorial_txt_white, self.tutorial_txt_yellow, self.tutorial_txt_pos)
            self.tutorial_option.draw(pygame.display.get_surface())

            if self.tutorial_option.pressed == True:
                menu_music.stop()
                enter_maze_sound.play()
                self.tutorial_on = True
                self.in_menu = False
                print("PRESSED TUTORIAL")



            # quit menu text
            self.quit_txt_white = pygame.image.load("../Graphics/menu/quit_white.png")
            self.quit_txt_yellow = pygame.image.load("../Graphics/menu/quit_yellow.png")
            self.quit_txt_pos = (screen_width//10, screen_height//1.5)

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


# ITENARY
# boss fights
# endless mode
# game over screen
# load levels as they are needed
