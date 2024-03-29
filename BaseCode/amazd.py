import pygame

import customlevels as cust_lvl
import gamechange as g_change
import globalfunctions as gf
import ingamemenus as ig_menu
import mainmenu as mn_menu
import maze as mz
import mazelevel as mz_lvl
import tutorial as tutor


class Amazd:
    """
    Description:
        The main game class of Amazd, acts as the class that runs the entire game.
        Will handle menus, and create level objects.

    Attributes:
        __screen (pygame.Surface): The screen surface for which the entire game is written onto
        __clock (pygame.time.Clock): Clock object that controls the frame rate of the game
        __first_run (bool): flag variable that indicates if a level is in the game loop for the first time
        __num_of_levels (int): The number of normal levels the player will have to go through in the game
        __in_game (bool): boolean value for if the game is currently running

        __tutorial (tutor.TutorialLevel): creates the custom maze for the tutorials first level
        __tutorial_maze (mz.DepthFirstMaze): Creates the dfs maze for the tutorials second level
        __boss_level (mz_lvl.MazeLevel): creates the custom maze for the boss level
        __all_levels (list): A list of all the regular maze levels

        __main_menu (mn_menu.MainMenu): creates the object for the main menu
        __in_game_menu (ig_menu.InGameMenu): creates the object for the in game menu
        __controls_menu (ig_menu.ControlsMenu): creates the object for the controls menu
        __game_win (g_change.GameWin): creates the object for the game win menu
        __game_over (g_change.GameOver): creates the object for the game over menu
    """

    def __init__(self):
        """
        Description:
            Initialisation function for the Amazd class. Initialises pygame, levels and all the menus.
        """
        pygame.init()
        # initial setup
        self.__screen = pygame.display.set_mode((gf.screen_width, gf.screen_height))
        pygame.display.set_caption("Amaz'd")
        self.__clock = pygame.time.Clock()
        self.__first_run = True
        self.__num_of_levels = gf.number_of_levels
        self.__in_game = True

        # --- LEVEL INITIALISATION ---
        self.__tutorial_maze = mz.DepthFirstMaze(13, 13)
        self.__tutorial_maze = tutor.TutorialLevel(self.__tutorial_maze.create_maze())
        self.__tutorial = tutor.TutorialLevel(cust_lvl.tutorial)
        self.__boss_level = mz_lvl.MazeLevel(cust_lvl.boss_arena)
        self.__all_levels = self.__create_levels()

        # --- MENUS INITIALISATION ---
        self.__main_menu = mn_menu.MainMenu()
        self.__in_game_menu = ig_menu.InGameMenu()
        self.__controls_menu = ig_menu.ControlsMenu()
        self.__game_win = g_change.GameWin()
        self.__game_over = g_change.GameOver()

    def run(self):
        """
        Description:
            Is the public method that will run the game loop.

            Checks if levels, menu, in-game menu or controls menu need to be played, and checks for pygame events
            such as keyboard inputs.
            Draws the pygame display onto the screen 60 times per second.
        """
        while self.__in_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.__in_game = False

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

    def __reset_levels(self):
        """
        Description:
            Randomly regenerates all levels, to be played again
        """
        self.__main_menu.game_on = False  # makes sure the game is not on before resetting all levels
        self.__boss_level = mz_lvl.MazeLevel(cust_lvl.boss_arena)
        self.__all_levels = self.__create_levels()
        self.__reset_menus()

    def __reset_tutorial(self):
        """
        Description:
            Randomly regenerates the tutorial levels, to be played again
        """
        self.__main_menu.tutorial_on = False
        self.__tutorial_maze = mz.DepthFirstMaze(13, 13)
        self.__tutorial_maze = tutor.TutorialLevel(self.__tutorial_maze.create_maze())
        self.__tutorial = tutor.TutorialLevel(cust_lvl.tutorial)
        self.__reset_menus()

    def __reset_menus(self):
        """
        Description:
            Resets all menus, to be played again
        """
        self.__main_menu.in_menu = True
        self.__first_run = True
        self.__in_game_menu.__escape_counter = 0
        self.__controls_menu.__escape_counter = 0

    def __handle_in_game_menu(self):
        """
        Description:
            Displays the in-game menu on the screen.
            Checks if the in-game menu is opened while the controls menu is open, and closes the controls menu if so.
            Checks if the menu option was pressed in the in-game menu, and resets all levels if so.
          """
        # if we are in the controls menu when we try to access in game menu, close the controls menu
        if self.__controls_menu.in_game_menu_state:
            self.__controls_menu.in_game_menu_state = False
            self.__controls_menu.escape_counter += 1

        if self.__in_game_menu.display_menu():
            # recreates all levels and returns us to the menu
            self.__reset_levels()
            self.__reset_tutorial()

    def __handle_controls_menu(self):
        """
        Description:
            Displays the controls menu on the screen.
        """
        self.__controls_menu.display_menu()

    def __handle_tutorials(self):
        """
        Description:
            Runs the tutorial when pressed in the menu.
            Checks if the first tutorial is beat, if so, run the second tutorial.
            Resets all tutorials once the tutorial is beaten.
          """
        if self.__main_menu.tutorial_on:  # runs the game tutorial
            self.__run_tutorial(self.__tutorial)
            self.__tutorial.tutorial_hud()  # hud

        if not self.__tutorial.is_active:  # after tutorial explanation ends, start tutorial maze
            self.__run_tutorial(self.__tutorial_maze)
            self.__tutorial_maze.tutorial_two_hud()  # hud
            self.__main_menu.tutorial_on = False  # closes first tutorial

        if not self.__tutorial_maze.is_active:  # when you reach the end of the tutorial maze
            self.__reset_tutorial()

    def __run_tutorial(self, tutorial_type: mz_lvl.MazeLevel):
        """
        Description:
            Runs an individual tutorial level

        Parameters:
            tutorial_type (mz_lvl.MazeLevel): The maze level object representing the tutorial level
        """
        tutorial_type.run_level()
        self.__check_game_over(tutorial_type)
        tutorial_type.character.tutorial_mode = True

    def __create_levels(self):
        """
        Description:
            Creates all the depth-first mazes and translates them into pygame. All mazes added to the "all_levels"
            list.
            Mazes generated to get progressively more difficult as the player progresses through the game.

        Returns:
            all_levels_list (list): a list of all the regular maze levels
        """
        self.all_mazes = []
        self.all_levels_list = []

        maze_width = 7
        maze_height = 7

        for level_num in range(self.__num_of_levels):
            if level_num % 2 == 0:
                maze_height += level_num  # makes the mazes bigger every 2 levels by adding "i", so 7 7, 9 9, 13 13, etc
                maze_width += level_num
            depth_first_maze = mz.DepthFirstMaze(maze_width, maze_height)
            self.all_mazes.append(depth_first_maze.create_maze())
            self.all_levels_list.append(mz_lvl.MazeLevel(self.all_mazes[level_num]))

        return self.all_levels_list

    def __load_levels(self, current_level: mz_lvl.MazeLevel, previous_level: mz_lvl.MazeLevel):
        """
        Description:
            Loads and runs the current level, carries over player data from the previous data to the current level.
        """
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
        """
        Description:
            Plays all levels. Checks if the tutorial is being played, or if the main game is being played.
            Resets all levels once the game is beaten.
        """
        self.__handle_tutorials()  # runs tutorial when needed

        # --- RUNS FIRST LEVEL ---
        if self.__main_menu.game_on:
            self.__all_levels[0].run_level()
            self.__check_game_over(self.__all_levels[0])

        # --- RUNS THE REST OF THE LEVELS ---
        for level_num in range(self.__num_of_levels - 1):
            self.__load_levels(self.__all_levels[level_num + 1], self.__all_levels[level_num])

        # --- RUNS THE FINAL LEVEL ---
        self.__load_levels(self.__boss_level, self.__all_levels[self.__num_of_levels - 1])
        self.__check_game_over(self.__boss_level)

        # --- PLAYER HAS WON THE GAME ---
        if not self.__boss_level.is_active:  # when you reach the end of the maze
            self.__boss_level.character.get_high_score()
            self.__game_win.run(self.__boss_level.character.points)
            self.__game_win = g_change.GameWin()
            self.__reset_levels()

    def __check_game_over(self, current_level: mz_lvl.MazeLevel):  # checks if we need to go into the game over menu
        """
        Description:
            Displays the game over screen once the character dies.

        Parameters:
            current_level (mz_lvl.MazeLevel): The current maze level that the player is playing in.
        """
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
