import pygame

import mazelayout as mz_lay
import globalfunctions as gf
import character as chara
import collidables as coll
import camera as cam
import enemy


class MazeLevel:
    def __init__(self, maze_list):
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

    def __maze_loop(self, maze_lst, check_maze_cell):  # loops through every cell in the maze
        row_num = -1
        for row in maze_lst:
            row_num += 1
            col_num = -1

            for cell in row:
                col_num += 1
                position = (col_num * gf.tile_size, row_num * gf.tile_size)
                check_maze_cell(cell, position)

    def __check_maze_layout(self, cell, position):

        if cell == "X":  # if there are walls
            mz_lay.WallHidden(position, [self.__game_camera, self.__wall_sprites])
            # all the groups that belong to the sprite class

        if cell == "Y":
            mz_lay.WallVisible(position, [self.__game_camera, self.__wall_sprites])

        if cell in " PUECOSH":  # if there are floor tiles, including on the player
            self.floor = mz_lay.Floor(position, [self.__game_camera])

    def __check_maze_elements(self, cell, position):
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

    def create_pygame_maze(self, maze_lst):  # creates the completed pygame maze
        self.__maze_loop(maze_lst, self.__check_maze_layout)
        self.__maze_loop(maze_lst, self.__check_maze_elements)

    def __character_hit_enemy_check(self):  # checks if a player can attack an enemy
        if self.__sword_sprites:
            for attack_sprite in self.__sword_sprites:
                # list of all sprites that are colliding
                collision = pygame.sprite.spritecollide(attack_sprite, self.__enemy_sprites, False)

                if collision:
                    for enemy_sprite in collision:
                        enemy_sprite.enemy_hit(self.character)

    def run_level(self):  # runs the completed pygame maze level
        self.__game_camera.draw_camera_offset(self.character)
        self.__game_camera.update()
        self.__character_hit_enemy_check()
        if not self.character.in_level:
            self.is_active = False

    def character_level_carryover(self, new_points, new_health, new_level_number):
        # after a level is completed, the character points, health, level number is carried over to the next level
        self.character.level_number = new_level_number
        self.character.points = new_points
        self.character.health = new_health
