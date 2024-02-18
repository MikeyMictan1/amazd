import pygame
from globalfunctions import *
from math import cos, sqrt

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_name, pos, groups, wall_sprites, character):
        super().__init__(groups)
        self.frame_index = 0
        self.frame_speed = 0.15
        self.movement_vector = pygame.math.Vector2()
        self.collision_direction = None

        # general setup
        self.position = pos
        self.character = character

        # graphics setup
        self.animations_dict = {"idle":[], "moving":[], "attacking":[]}
        self.animations_dict = import_graphics_dict(enemy_name, self.animations_dict, "../Graphics/enemy")

        self.animation_state = "idle"
        self.image = self.animations_dict[self.animation_state][self.frame_index]
        self.image = pygame.transform.scale(self.image, (50,64))

        # movement
        self.rect = self.image.get_rect(topleft = self.position)
        self.wall_sprites = wall_sprites

        # player-enemy interactions
        self.can_be_damaged = True
        self.hit_time = None
        self.max_damage_time = 400
        self.attack_state = True
        self.time_of_attack = None
        self.attack_cooldown = 550

        # stats
        self.enemy_name = enemy_name
        self.knockback = 3
        self.enemy_damage = 100

        if self.enemy_name == "slime":
            self.health = 400
            self.speed = 7
            self.distance_to_attack = 200
            self.distance_to_notice = 760

        else:
            self.health = 100
            self.speed = 3
            self.distance_to_attack = 50
            self.distance_to_notice = 360

    def character_hit(self):  # player gets hit
        if self.character.can_be_damaged:
            self.character.health -= self.enemy_damage
            damage_music = pygame.mixer.Sound("../Audio/health_hit.mp3")
            damage_music.play()
            damage_music.set_volume(0.5)
            self.character.can_be_damaged = False
            self.character.time_damaged = pygame.time.get_ticks()

    def enemy_character_distance_vector(self, character):
        character_coordinate = pygame.math.Vector2(character.rect.center)
        enemy_coordinate = pygame.math.Vector2(self.rect.center)

        x_squared_distance = (character_coordinate[0] - enemy_coordinate[0]) ** 2
        y_squared_distance = (character_coordinate[1] - enemy_coordinate[1]) ** 2

        enemy_character_distance = sqrt(x_squared_distance + y_squared_distance)
        enemy_character_vector = character_coordinate - enemy_coordinate

        return (enemy_character_distance, enemy_character_vector)

    def enemy_hit(self, character): # enemy gets hit
        enemy_character_info = self.enemy_character_distance_vector(character)
        enemy_player_vector = enemy_character_info[1]

        if self.can_be_damaged:  # if enemy can be damaged
            self.movement_vector = enemy_player_vector  # getting enemy direction and moving them in a different direction
            self.health -= character.damage_enemy()
            self.hit_time = pygame.time.get_ticks()
            self.can_be_damaged = False

    def enemy_character_state(self, player):
        enemy_character_info = self.enemy_character_distance_vector(player)
        enemy_character_distance = enemy_character_info[0]
        enemy_character_vector = enemy_character_info[1]

        if enemy_character_distance <= self.distance_to_attack and self.attack_state:
            if self.animation_state != "attacking":
                self.frame_index = 0
            self.animation_state = "attacking"
            self.time_of_attack = pygame.time.get_ticks()
            self.character_hit()

        elif enemy_character_distance <= self.distance_to_notice:
            self.animation_state = "moving"
            self.movement_vector = enemy_character_vector

        else:
            self.animation_state = "idle"
            self.movement_vector = pygame.math.Vector2()

    def animation(self):
        self.frame_index += self.frame_speed

        # animating player
        if self.animation_state == "idle":
            if self.frame_index >= len(self.animations_dict["idle"]):
                self.frame_index = 0
            self.image = self.animations_dict["idle"][int(self.frame_index)]

        if self.animation_state == "moving":
            if self.frame_index >= len(self.animations_dict["moving"]):
                self.frame_index = 0
            self.image = self.animations_dict["moving"][int(self.frame_index)]

        if self.animation_state == "attacking":
            if self.frame_index >= len(self.animations_dict["attacking"]):
                self.frame_index = 0
                self.attack_state = False
            self.image = self.animations_dict["attacking"][int(self.frame_index)]

        # changing size depending on the enemy
        if self.enemy_name == "slime":
            self.image = pygame.transform.scale(self.image, (300, 300))

        else:
            self.image = pygame.transform.scale(self.image, (50, 64))

        self.rect = self.image.get_rect(center = self.rect.center)

        # enemy flickers on hit
        flicker = cos(0.1 * pygame.time.get_ticks())
        if not self.can_be_damaged and flicker < 0:
            self.image.set_alpha(255)

        elif not self.can_be_damaged:
            self.image.set_alpha(50)

        else:
            self.image.set_alpha(255)

    def damage_cooldown(self):
        game_loop_time = pygame.time.get_ticks()

        if not self.attack_state and (game_loop_time - self.time_of_attack) >= self.attack_cooldown:
            self.attack_state = True

        if not self.can_be_damaged:
            self.movement_vector *= -self.knockback  # enemy knockback
            if game_loop_time - self.hit_time >= self.max_damage_time:
                self.can_be_damaged = True

    def check_enemy_death(self):
        if self.health <= 0:
            enemy_death_sound = pygame.mixer.Sound("../Audio/enemy_death_sound.mp3")
            enemy_death_sound.play()
            enemy_death_sound.set_volume(0.2)
            self.kill()

    def enemy_movement(self):
        if self.movement_vector.magnitude():  # if vector has length
            self.movement_vector = self.movement_vector.normalize()  # set length of vector to 1 no matter what direction

        self.rect.x += self.movement_vector.x * self.speed
        self.collision_direction = "x"
        self.wall_collisions_check()
        self.rect.y += self.movement_vector.y * self.speed
        self.collision_direction = "y"
        self.wall_collisions_check()

    def wall_collisions_check(self):
        if self.collision_direction == "x":
            for sprite in self.wall_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.movement_vector.x > 0:  # moving right
                        self.rect.right = sprite.rect.left

                    if self.movement_vector.x < 0:  # moving left
                        self.rect.left = sprite.rect.right

        if self.collision_direction == "y":
            for sprite in self.wall_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.movement_vector.y > 0:  # moving down
                        self.rect.bottom = sprite.rect.top

                    if self.movement_vector.y < 0:  # moving up
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.damage_cooldown()
        self.enemy_movement()
        self.animation()
        self.check_enemy_death()




