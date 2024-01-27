import pygame
from tile import *
from settings import *
from player import Player
from debug import debug
from powerups import Powerups
from weapon import Weapon
from enemy import Enemy
from coins import Coins
from exit import Exit



class Level:
    def __init__(self, maze_list):
        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.powerup_sprites = pygame.sprite.Group()
        self.coin_sprites = pygame.sprite.Group()
        self.exit_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map(maze_list)

        # weapon sprites
        self.current_attack = None


        #
        self.level_active = True




    def create_map(self, maze_list):  # layout will be our map list !
        for row_index,row in enumerate(maze_list):
            for col_index,cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == "X":  # if there are walls
                    Wall_Tile_Hidden((x,y),[self.visible_sprites, self.obstacle_sprites])  # all the groups that belong to the sprite class

                if cell == "Y":  # if there are walls
                    Wall_Tile_Visible((x,y),[self.visible_sprites, self.obstacle_sprites])  # all the groups that belong to the sprite class

                if cell == " " or cell == "P" or cell == "U" or cell == "E" or cell == "C" or cell == "O":  # if there are floor tiles, including on the player
                    self.floor = Floor_Tile((x,y),[self.visible_sprites])  # all the groups that belong to the sprite class !

        # draws the player on top of all the other sprites
        for row_index,row in enumerate(maze_list):
            for col_index,cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == "P":  # if there is a player
                    self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites, self.powerup_sprites, self.coin_sprites,self.exit_sprites , self.create_attack, self.destroy_attack)

                if cell == "U":
                    self.powerup = Powerups((x,y),[self.visible_sprites, self.powerup_sprites])

                if cell == "C":
                    self.coins = Coins((x,y),[self.visible_sprites, self.coin_sprites])

                if cell == "E":
                    self.enemy = Enemy("skeleton", (x,y),
                                       [self.visible_sprites, self.attackable_sprites],
                                       self.obstacle_sprites,
                                       self.damage_player)

                if cell == "O":
                    self.exit = Exit((x,y), [self.visible_sprites, self.exit_sprites])


    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
            print("destroyed")  # can be removed

        self.current_attack = None

    def player_attack_logic(self):  # checks if a player can attack an enemy
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                # list of all sprites that are colliding
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "enemy":
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)


    def damage_player(self, amount):  # attack type doesn't get used
        if self.player.can_damage:
            self.player.health -= amount
            damage_music = pygame.mixer.Sound("../Audio/health_hit.mp3")
            damage_music.play()
            damage_music.set_volume(0.5)
            self.player.can_damage = False
            self.player.hurt_time = pygame.time.get_ticks()
            # spawn particles

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        debug(self.player.direction)
        if self.player.in_level == False:
            self.level_active = False
            print("level complete")



    def player_level_carryover(self, new_points, new_health):
        self.player.points = new_points
        self.player.health = new_health







class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2  # can change to my code later
        self.half_height = self.display_surface.get_size()[1] // 2  # can change to my code later
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        keys = pygame.key.get_pressed()
        # getting the offset
        self.offset.y = player.rect.centery - self.half_height
        self.offset.x = player.rect.centerx - self.half_width


        for sprite in self.sprites():
            # we can add a vector to sprite.rect (an offset that effects where the sprite will be drawn)
            # draw the sprite image in the same place as the rectangle
            offset_pos = sprite.rect.topleft - self.offset
            
            if sprite == player:
                self.display_surface.blit(sprite.image, offset_pos + (-75, -45))

            else:
                self.display_surface.blit(sprite.image, offset_pos)


    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)







# LOOK INTO DRAWING THE STUFF ONLY WHEN IT IS OFFSCREEN BCZ THATS APPARENTLY DO-ABLE
