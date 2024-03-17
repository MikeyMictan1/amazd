import pygame
import sys

import customlevels as cust_lvl
import gamechange as g_change
import globalfunctions as gf
import ingamemenus as ig_menu
import mainmenu as mn_menu
import maze as mz
import mazelevel as mz_lvl
import tutorial as tutor


class Amazd:
    def __init__(self):
        pygame.init()
        # initial setup
        self.__screen = pygame.display.set_mode((gf.screen_width, gf.screen_height))
        pygame.display.set_caption("Amaz'd")
        self.__clock = pygame.time.Clock()
        self.__first_run = True
        self.__num_of_levels = gf.number_of_levels

        # --- LEVEL INITIALISATION ---
        self.__tutorial_maze = mz.DepthFirstMaze(13, 13)
        self.__tutorial_maze_list = self.__tutorial_maze.create_maze()
        self.__tutorial_maze = tutor.TutorialLevel(self.__tutorial_maze_list)
        self.__tutorial = tutor.TutorialLevel(cust_lvl.tutorial)
        self.__boss_level = mz_lvl.MazeLevel(cust_lvl.boss_arena)
        self.__create_levels()

        # --- MENUS INITIALISATION ---
        self.__main_menu = mn_menu.MainMenu()
        self.__in_game_menu = ig_menu.InGameMenu()
        self.__controls_menu = ig_menu.ControlsMenu()
        self.__game_win = g_change.GameWin()
        self.__game_over = g_change.GameOver()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # in-game menu
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_TAB or event.key == pygame.K_ESCAPE):
                    self.__in_game_menu.run_menu()

                if event.type == pygame.KEYDOWN and (event.key == pygame.K_c):
                    self.__controls_menu.run_menu()

            self.__screen.fill("black")

            # --- PLAYS LEVELS ---
            self.__play_levels()

            # --- CHECKS IF IN MAIN MENU ---
            if self.__main_menu.in_menu:
                self.__first_run = True
                self.__main_menu.menu()

            # --- CHECKS IF IN GAME MENU ---
            if self.__in_game_menu.in_game_menu_state:  # if we open the in game menu by pressing ESC
                self.__handle_in_game_menu()

            # --- IN CONTROLS MENU ---
            if self.__controls_menu.in_game_menu_state:  # Handling controls menu
                self.__handle_controls_menu()

            pygame.display.update()
            self.__clock.tick(gf.FPS)

    def __reset_levels(self):  # resets all levels, to be played again
        self.__main_menu.game_on = False
        self.__boss_level = mz_lvl.MazeLevel(cust_lvl.boss_arena)
        self.__create_levels()
        self.__reset_menus()

    def __reset_tutorial(self):  # resets the tutorial, to be played again
        self.__main_menu.tutorial_on = False
        self.__tutorial_maze = tutor.TutorialLevel(self.__tutorial_maze_list)
        self.__tutorial = tutor.TutorialLevel(cust_lvl.tutorial)
        self.__reset_menus()

    def __reset_menus(self):  # resets all menus, to be used again
        self.__main_menu.in_menu = True
        self.__first_run = True
        self.__in_game_menu.__escape_counter = 0
        self.__controls_menu.__escape_counter = 0

    def __handle_in_game_menu(self):
        # if we are in the controls menu when we try to access in game menu, close the controls menu
        if self.__controls_menu.in_game_menu_state:
            self.__controls_menu.in_game_menu_state = False
            self.__controls_menu.escape_counter += 1

        if self.__in_game_menu.display_menu():
            # recreates all levels and returns us to the menu
            self.__reset_levels()
            self.__reset_tutorial()

    def __handle_controls_menu(self):  # displays the controls menu
        self.__controls_menu.display_menu()

    def __handle_tutorials(self):
        if self.__main_menu.tutorial_on:  # runs the game tutorial
            self.__run_tutorial(self.__tutorial)
            self.__tutorial.tutorial_hud()  # hud

        if not self.__tutorial.is_active:  # after tutorial explanation ends, start tutorial maze
            self.__run_tutorial(self.__tutorial_maze)
            self.__tutorial_maze.tutorial_two_hud()  # hud
            self.__main_menu.tutorial_on = False  # closes first tutorial

        if not self.__tutorial_maze.is_active:  # when you reach the end of the tutorial maze
            self.__reset_tutorial()

    def __run_tutorial(self, tutorial_type):
        tutorial_type.run_level()
        self.__check_game_over(tutorial_type)
        tutorial_type.character.tutorial_mode = True

    def __create_levels(self):  # creates all the levels to play (customize later)
        self.all_mazes = []
        self.all_levels = []

        maze_width = 7
        maze_height = 7

        for level_num in range(self.__num_of_levels):
            if level_num % 2 == 0:
                maze_height += level_num  # makes the mazes bigger every 2 levels by adding "i", so 7 7, 9 9, 13 13, etc
                maze_width += level_num
            depth_first_maze = mz.DepthFirstMaze(maze_width, maze_height)
            self.all_mazes.append(depth_first_maze.create_maze())
            self.all_levels.append(mz_lvl.MazeLevel(self.all_mazes[level_num]))

    def __load_levels(self, current_level, previous_level):  # loads and runs a level
        # --- If previous level is not active, and current level is active then run the current level ---
        if not previous_level.is_active and current_level.is_active:
            self.__main_menu.game_on = False
            current_level.run_level()
            self.__check_game_over(current_level)
            #  --- if this is the first loop of this function for the current level, then carryover player data ---
            if self.__first_run:
                current_level.character_level_carryover(previous_level.character.points, previous_level.character.health
                                                        , previous_level.character.level_number)

                self.__first_run = False  # makes sure all other loops of the function don't carry over player data

            if not current_level.is_active:  # if the game isn't active, set first run to true again for the next level
                self.__first_run = True

    def __play_levels(self):
        self.__handle_tutorials()  # runs tutorial when needed

        # --- RUNS FIRST LEVEL ---
        if self.__main_menu.game_on:
            self.all_levels[0].run_level()
            self.__check_game_over(self.all_levels[0])

        # --- RUNS THE REST OF THE LEVELS ---
        for level_num in range(self.__num_of_levels - 1):
            self.__load_levels(self.all_levels[level_num + 1], self.all_levels[level_num])

        # --- RUNS THE FINAL LEVEL ---
        self.__load_levels(self.__boss_level, self.all_levels[self.__num_of_levels - 1])
        self.__check_game_over(self.__boss_level)

        # --- PLAYER HAS WON THE GAME ---
        if not self.__boss_level.is_active:  # when you reach the end of the maze
            self.__boss_level.character.get_high_score()
            self.__game_win.run(self.__boss_level.character.points)
            self.__game_win = g_change.GameWin()
            self.__reset_levels()

    def __check_game_over(self, current_level):  # checks if we need to go into the game over menu
        if current_level.character.health <= 0 or current_level.character.points <= 0:
            self.__game_over.run(current_level.character.points)

            if not self.__game_over.game_over_state:
                if current_level.level_type == "tutorial":
                    self.__reset_tutorial()

                else:
                    self.__reset_levels()

                self.__game_over = g_change.GameOver()


amazd = Amazd()
amazd.run()
