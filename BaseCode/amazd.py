import pygame, sys, os
from mazelevel import MazeLevel
from globalfunctions import *
from maze import *
from customlevels import tutorial, boss_arena
from gamechange import GameWin, GameOver
from main_menu import MainMenu
from ingamemenus import InGameMenu, ControlsMenu
from tutorial import TutorialLevel

# ----------------------------------------
class Amazd:
    def __init__(self):
        pygame.init()
        # initial setup
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Amaz'd")
        self.clock = pygame.time.Clock()
        self.first_run = True
        self.num_of_levels = 7

        # --- LEVEL INITIALISATION ---
        self.tutorial_maze = DepthFirstMaze(13, 13)
        self.tutorial_maze_list = self.tutorial_maze.create_maze()
        self.tutorial_maze = TutorialLevel(self.tutorial_maze_list)
        self.tutorial = TutorialLevel(tutorial)
        self.boss_level = MazeLevel(boss_arena)
        self.create_levels()

        # --- MENUS INITIALISATION ---
        self.main_menu = MainMenu()
        self.in_game_menu = InGameMenu()
        self.controls_menu = ControlsMenu()
        self.game_win = GameWin()
        self.game_over = GameOver()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # in-game menu
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_TAB or event.key == pygame.K_ESCAPE):
                    self.in_game_menu.run_menu()

                if event.type == pygame.KEYDOWN and (event.key == pygame.K_c):
                    self.controls_menu.run_menu()

            self.screen.fill("black")

            # --- PLAYS LEVELS ---
            self.play_levels()

            # --- CHECKS IF IN MAIN MENU ---
            if self.main_menu.in_menu:
                self.first_run = True
                self.main_menu.menu()

            # --- CHECKS IF IN GAME MENU ---
            if self.in_game_menu.in_game_menu_state:  # if we open the in game menu by pressing ESC
                self.handle_in_game_menu()

            # --- IN CONTROLS MENU ---
            if self.controls_menu.in_game_menu_state:  # Handling controls menu
                self.handle_controls_menu()

            pygame.display.update()
            self.clock.tick(FPS)

    def reset_levels(self):
        self.main_menu.game_on = False
        self.boss_level = MazeLevel(boss_arena)
        self.create_levels()
        self.reset_menus()

    def reset_tutorial(self):
        self.main_menu.tutorial_on = False
        self.tutorial_maze = TutorialLevel(self.tutorial_maze_list)
        self.tutorial = TutorialLevel(tutorial)
        self.reset_menus()

    def reset_menus(self):
        self.main_menu.in_menu = True
        self.first_run = True
        self.in_game_menu.escape_counter = 0
        self.controls_menu.escape_counter = 0

    def handle_in_game_menu(self):
        # if we are in the controls menu when we try to access in game menu, close the controls menu
        if self.controls_menu.in_game_menu_state:
            self.controls_menu.in_game_menu_state = False
            self.controls_menu.escape_counter += 1

        if self.in_game_menu.display_menu():
            # recreates all levels and returns us to the menu
            self.reset_levels()
            self.reset_tutorial()

    def handle_controls_menu(self):
        self.controls_menu.display_menu()

    def handle_tutorials(self):
        if self.main_menu.tutorial_on:  # runs the game tutorial
            self.run_tutorial(self.tutorial)
            self.tutorial.tutorial_hud()  # hud

        if not self.tutorial.is_active:  # after tutorial explanation ends, start tutorial maze
            self.run_tutorial(self.tutorial_maze)
            self.tutorial_maze.tutorial_two_hud()  # hud
            self.main_menu.tutorial_on = False  # closes first tutorial

        if not self.tutorial_maze.is_active:  # when you reach the end of the tutorial maze
            self.reset_tutorial()

    def run_tutorial(self, tutorial_type):
        tutorial_type.run_level()
        self.check_game_over(tutorial_type)
        tutorial_type.character.tutorial_mode = True

    def create_levels(self):  # creates all the levels to play (customize later)
        self.all_mazes = []
        self.all_levels = []

        maze_width = 7
        maze_height = 7

        for level_num in range(self.num_of_levels):
            if level_num % 2 == 0:
                maze_height += level_num  # makes the mazes bigger every 2 levels by adding "i", so 7 7, 9 9, 13 13, etc
                maze_width += level_num
            depth_first_maze = DepthFirstMaze(maze_width, maze_height)
            self.all_mazes.append(depth_first_maze.create_maze())
            self.all_levels.append(MazeLevel(self.all_mazes[level_num]))

    def load_levels(self, current_level, previous_level):  # currently does nothing
        if not previous_level.is_active and current_level.is_active:  # if previous level is not active, and current level is active then run the current level
            self.main_menu.game_on = False
            current_level.run_level()
            self.check_game_over(current_level)
            if self.first_run:  # if this is the first loop of this function for the current level, then carryover player data
                current_level.character_level_carryover(previous_level.character.points, previous_level.character.health,
                                                     previous_level.character.level_number)

                self.first_run = False  # makes sure all other loops of the function don't carry over player data

            if not current_level.is_active:  # if the game isn't active, set first run to true again for the next level
                self.first_run = True

    def play_levels(self):
        self.handle_tutorials()  # runs tutorial when needed

        # --- RUNS FIRST LEVEL ---
        if self.main_menu.game_on:
            self.all_levels[0].run_level()
            self.check_game_over(self.all_levels[0])

        # --- RUNS THE REST OF THE LEVELS ---
        for level_num in range(self.num_of_levels - 1):
            self.load_levels(self.all_levels[level_num + 1], self.all_levels[level_num])

        # --- RUNS THE FINAL LEVEL ---
        self.load_levels(self.boss_level, self.all_levels[self.num_of_levels - 1])
        self.check_game_over(self.boss_level)

        # --- PLAYER HAS WON THE GAME ---
        if not self.boss_level.is_active:  # when you reach the end of the maze
            self.boss_level.character.get_high_score()
            self.game_win.run(self.boss_level.character.points)
            self.game_win = GameWin()
            self.reset_levels()

    def check_game_over(self, current_level):
        if current_level.character.health <= 0 or current_level.character.points <= 0:
            self.game_over.run(current_level.character.points)

            if not self.game_over.game_over_state:
                if current_level.level_type == "tutorial":
                    self.reset_tutorial()

                else:
                    self.reset_levels()

                self.game_over = GameOver()


amazd = Amazd()
amazd.run()

