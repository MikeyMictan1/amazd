import pygame
import math

import character as chara
import globalfunctions as gf


# clear code inspired class
class Enemy(pygame.sprite.Sprite):
    """
    Description:
        Class for the enemies that attack the character

    Inherits:
        pygame.sprite.Group: Inherits from pygame's sprite class to make sprite interactions and functions easier to
        handle.

    Attributes:
        __frame_index (float): Current frame used for animation
        __frame_speed (float): Speed of animations for the enemy
        __movement_vector (tuple): The vector in which the enemy is currently moving in
        __collision_direction (str): The direction the enemy collides with an object
        __position (tuple): Position of the character to be drawn onto the screen, given as a vector
        character (chara.Character): character sprite that the enemy will attack

        __animations_dict (dict): Dictionary of all images used for the enemy's animations
        __animation_state (str): Current animation state that the enemy is in
        image (pygame.Surface): The current image of the enemy
        rect (pygame.Rect): The rectangular area of the enemy in a certain location
        __wall_sprites (pygame.sprite.group): Sprite group consisting of maze wall sprites

        can_be_damaged (bool): Flag that checks if the character can deal damage to the enemy
        __time_damaged (float): The game time at which the enemy gets hit
        max_damage_time (float): The max amount of frames for which the enemy will be in an invulnerable state
        attack_state (bool): flag that checks if the enemy is attacking
        time_of_attack (float): The time at which the enemy starts an attack
        attack_cooldown (int): The number of frames for which an enemy cannot start another attack

        enemy_name (str): Name of the enemy sprite
        knock_back (int): The amount an enemy will be knocked back after being hit by a character
        enemy_damage (int): The amount of damage the enemy deals to the character
        health (float): The current value of health the enemy is on
        speed (float): How fast the enemy can move
        distance_to_attack (int): The distance for an enemy to start attacking the character
        distance_to_notice (int): The distance for an enemy to start moving towards the character
    """
    def __init__(self, enemy_name: str, pos: tuple, groups: list,
                 wall_sprites: pygame.sprite.Group, character: chara.Character):
        """
        Description:
            Initialisation function for the enemy class.

        Parameters:
            enemy_name (str): name of the enemy sprite
            pos (tuple): position of the enemy sprite on the screen
            groups (list): The sprite groups that the enemy belongs to
            wall_sprites (pygame.sprite.Group): Sprite group consisting of maze wall sprites
            character (chara.Character): Character that the enemy will move towards and attack
        """
        super().__init__(groups)
        self.__frame_index = 0
        self.__frame_speed = 0.15
        self.__movement_vector = pygame.math.Vector2()
        self.__collision_direction = None

        # general setup
        self.__position = pos
        self.character = character

        # graphics setup
        self.__animations_dict = {"idle": [], "moving": [], "attacking": []}
        self.__animations_dict = gf.import_graphics_dict(enemy_name, self.__animations_dict, "../Graphics/enemy")

        self.__animation_state = "idle"
        self.image = self.__animations_dict[self.__animation_state][self.__frame_index]
        self.image = pygame.transform.scale(self.image, (50, 64))

        # movement
        self.rect = self.image.get_rect(topleft=self.__position)
        self.__wall_sprites = wall_sprites

        # player-enemy interactions
        self.__time_damaged = None
        self.can_be_damaged = True
        self.max_damage_time = 400
        self.attack_state = True
        self.time_of_attack = None
        self.attack_cooldown = 550

        # stats
        self.enemy_name = enemy_name
        self.knock_back = 3
        self.enemy_damage = 100

        if self.enemy_name == "slime":  # if the enemy is the slime boss, then given them modified stats
            self.health = 400
            self.speed = 7
            self.distance_to_attack = 130
            self.distance_to_notice = 760

        else:
            self.health = 100
            self.speed = 3
            self.distance_to_attack = 50
            self.distance_to_notice = 360

    def __character_hit(self):
        """
        Description:
            Checks if a character can be hit, if so, then damage the character.
        """
        if self.character.can_be_damaged:
            self.character.health -= self.enemy_damage  # deals damage to the character
            damage_music = pygame.mixer.Sound("../Audio/health_hit.mp3")
            damage_music.play()
            damage_music.set_volume(0.5)
            self.character.can_be_damaged = False
            self.character.time_damaged = pygame.time.get_ticks()

    def __enemy_character_distance_vector(self, character: chara.Character):
        """
        Description:
            finds the distance and vector between the enemy and character

        Parameters:
            character (chara.Character): character sprite (the player)

        Returns:
            enemy_character_distance (float): the distance from the enemy to the character
            enemy_character_vector (tuple) The vector between the enemy and the character
        """
        character_coordinate = pygame.math.Vector2(character.rect.center)
        enemy_coordinate = pygame.math.Vector2(self.rect.center)

        x_squared_distance = (character_coordinate[0] - enemy_coordinate[0]) ** 2
        y_squared_distance = (character_coordinate[1] - enemy_coordinate[1]) ** 2

        enemy_character_distance = math.sqrt(x_squared_distance + y_squared_distance)  # pythagorean theorem
        enemy_character_vector = character_coordinate - enemy_coordinate

        return enemy_character_distance, enemy_character_vector

    def enemy_hit(self, character: chara.Character):  # enemy gets hit
        """
        Description:
            Checks if the enemy can be hit, if so, then damage the enemy

        Parameters:
            character (chara.Character): character sprite (the player)
        """
        enemy_character_info = self.__enemy_character_distance_vector(character)
        enemy_player_vector = enemy_character_info[1]

        if self.can_be_damaged:  # if enemy can be damaged
            self.__movement_vector = enemy_player_vector  # get enemy direction and move it in a different direction
            self.health -= character.damage_enemy()
            self.__time_damaged = pygame.time.get_ticks()
            self.can_be_damaged = False

    def enemy_character_state(self, character: chara.Character):
        """
        Description:
            decides what state the enemy should be in depending on factors such as distance from character

        Parameters:
            character (chara.Character): character sprite (the player)
        """
        enemy_character_info = self.__enemy_character_distance_vector(character)
        enemy_character_distance = enemy_character_info[0]
        enemy_character_vector = enemy_character_info[1]

        # if the enemy is close enough to the character, then the state should be "attacking"
        if enemy_character_distance <= self.distance_to_attack and self.attack_state:
            if self.__animation_state != "attacking":
                self.__frame_index = 0
            self.__animation_state = "attacking"
            self.time_of_attack = pygame.time.get_ticks()
            self.__character_hit()

        # if the enemy is close enough to the character, then the state should be "moving"
        elif enemy_character_distance <= self.distance_to_notice:
            self.__animation_state = "moving"
            self.__movement_vector = enemy_character_vector

        # if the enemy is not close to the character, then the state of the enemy will be "idle"
        else:
            self.__animation_state = "idle"
            self.__movement_vector = pygame.math.Vector2()

    def __animation(self):  # handles animations of the enemy
        """
        Description:
            Animates the enemy depending on the enemies current state
        """
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

        self.rect = self.image.get_rect(center=self.rect.center)

        # enemy flickers on hit
        flicker = math.cos(0.1 * pygame.time.get_ticks())
        if not self.can_be_damaged and flicker > 0:
            self.image.set_alpha(50)

        else:
            self.image.set_alpha(255)

    def __damage_cooldown(self):
        """
        Description:
            Allows the enemy to  only be able to attack, or be attacked, every few seconds
        """
        game_loop_time = pygame.time.get_ticks()

        if not self.attack_state and (game_loop_time - self.time_of_attack) >= self.attack_cooldown:
            self.attack_state = True

        if not self.can_be_damaged:
            self.__movement_vector *= -self.knock_back  # knocks the enemy back in the opposite direction to the player
            if game_loop_time - self.__time_damaged >= self.max_damage_time:
                self.can_be_damaged = True

    def __check_enemy_death(self):
        """
        Description:
            checks if the enemy is dead, if so, then kill the enemy sprite
        """
        if self.health <= 0:
            enemy_death_sound = pygame.mixer.Sound("../Audio/enemy_death_sound.mp3")
            enemy_death_sound.play()
            enemy_death_sound.set_volume(0.2)
            self.kill()

    def __enemy_movement(self):
        """
        Description:
            Moves the enemy by their movement vector, and checks for collisions in x and y directions.
        """
        if self.__movement_vector.magnitude():  # if vector has length
            self.__movement_vector = self.__movement_vector.normalize()  # length of vector = 1 no matter the direction

        self.rect.x += self.__movement_vector.x * self.speed
        # checks if the enemy collides with a wall in "x" direction, if so, don't let them move through it
        self.__collision_direction = "x"
        self.__wall_collisions_check()
        self.rect.y += self.__movement_vector.y * self.speed
        # checks if the enemy collides with a wall in "y" direction, if so, don't let them move through it
        self.__collision_direction = "y"
        self.__wall_collisions_check()

    def __wall_collisions_check(self):
        """
        Description:
            Checks if there is a collision with walls, if so, don't let the enemy move through them
        """
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
        """
         Description:
             Runs most methods, so that the enemy is constantly updates every frame
         """
        self.__damage_cooldown()
        self.__enemy_movement()
        self.__animation()
        self.__check_enemy_death()
