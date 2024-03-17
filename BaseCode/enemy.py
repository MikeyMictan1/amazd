import pygame
from globalfunctions import *
from math import cos, sqrt

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_name, pos, groups, wall_sprites, character):
        super().__init__(groups)
        self.__frame_index = 0
        self.__frame_speed = 0.15
        self.__movement_vector = pygame.math.Vector2()
        self.__collision_direction = None

        # general setup
        self.__position = pos
        self.character = character

        # graphics setup
        self.__animations_dict = {"idle":[], "moving":[], "attacking":[]}
        self.__animations_dict = import_graphics_dict(enemy_name, self.__animations_dict, "../Graphics/enemy")

        self.__animation_state = "idle"
        self.image = self.__animations_dict[self.__animation_state][self.__frame_index]
        self.image = pygame.transform.scale(self.image, (50, 64))

        # movement
        self.rect = self.image.get_rect(topleft = self.__position)
        self.__wall_sprites = wall_sprites

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
            self.distance_to_attack = 130
            self.distance_to_notice = 760

        else:
            self.health = 100
            self.speed = 3
            self.distance_to_attack = 50
            self.distance_to_notice = 360

    def __character_hit(self):  # player gets hit
        if self.character.can_be_damaged:
            self.character.health -= self.enemy_damage
            damage_music = pygame.mixer.Sound("../Audio/health_hit.mp3")
            damage_music.play()
            damage_music.set_volume(0.5)
            self.character.can_be_damaged = False
            self.character.time_damaged = pygame.time.get_ticks()

    def __enemy_character_distance_vector(self, character):
        character_coordinate = pygame.math.Vector2(character.rect.center)
        enemy_coordinate = pygame.math.Vector2(self.rect.center)

        x_squared_distance = (character_coordinate[0] - enemy_coordinate[0]) ** 2
        y_squared_distance = (character_coordinate[1] - enemy_coordinate[1]) ** 2

        enemy_character_distance = sqrt(x_squared_distance + y_squared_distance)
        enemy_character_vector = character_coordinate - enemy_coordinate

        return (enemy_character_distance, enemy_character_vector)

    def enemy_hit(self, character): # enemy gets hit
        enemy_character_info = self.__enemy_character_distance_vector(character)
        enemy_player_vector = enemy_character_info[1]

        if self.can_be_damaged:  # if enemy can be damaged
            self.__movement_vector = enemy_player_vector  # getting enemy direction and moving them in a different direction
            self.health -= character.damage_enemy()
            self.hit_time = pygame.time.get_ticks()
            self.can_be_damaged = False

    def enemy_character_state(self, character):
        enemy_character_info = self.__enemy_character_distance_vector(character)
        enemy_character_distance = enemy_character_info[0]
        enemy_character_vector = enemy_character_info[1]

        if enemy_character_distance <= self.distance_to_attack and self.attack_state:
            if self.__animation_state != "attacking":
                self.__frame_index = 0
            self.__animation_state = "attacking"
            self.time_of_attack = pygame.time.get_ticks()
            self.__character_hit()

        elif enemy_character_distance <= self.distance_to_notice:
            self.__animation_state = "moving"
            self.__movement_vector = enemy_character_vector

        else:
            self.__animation_state = "idle"
            self.__movement_vector = pygame.math.Vector2()

    def __animation(self):
        self.__frame_index += self.__frame_speed

        # animating player
        if self.__animation_state == "idle":
            if self.__frame_index >= len(self.__animations_dict["idle"]):
                self.__frame_index = 0
            self.image = self.__animations_dict["idle"][int(self.__frame_index)]

        if self.__animation_state == "moving":
            if self.__frame_index >= len(self.__animations_dict["moving"]):
                self.__frame_index = 0
            self.image = self.__animations_dict["moving"][int(self.__frame_index)]

        if self.__animation_state == "attacking":
            if self.__frame_index >= len(self.__animations_dict["attacking"]):
                self.__frame_index = 0
                self.attack_state = False
            self.image = self.__animations_dict["attacking"][int(self.__frame_index)]

        # changing size depending on the enemy
        if self.enemy_name == "slime":
            self.image = pygame.transform.scale(self.image, (300, 300))

        else:
            self.image = pygame.transform.scale(self.image, (50, 64))

        self.rect = self.image.get_rect(center = self.rect.center)

        # enemy flickers on hit
        flicker = cos(0.1 * pygame.time.get_ticks())
        if not self.can_be_damaged and flicker > 0:
            self.image.set_alpha(50)

        else:
            self.image.set_alpha(255)

    def __damage_cooldown(self):
        game_loop_time = pygame.time.get_ticks()

        if not self.attack_state and (game_loop_time - self.time_of_attack) >= self.attack_cooldown:
            self.attack_state = True

        if not self.can_be_damaged:
            self.__movement_vector *= -self.knockback  # enemy knockback
            if game_loop_time - self.hit_time >= self.max_damage_time:
                self.can_be_damaged = True

    def __check_enemy_death(self):
        if self.health <= 0:
            enemy_death_sound = pygame.mixer.Sound("../Audio/enemy_death_sound.mp3")
            enemy_death_sound.play()
            enemy_death_sound.set_volume(0.2)
            self.kill()

    def __enemy_movement(self):
        if self.__movement_vector.magnitude():  # if vector has length
            self.__movement_vector = self.__movement_vector.normalize()  # set length of vector to 1 no matter what direction

        self.rect.x += self.__movement_vector.x * self.speed
        self.__collision_direction = "x"
        self.__wall_collisions_check()
        self.rect.y += self.__movement_vector.y * self.speed
        self.__collision_direction = "y"
        self.__wall_collisions_check()

    def __wall_collisions_check(self):
        if self.__collision_direction == "x":
            for sprite in self.__wall_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.__movement_vector.x > 0:  # moving right
                        self.rect.right = sprite.rect.left

                    if self.__movement_vector.x < 0:  # moving left
                        self.rect.left = sprite.rect.right

        if self.__collision_direction == "y":
            for sprite in self.__wall_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.__movement_vector.y > 0:  # moving down
                        self.rect.bottom = sprite.rect.top

                    if self.__movement_vector.y < 0:  # moving up
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.__damage_cooldown()
        self.__enemy_movement()
        self.__animation()
        self.__check_enemy_death()



