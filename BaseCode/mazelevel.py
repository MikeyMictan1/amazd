import pygame

import mazelayout as mz_lay
import globalfunctions as gf
import character as chara
import collidables as coll
import camera as cam
import enemy


class MazeLevel:
    """
    Description:
        Class that takes the depth-first created maze as a list, and "translates" it into pygame, in order to be played.

        Acts as the interface for which enemies and characters interact.

    Attributes:
        __powerup_sprites (pygame.sprite.Group): Sprite group consisting of speed powerup sprites
        __coin_sprites (pygame.sprite.Group): Sprite group consisting of coin sprites
        __health_pot_sprites (pygame.sprite.Group): Sprite group consisting of health potion sprites
        __exit_sprites (pygame.sprite.Group): Sprite group consisting of exit portal sprites
        __enemy_sprites (pygame.sprite.Group): Sprite group consisting of enemy sprites
        __sword_sprites (pygame.sprite.Group): Sprite group consisting of sword sprites
        __game_camera (pygame.sprite.Group): Sprite group consisting of the camera that the character centres around
        __wall_sprites (pygame.sprite.Group): Sprite group consisting of maze wall sprites

        is_active (bool): Flag that checks if the current maze level is active
        level_type (str): What type of level the current level is (e.g. tutorial, normal, boss)
    """
    def __init__(self, maze_list: list):
        """
        Description:
            Initialisation method for the MazeLevel class

        parameters:
            maze_list (list): The depth-first generated maze, as a list.
        """
        # sprite groups setup
        self.__powerup_sprites = pygame.sprite.Group()
        self.__coin_sprites = pygame.sprite.Group()
        self.__health_pot_sprites = pygame.sprite.Group()
        self.__exit_sprites = pygame.sprite.Group()
        self.__enemy_sprites = pygame.sprite.Group()
        self.__sword_sprites = pygame.sprite.Group()
        self.__game_camera = cam.GameCamera()
        self.__wall_sprites = pygame.sprite.Group()

        # maze creation
        self.create_pygame_maze(maze_list)

        # other setup
        self.is_active = True
        self.level_type = "normal"

    def create_pygame_maze(self, maze_lst: list):  # creates the completed pygame maze
        """
        Description:
            Creates the completed maze in pygame with sprites.

        Parameters:
            maze_lst (list): The depth-first maze as a list.
        """
        self.__maze_loop(maze_lst, self.__check_maze_layout)  # loops through the maze, putting walls, floors in place
        self.__maze_loop(maze_lst, self.__check_maze_elements)  # loops through, putting powerups, enemies etc. in place

    @staticmethod
    def __maze_loop(maze_lst: list, check_maze_cell):  # loops through every cell in the maze
        """
        Description:
        Loops through every cell of the maze, translating the cells strings into pygame sprites.

        Parameters:
            maze_lst (list): The depth-first maze as a list.
            check_maze_cell: Checks the contents of the cell. Will create a sprite at that cell position depending on
            what the cell was.
        """
        row_num = -1
        for row in maze_lst:
            row_num += 1
            col_num = -1

            for cell in row:
                col_num += 1
                position = (col_num * gf.tile_size, row_num * gf.tile_size)
                check_maze_cell(cell, position)

    def __check_maze_layout(self, cell: str, position: tuple):
        """
        Description:
        Checks a cell, and makes that cell into a wall or floor sprite, depending on what letter the cell is.

        Parameters:
            cell (list): One individual letter in the maze, that represents a sprite such as a wall, floor, etc.
            position (tuple): Position of where the sprite should be drawn onto the screen.
        """
        if cell == "X":  # if there are walls
            mz_lay.WallHidden(position, [self.__game_camera, self.__wall_sprites])
            # all the groups that belong to the sprite class

        if cell == "Y":
            mz_lay.WallVisible(position, [self.__game_camera, self.__wall_sprites])

        if cell in " PUECOSH":  # if there are floor tiles, including on the player
            self.floor = mz_lay.Floor(position, [self.__game_camera])

    def __check_maze_elements(self, cell: str, position: tuple):
        """
        Description:
        Checks a cell, and makes that cell into a character, powerup, coin, enemy, health potion or exit sprite,
        depending on what letter the cell is.

        Parameters:
            cell (list): One individual letter in the maze, that represents a sprite such as a powerup, character, etc.
            position (tuple): Position of where the sprite should be drawn onto the screen.
        """
        if cell == "P":  # if there is a player
            self.character = chara.Character(position, [self.__game_camera], self.__wall_sprites,
                                             self.__powerup_sprites,
                                             self.__coin_sprites,
                                             self.__health_pot_sprites, self.__exit_sprites, self.__sword_sprites)

        elif cell == "U":  # translates powerups from the maze into pygame
            self.powerup = coll.Powerups(position, [self.__game_camera, self.__powerup_sprites])

        elif cell == "C":  # translates coins from the maze into pygame
            self.coins = coll.Coins(position, [self.__game_camera, self.__coin_sprites])

        elif cell == "E":  # translates enemies from the maze into pygame
            self.enemy = enemy.Enemy("skeleton", position,
                                     [self.__game_camera, self.__enemy_sprites],
                                     self.__wall_sprites,
                                     self.character)

        elif cell == "S":  # translates slime enemies from the maze into pygame
            self.enemy_slime = enemy.Enemy("slime", position,
                                           [self.__game_camera, self.__enemy_sprites],
                                           self.__wall_sprites,
                                           self.character)

        elif cell == "H":  # translates health potions from the maze into pygame
            self.health_pot = coll.HealthPot(position, [self.__game_camera, self.__health_pot_sprites])

        elif cell == "O":  # translates portals from the maze into pygame
            self.exit = coll.Exit(position, [self.__game_camera, self.__exit_sprites])

    def __character_hit_enemy_check(self):
        """
        Description:
            Checks if a character has hit an enemy, if so, then the enemy should take damage.
        """
        if self.__sword_sprites:
            for attack_sprite in self.__sword_sprites:
                # list of all sprites that are colliding
                collision = pygame.sprite.spritecollide(attack_sprite, self.__enemy_sprites, False)

                if collision:
                    for enemy_sprite in collision:
                        enemy_sprite.enemy_hit(self.character)

    def run_level(self):
        """
        Description:
            Runs the completed pygame maze level, with the camera centering around the character.
        """
        self.__game_camera.draw_camera_offset(self.character)
        self.__game_camera.update()
        self.__character_hit_enemy_check()
        if not self.character.in_level:
            self.is_active = False

    def character_level_carryover(self, new_points: float, new_health: float, new_level_number: int):
        """
        Description:
            Runs the completed pygame maze level, with the camera centering around the character.

        Parameters:
            new_points (float): The number of points the character was on, to be carried over to the next level
            new_health (float) The health the character was on, to be carried over to the next level
            new_level_number (int) The level number the character was on, to be carried over to the next level
        """
        # after a level is completed, the character points, health, level number is carried over to the next level
        self.character.level_number = new_level_number
        self.character.points = new_points
        self.character.health = new_health
