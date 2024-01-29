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
from gamewin import GameWin

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
        self.tutorial.level_type = "tutorial"

        self.tutorial_maze = Level(tutorial_maze_list)
        self.tutorial_maze.level_type = "tutorial"

        self.boss_level = Level(boss_arena)

        self.game_on = False
        self.tutorial_on = False
        self.in_menu = True
        self.first_run = True
        self.num_of_levels = 2

        self.create_levels()

        # tutorial text and graphics
        self.tutorial_coin_txt = tutorial_font.render("Coin (pickup for 20 points)", 1, white)
        self.tutorial_stamina_txt = tutorial_font.render("Stamina bar (sprint)", 1, white)
        self.tutorial_point_txt_1 = tutorial_font.render("Points (start at 500, they go down as time", 1, white)
        self.tutorial_point_txt_2 = tutorial_font.render("passes, coins and enemy hits increase points)", 1, white)
        self.tutorial_point_txt_3 = tutorial_font.render("Press 'C' to see all controls, press again to close menu", 1, white)
        self.tutorial_health_txt = tutorial_font.render("Health Bar (Enemies can attack to lower it)", 1, white)
        self.tutorial_objective_txt = tutorial_font.render(
            "REACH THE PORTAL AT THE END OF THE MAZE WITH AS MANY POINTS AS POSSIBLE!", 1, white)
        self.tutorial_death_txt = tutorial_font.render(
            "RUNNING OUT OF HEARTS ENDS THE GAME", 1, white)

        self.tutorial_coin_image = pygame.image.load(f"../Graphics/powerups/coin.png").convert_alpha()
        self.tutorial_coin_image = pygame.transform.scale(self.tutorial_coin_image, (70, 70))



        # self.log
        self.logo_image = pygame.image.load(f"../Graphics/amazd_logo.png")
        pygame.display.set_icon(self.logo_image)
        self.logo_image = pygame.transform.scale(self.logo_image, (140, 280))

        self.game_win = GameWin()  # checks for game win

        # --- IN GAME MENU ---
        self.in_game_menu = False
        # menu text
        self.in_game_menu_txt = font.render("IN-GAME MENU", 1, white)

        self.menu_txt_white = pygame.image.load("../Graphics/gameover/menu_white.png")
        self.menu_txt_yellow = pygame.image.load("../Graphics/gameover/menu_yellow.png")
        self.menu_txt_pos = (screen_width // 2 - self.menu_txt_white.get_width()//2, screen_height // 2.6)
        self.menu_option = OptionPress(self.menu_txt_white, self.menu_txt_yellow, self.menu_txt_pos)

        self.continue_txt_white = pygame.image.load("../Graphics/ingamemenu/continue_white.png")
        self.continue_txt_yellow = pygame.image.load("../Graphics/ingamemenu/continue_yellow.png")
        self.continue_txt_pos = (screen_width // 2 - self.continue_txt_white.get_width()//2, screen_height // 1.75)
        self.continue_option = OptionPress(self.continue_txt_white, self.continue_txt_yellow, self.continue_txt_pos)

        self.quit_white = pygame.image.load("../Graphics/menu/quit_white.png")
        self.quit_yellow = pygame.image.load("../Graphics/menu/quit_yellow.png")
        self.quit_pos = (screen_width // 2 - self.quit_white.get_width()//2, screen_height // 1.3)
        self.quit_ingame_option = OptionPress(self.quit_white, self.quit_yellow, self.quit_pos)

        self.menu_overlay = pygame.image.load("../Graphics/ingamemenu/menu_overlay.png")
        self.menu_overlay = pygame.transform.scale(self.menu_overlay, (1100,800))

        self.escape_counter = 0

        # --- CONTROLS MENU ---
        self.in_controls_menu = False
        self.controls_counter = 0

        self.control_set_image = pygame.image.load("../Graphics/controls/control_set.png")
        self.control_set_image = pygame.transform.scale(self.control_set_image, (500,600))

    def run_tutorial(self):
        if self.tutorial_on:  # runs the game tutorial

            #with open("high_score.txt", "r+") as high_score_file:  # if file is empty, set score to 0
            #    if high_score_file.read() == "":
            #        high_score_file.write("0")

            #with open("high_score.txt", "r") as high_score_file:  # reads the file for the high score
            #    self.real_high_score = int(high_score_file.read())

            self.tutorial.run()
            self.check_game_over(self.tutorial)

            self.tutorial.player.tutorial_mode = True
            # images
            self.screen.blit(self.tutorial_coin_image, (screen_width // 2-self.tutorial_coin_image.get_width()//2, screen_height // 1.13))
            self.screen.blit(self.tutorial_coin_txt, (screen_width // 2 - self.tutorial_coin_txt.get_width() // 2, screen_height // 1.03))

            # text
            self.screen.blit(self.tutorial_health_txt, (screen_width // 14, screen_height // 8))
            self.screen.blit(self.tutorial_stamina_txt, (screen_width // 14, screen_height // 5))
            self.screen.blit(self.tutorial_point_txt_1, (screen_width // 2, screen_height // 8))
            self.screen.blit(self.tutorial_point_txt_2, (screen_width // 2, screen_height // 6))
            self.screen.blit(self.tutorial_point_txt_3, (screen_width // 2 - self.tutorial_point_txt_3.get_width()//2, screen_height // 1.2))




        if not self.tutorial.level_active and not self.in_menu:  # after tutorial explanation ends, start tutorial maze
            self.tutorial_maze.run()
            self.check_game_over(self.tutorial_maze)
            self.tutorial_maze.player.tutorial_mode = True
            self.screen.blit(self.tutorial_objective_txt,
                             (screen_width // 2 - self.tutorial_objective_txt.get_width() // 2, screen_height // 1.2))

            self.screen.blit(self.tutorial_death_txt,
                             (screen_width // 2 - self.tutorial_death_txt.get_width() // 2, screen_height // 1.1))

            self.tutorial_on = False  # tutorial set to not be on


        if not self.tutorial.level_active and self.in_menu == False and not self.tutorial_maze.level_active:  # when you reach the end of the tutorial maze
            self.tutorial = Level(tutorial)  # resets tutorial after its beaten
            self.tutorial.level_type = "tutorial"
            self.tutorial_maze = Level(tutorial_maze_list)
            self.tutorial_maze.level_type = "tutorial"
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
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_TAB or event.key == pygame.K_ESCAPE):
                    print("tryna escape")
                    self.escape_counter += 1
                    self.in_game_menu = True

                if event.type == pygame.KEYDOWN and (event.key == pygame.K_c):
                    self.controls_counter += 1
                    self.in_controls_menu = True
                    print("tryna see controls")


            self.screen.fill("black")


            if self.game_on == True:
                self.all_levels[0].run()  # runs the first level
                self.check_game_over(self.all_levels[0])


            self.run_tutorial()  # runs tutorial when needed

            if self.in_menu == True:
                print("in menu")
                self.menu()

            for i in range(self.num_of_levels-1):  # runs the rest of the levels
                self.run_levels(self.all_levels[i+1], self.all_levels[i])

            # after all levels, plays the boss level
            self.run_levels(self.boss_level, self.all_levels[self.num_of_levels-1])
            self.check_game_over(self.boss_level)


            if not self.in_menu and not self.boss_level.level_active:  # when you reach the end of the maze
                print("player won the game")
                self.escape_counter = 0
                self.controls_counter = 0
                self.game_win.run(self.boss_level.player.points)
                self.game_win = GameWin()

                self.boss_level.player.get_high_score()
                self.create_levels()  # resets all levels
                self.boss_level = Level(boss_arena)  # resets the boss fight
                self.in_menu = True



            if self.in_game_menu:  # if we open the in game menu by pressing ESC
                # if we are in the controls menu when we try to access in game menu, close the controls menu
                if self.in_controls_menu:
                    self.in_controls_menu = False
                    self.controls_counter += 1

                if self.escape_counter % 2 == 0:  # makes sure esc will open AND close the in game menu
                    self.in_game_menu = False

                self.screen.blit(self.menu_overlay, (screen_width // 2 - self.menu_overlay.get_width()//2 , screen_height // 2 - self.menu_overlay.get_height()//2))
                self.screen.blit(self.in_game_menu_txt,
                                 (screen_width // 2 - self.in_game_menu_txt.get_width() // 2, screen_height // 10))

                self.menu_option.draw(pygame.display.get_surface())
                self.continue_option.draw(pygame.display.get_surface())
                self.quit_ingame_option.draw(pygame.display.get_surface())

                if self.menu_option.pressed == True:
                    self.escape_counter += 1
                    # recreates all levels and returns us to the menu
                    self.tutorial_on = False
                    self.game_on = False
                    self.menu_option.pressed = False
                    self.in_game_menu = False
                    self.tutorial_maze = Level(tutorial_maze_list)
                    self.tutorial = Level(tutorial)
                    self.boss_level = Level(boss_arena)
                    self.create_levels()
                    self.in_menu = True
                    print("did we get here?")

                if self.continue_option.pressed:
                    self.escape_counter += 1
                    self.in_game_menu = False
                    self.continue_option.pressed = False

                if self.quit_ingame_option.pressed == True:  # quits the game if "quit" is pressed
                    pygame.quit()
                    sys.exit()

            if self.in_controls_menu:  # Handling controls menu
                if self.controls_counter % 2 == 0:
                    self.in_controls_menu = False
                self.screen.blit(self.menu_overlay, (screen_width // 2 - self.menu_overlay.get_width() // 2,
                                                     screen_height // 2 - self.menu_overlay.get_height() // 2))

                self.screen.blit(self.control_set_image, (screen_width // 2 - self.control_set_image.get_width() // 2,
                                                     screen_height // 2 - self.control_set_image.get_height() // 2))




            pygame.display.update()
            self.clock.tick(FPS)

    def check_game_over(self, current_level):
        if not current_level.game_over_active:
            # resets all levels
            if current_level.level_type == "tutorial":
                self.tutorial_on = False
                self.tutorial_maze = Level(tutorial_maze_list)
                self.tutorial = Level(tutorial)

            else:
                self.boss_level = Level(boss_arena)
                self.create_levels()

            self.game_on = False
            self.in_menu = True  # places user in the menu

    def run_levels(self, current_level, previous_level):  # currently does nothing
        if not previous_level.level_active and current_level.level_active:  # if previous level is not active, and current level is active then run the current level
            self.game_on = False
            current_level.run()
            self.check_game_over(current_level)

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
                maze_height += i  # makes the mazes bigger every 2 levels by an addition of "i", so 7 7, 9 9, 13 13, etc
                maze_width += i
            depth_first_maze = df_maze_generation(maze_width, maze_height)
            depth_first_maze.main_code()
            self.all_mazes.append(depth_first_maze.create_maze())
            self.all_levels.append(Level(self.all_mazes[i]))



    # code for starting menu
    def menu(self):
        # initialising needed variables
        pygame.mixer.stop()

        frame = 0
        frame_speed = 0.1
        menu_music = pygame.mixer.Sound("../Audio/maze_music.mp3")
        self.maze_music = pygame.mixer.Sound("../Audio/in_maze_music.mp3")  # undertale
        menu_music.play(999)
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
                self.maze_music.play(999)
                self.maze_music.set_volume(0.05)
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
                self.maze_music.play()
                self.maze_music.set_volume(0.05)
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
# load levels as they are needed
