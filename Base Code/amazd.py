import pygame, sys, os
from mazelevel import MazeLevel
from globalfunctions import *
from maze import *
from customlevels import tutorial, boss_arena
from gamechange import GameWin
from main_menu import MainMenu
from ingamemenus import InGameMenu, ControlsMenu
from tutorial import TutorialClass

# ----------------------------------------
class Amazd:
    def __init__(self):
        pygame.init()
        # initial setup
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Amaz'd")
        self.clock = pygame.time.Clock()
        self.first_run = True
        self.num_of_levels = 3

        # --- LEVEL INITIALISATION ---
        self.tutorial_maze = DepthFirstMaze(13, 13)
        self.tutorial_maze_list = self.tutorial_maze.create_maze()
        self.tutorial = TutorialClass(tutorial)
        self.tutorial_maze = TutorialClass(self.tutorial_maze_list)
        self.boss_level = MazeLevel(boss_arena)
        self.create_levels()

        # --- MENUS INITIALISATION ---
        self.main_menu = MainMenu()
        self.in_game_menu = InGameMenu()
        self.controls_menu = ControlsMenu()
        self.game_win = GameWin()
        self.in_game_menu_sound = pygame.mixer.Sound("../Audio/open_maze_menu1.mp3")


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # in-game menu
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_TAB or event.key == pygame.K_ESCAPE):
                    self.in_game_menu_sound.play()
                    self.in_game_menu_sound.set_volume(0.1)
                    self.in_game_menu.escape_counter += 1
                    self.in_game_menu.in_game_menu_state = True

                if event.type == pygame.KEYDOWN and (event.key == pygame.K_c):
                    self.in_game_menu_sound.play()
                    self.in_game_menu_sound.set_volume(0.1)
                    self.controls_menu.controls_counter += 1
                    self.controls_menu.in_controls_menu_state = True

            self.screen.fill("black")

            # --- CHECKS IF IN MAIN MENU ---
            if self.main_menu.in_menu:
                self.main_menu.menu()

            self.play_levels()

            # --- CHECKS IF IN GAME MENU ---
            if self.in_game_menu.in_game_menu_state:  # if we open the in game menu by pressing ESC
                self.handle_in_game_menu()

            # --- IN CONTROLS MENU ---
            if self.controls_menu.in_controls_menu_state:  # Handling controls menu
                self.handle_controls_menu()

            pygame.display.update()
            self.clock.tick(FPS)


    def reset_levels(self):
        self.main_menu.tutorial_on = False
        self.main_menu.game_on = False
        self.main_menu.in_menu = True
        self.tutorial_maze = TutorialClass(self.tutorial_maze_list)
        self.tutorial = TutorialClass(tutorial)
        self.boss_level = MazeLevel(boss_arena)
        self.create_levels()


    def handle_in_game_menu(self):
        # if we are in the controls menu when we try to access in game menu, close the controls menu
        if self.controls_menu.in_controls_menu_state:
            self.controls_menu.in_controls_menu_state = False
            self.controls_menu.controls_counter += 1

        self.in_game_menu.game_change_buttons()

        if self.in_game_menu.menu_option.pressed == True:
            self.in_game_menu.escape_counter += 1
            self.in_game_menu.menu_option.pressed = False
            self.in_game_menu.in_game_menu_state = False
            # recreates all levels and returns us to the menu
            self.reset_levels()

        if self.in_game_menu.continue_option.pressed:
            self.in_game_menu.escape_counter += 1
            self.in_game_menu.in_game_menu_state = False
            self.in_game_menu.continue_option.pressed = False

        if self.in_game_menu.quit_option.pressed == True:  # quits the game if "quit" is pressed
            pygame.quit()
            sys.exit()


    def handle_controls_menu(self):
        self.controls_menu.game_change_buttons()


    def handle_tutorial(self):
        if self.main_menu.tutorial_on:  # runs the game tutorial
            self.tutorial.run_level()
            self.check_game_over(self.tutorial)
            self.tutorial.character.tutorial_mode = True
            # hud
            self.tutorial.tutorial_hud()

        if not self.tutorial.level_active and not self.main_menu.in_menu:  # after tutorial explanation ends, start tutorial maze
            self.tutorial_maze.run_level()
            self.check_game_over(self.tutorial_maze)
            self.tutorial_maze.character.tutorial_mode = True
            # hud
            self.tutorial_maze.tutorial_two_hud()

            self.main_menu.tutorial_on = False  # closes first tutorial

        if not self.tutorial.level_active and not self.main_menu.in_menu and not self.tutorial_maze.level_active:  # when you reach the end of the tutorial maze
            self.tutorial = TutorialClass(tutorial)  # resets tutorial after its beaten
            self.tutorial_maze = TutorialClass(self.tutorial_maze_list)
            self.main_menu.in_menu = True  # user goes back to the menu


    def create_levels(self):  # creates all the levels to play (customize later)
        self.all_mazes = []
        self.all_levels = []

        maze_width = 7
        maze_height = 7

        for i in range(self.num_of_levels):
            if i % 2 == 0:
                maze_height += i  # makes the mazes bigger every 2 levels by an addition of "i", so 7 7, 9 9, 13 13, etc
                maze_width += i
            depth_first_maze = DepthFirstMaze(maze_width, maze_height)
            self.all_mazes.append(depth_first_maze.create_maze())
            self.all_levels.append(MazeLevel(self.all_mazes[i]))


    def load_levels(self, current_level, previous_level):  # currently does nothing
        if not previous_level.level_active and current_level.level_active:  # if previous level is not active, and current level is active then run the current level
            self.main_menu.game_on = False
            current_level.run_level()
            self.check_game_over(current_level)

            if self.first_run:  # if this is the first loop of this function for the current level, then carryover player data
                current_level.character_level_carryover(previous_level.character.points, previous_level.character.health,
                                                     previous_level.character.level_number)

            self.first_run = False  # makes sure all other loops of the function don't carry over player data

            if not current_level.level_active:  # if the game isn't active, set first run to true again for the next level
                self.first_run = True


    def play_levels(self):
        self.handle_tutorial()  # runs tutorial when needed

        # runs the first level
        if self.main_menu.game_on == True:
            self.all_levels[0].run_level()
            self.check_game_over(self.all_levels[0])

        for i in range(self.num_of_levels - 1):  # runs the rest of the levels
            self.load_levels(self.all_levels[i + 1], self.all_levels[i])

        # after all levels, plays the boss level
        self.load_levels(self.boss_level, self.all_levels[self.num_of_levels - 1])
        self.check_game_over(self.boss_level)

        if not self.main_menu.in_menu and not self.boss_level.level_active:  # when you reach the end of the maze
            self.in_game_menu.escape_counter = 0
            self.controls_menu.controls_counter = 0
            self.boss_level.character.get_high_score()
            self.game_win.run(self.boss_level.character.points)
            self.game_win = GameWin()

            self.reset_levels()


    def check_game_over(self, current_level):
        if not current_level.game_over_active:
            # resets all levels
            if current_level.level_type == "tutorial":
                self.main_menu.tutorial_on = False
                self.tutorial_maze = TutorialClass(self.tutorial_maze_list)
                self.tutorial = TutorialClass(tutorial)

            else:
                self.boss_level = MazeLevel(boss_arena)
                self.create_levels()

            self.main_menu.game_on = False
            self.main_menu.in_menu = True  # places user in the menu


amazd = Amazd()

while True:
    amazd.run()

