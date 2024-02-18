import pygame
from mazelayout import *
from globalfunctions import *
from character import Character
from collidables import Powerups, Coins, HealthPot, Exit
from sword import Sword
from enemy import Enemy
from gamechange import GameOver
from camera import GameCamera

class MazeLevel:
    def __init__(self, maze_list):
        # sprite groups setup
        self.powerup_sprites = pygame.sprite.Group()
        self.coin_sprites = pygame.sprite.Group()
        self.health_pot_sprites = pygame.sprite.Group()
        self.exit_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.sword_sprites = pygame.sprite.Group()
        self.game_camera = GameCamera()
        self.wall_sprites = pygame.sprite.Group()

        # maze creation
        self.create_pygame_maze(maze_list)

        # other setup
        self.current_attack = None
        self.is_active = True
        self.level_type = "normal"


    def maze_loop(self, maze_lst, cell_check):
        row_num = -1
        for row in maze_lst:
            row_num += 1
            col_num = -1

            for cell in row:
                col_num += 1
                position = (col_num * tile_size, row_num * tile_size)
                cell_check(cell, position)

    def check_maze_layout(self, cell, position):
        if cell == "X":  # if there are walls
            Wall_Hidden(position,
                        [self.game_camera, self.wall_sprites])  # all the groups that belong to the sprite class

        if cell == "Y":
            Wall_Visible(position, [self.game_camera, self.wall_sprites])

        if cell in " PUECOSH":  # if there are floor tiles, including on the player
            self.floor = Floor(position, [self.game_camera])

    def check_maze_elements(self, cell, position):
        if cell == "P":  # if there is a player
            self.character = Character(position, [self.game_camera], self.wall_sprites, self.powerup_sprites, self.coin_sprites,
                                       self.health_pot_sprites, self.exit_sprites, self.sword_sprites)

        elif cell == "U":
            self.powerup = Powerups(position, [self.game_camera, self.powerup_sprites])

        elif cell == "C":
            self.coins = Coins(position, [self.game_camera, self.coin_sprites])

        elif cell == "E":
            self.enemy = Enemy("skeleton", position,
                               [self.game_camera, self.enemy_sprites],
                               self.wall_sprites,
                               self.character)

        elif cell == "S":
            self.enemy_slime = Enemy("slime", position,
                                     [self.game_camera, self.enemy_sprites],
                                     self.wall_sprites,
                                     self.character)

        elif cell == "H":
            self.health_pot = HealthPot(position, [self.game_camera, self.health_pot_sprites])

        elif cell == "O":
            self.exit = Exit(position, [self.game_camera, self.exit_sprites])

    def create_pygame_maze(self, maze_lst):
        self.maze_loop(maze_lst, self.check_maze_layout)
        self.maze_loop(maze_lst, self.check_maze_elements)


    def character_hit_enemy_check(self):  # checks if a player can attack an enemy
        if self.sword_sprites:
            for attack_sprite in self.sword_sprites:
                # list of all sprites that are colliding
                collision = pygame.sprite.spritecollide(attack_sprite, self.enemy_sprites, False)

                if collision:
                    for enemy_sprite in collision:
                        enemy_sprite.enemy_hit(self.character)


    def run_level(self):
        self.game_camera.draw_camera_offset(self.character)
        self.game_camera.update()
        self.character_hit_enemy_check()
        if not self.character.in_level:
            self.is_active = False


    def character_level_carryover(self, new_points, new_health, new_level_number):
        self.character.level_number = new_level_number
        self.character.points = new_points
        self.character.health = new_health


