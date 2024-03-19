import pygame
import numpy
import math

import globalfunctions as gf
import sword


class Character(pygame.sprite.Sprite):
    """
    Description:
        The class for the character that the player controls

    Inherits:
        pygame.sprite.Group: Inherits from pygame's sprite class to make sprite interactions and functions easier to
        handle.

    Attributes:
        __key_press (pygame.key): Checks if a key on the keyboard has been pressed
        __level_up (bool): Flag that checks if the next level has been reached
        __screen (pygame.Surface): Screen that objects will be drawn onto
        __collision_direction (str): The direction the character collides with an object
        tutorial_mode (bool): Flag that checks if the character is in a tutorial level
        level_number (int): The number of the current level the character is in
            
        __wall_sprites (pygame.sprite.Group): Sprite group consisting of maze wall sprites
        __powerup_sprites (pygame.sprite.Group): Sprite group consisting of speed powerup sprites
        __coin_sprites (pygame.sprite.Group): Sprite group consisting of coin sprites
        __exit_sprites (pygame.sprite.Group): Sprite group consisting of exit portal sprites
        __health_pot_sprites (pygame.sprite.Group): Sprite group consisting of health potion sprites
        __sword_sprites (pygame.sprite.Group): Sprite group consisting of sword sprites
        __game_camera (pygame.sprite.Group): Sprite group consisting of the camera that the character centres around

        __position (tuple): Position of the character to be drawn onto the screen, given as a vector
        __rect_width (int): Width of the characters hit-box
        __rect_height (int): Height of the characters hit-box
        __character_width (int): Width of the image of the character
        __character_height (int): Height of the image of the character

        __sprinting (bool): Flag that checks if the character is sprinting
        __frame (float): Current frame used for animation
        __attacking_frame (float): Current frame used for animating the characters attacks
        __frame_speed (float): Speed of animations for the character
        __attacking_frame_speed (float): Speed of the characters attack animation

        __speed (int): The speed that the character can move
        __movement_vector (tuple): The vector in which the character is currently moving in
        __max_stamina (float): The maximum amount of stamina that the character can ever have
        __stamina (float): The characters current stamina, used for sprinting. Can never exceed max stamina

        __is_attacking (bool): Flag that checks if the character is currently in the attack animation
        __time_of_attack (float): Gets the game time at which the character starts an attack
        __character_damage (int): The value of "damage" that the player does to the enemy

        __powerup_active (float): Flag that checks if a speed powerup is active
        __powerup_timer_image (pygame.Surface): Image of a speed powerup that appears while a powerup is active

        __max_health (int): The max health value that the character can have
        health (float): The current health value of the character
        points (float): The current number of points that the character is on
        in_level (bool): A flag that checks if the character is supposed to be in the current level

        can_be_damaged (bool): Flag that checks if the enemy can deal damage to the character
        time_damaged (float): The game time at which the character gets hit
        max_damage_time (int): The max amount of frames for which the character will be in an invulnerable state

        __stats_animation_dict (dict): Dictionary of all images used for health and stamina animation
        __animation_dict (dict): Dictionary of all images used for the characters movement animations
        __state (str): The current animation state of the character
        __character_direction (str): The current direction the character is facing/moving
        image (pygame.Surface): The current image of the character
        rect (pygame.Rect): The rectangular area of the character in a certain location
        __move_count (int): checks how many times the player has inputted movement, in order to play walking sounds
        __walk_sound (pygame.mixer.Sound): Sound effect for the player moving

        __controls_font (pygame.font.Font): Text font used for the controls menu
        __controls_instructions (pygame.Surface): Image of the controls instructions
        __controls_instructions_txt (pygame.Surface): Text that states "controls" in the bottom left corner
    """
    def __init__(self, pos: tuple, groups: list, wall_sprites: pygame.sprite.Group,
                 powerup_sprites: pygame.sprite.Group, coin_sprites: pygame.sprite.Group,
                 health_pot_sprites: pygame.sprite.Group, exit_sprites: pygame.sprite.Group,
                 sword_sprites: pygame.sprite.Group):
        """
        Description:
            Initialisation function for the character class

        Parameters:
            pos (tuple): Position of the character to be drawn onto the screen, given as a vector
            groups (list): Groups that the character class is a part of
            wall_sprites (pygame.sprite.Group): Sprite group consisting of maze wall sprites
            powerup_sprites (pygame.sprite.Group): Sprite group consisting of speed powerup sprites
            coin_sprites (pygame.sprite.Group): Sprite group consisting of coin sprites
            health_pot_sprites (pygame.sprite.Group): Sprite group consisting of health potion sprites
            exit_sprites (pygame.sprite.Group): Sprite group consisting of exit portal sprites
            sword_sprites (pygame.sprite.Group): Sprite group consisting of sword sprites
        """
        super().__init__(groups)
        # general setup
        self.__key_press = pygame.key.get_pressed()
        self.__level_up = False  # have we reached the end of the level
        self.__screen = pygame.display.get_surface()
        self.__collision_direction = None
        self.tutorial_mode = False
        self.level_number = 1

        # obstacles collision
        self.__wall_sprites = wall_sprites
        self.__powerup_sprites = powerup_sprites
        self.__coin_sprites = coin_sprites
        self.__exit_sprites = exit_sprites
        self.__health_pot_sprites = health_pot_sprites
        self.__sword_sprites = sword_sprites
        self.__game_camera = groups

        # player setup
        self.__position = pos
        self.__rect_width = 50
        self.__rect_height = 64
        self.__character_width = 200
        self.__character_height = 160

        # player animation state
        self.__sprinting = False
        self.__frame = 0
        self.__attacking_frame = 0
        self.__frame_speed = 0.1
        self.__attacking_frame_speed = 0.1

        # movement
        self.__speed = 5
        self.__movement_vector = pygame.math.Vector2()
        self.__max_stamina = 1500
        self.__stamina = self.__max_stamina

        # attacks
        # clear code inspired ---
        self.__is_attacking = False
        self.__time_of_attack = None
        # clear code inspired ---

        self.__character_damage = 25

        # powerup timer
        self.__powerup_active = 0
        self.__powerup_timer_image = pygame.image.load(
            f"../Graphics/powerups/speedpowerup1.png").convert_alpha()  # making a standard square surface

        # stats
        self.__max_health = 700
        self.health = self.__max_health
        self.points = 501
        self.in_level = True

        # damage timer
        self.can_be_damaged = True
        self.time_damaged = None
        self.max_damage_time = 1000

        # stats animation dictionary
        self.__stats_animation_dict = {"health": [], "stamina": []}
        self.__stats_animation_dict = gf.import_graphics_dict("stats", self.__stats_animation_dict, "../Graphics")

        # making the character
        self.__animation_dict = {"attack_down": [], "attack_right": [], "attack_up": [],
                                 "idle_down": [], "idle_right": [], "idle_up": [],
                                 "moving_down": [], "moving_right": [], "moving_up": []}

        self.__animation_dict = gf.import_graphics_dict("character", self.__animation_dict, "../Graphics")
        self.__state = "idle_right"  # default states
        self.__character_direction = "down"
        self.image = self.__animation_dict[self.__state][self.__frame]
        self.image = pygame.transform.scale(self.image, (self.__rect_width, self.__rect_height))
        self.rect = self.image.get_rect(topleft=pos)
        self.__move_count = 0

        # walking audio
        self.__walk_sound = pygame.mixer.Sound("../Audio/walk_sound.mp3")

        # other hud info
        self.__controls_font = pygame.font.Font("../Fonts/Pixel.ttf", 30)
        self.__controls_instructions = pygame.image.load(
            "../Graphics/controls/controls_instruction.png").convert_alpha()
        self.__controls_instructions = pygame.transform.scale(self.__controls_instructions, (50, 50))
        self.__controls_instructions_txt = self.__controls_font.render("Controls", 1, gf.white)

    def __cause_attacks(self):
        """
        Description:
            Causes the character to enter an attacking state, by starting the attack animation and creating a sword
            sprite in-front of the character.
        """
        self.__is_attacking = True
        self.__time_of_attack = pygame.time.get_ticks()
        self.__positions = [self.rect.midright, self.rect.midleft, self.rect.midbottom, self.rect.midtop]
        self.__sword = sword.Sword(self.__character_direction, self.__positions,
                                   [self.__game_camera, self.__sword_sprites])
        self.__attacking_frame = 0

    def __character_input(self):
        """
        Description:
            Takes keyboard inputs from the player, and gives the relevant character output.

            Handles inputs for starting player movement, player attacks, sprinting, opening menus.
        """
        __key_press = pygame.key.get_pressed()

        # movement
        if __key_press[pygame.K_w]:
            self.__movement_vector.y = -1
            self.__character_direction = "up"

        elif __key_press[pygame.K_s]:
            self.__movement_vector.y = 1
            self.__character_direction = "down"
        else:
            self.__movement_vector.y = 0

        if __key_press[pygame.K_d]:
            self.__movement_vector.x = 1
            self.__character_direction = "right"

        elif __key_press[pygame.K_a]:
            self.__movement_vector.x = -1
            self.__character_direction = "left"

        else:
            self.__movement_vector.x = 0

        # ATTACK INPUT
        if not self.__is_attacking:
            if __key_press[pygame.K_SPACE]:
                self.__cause_attacks()

        # sprint
        # if sprinting, and we have enough stamina
        if __key_press[pygame.K_LSHIFT] and self.__stamina > 120 and (
                self.__movement_vector.x != 0 or self.__movement_vector.y != 0) and self.__speed <= 10:
            self.__speed = 10
            self.__sprinting = True
            self.__stamina -= 5
            # cutoff at 120, so that they cant sprint immediately after running out of stamina
            if self.__stamina <= 120:
                self.__stamina = 0

        else:
            self.__speed = 5
            self.__sprinting = False
            if self.__stamina < self.__max_stamina:
                self.__stamina += 6

        # code here round our value of stamina to the nearest 100, and puts in a format to be drawn to screen
        if len(str(self.__stamina)) == 4:
            round_number = numpy.format_float_positional(self.__stamina, precision=2, unique=False, fractional=False)

        else:
            round_number = numpy.format_float_positional(self.__stamina, precision=1, unique=False, fractional=False)

        stamina_lst = []

        for i in range(len(round_number) - 1):
            stamina_lst.append(round_number[i])

        self.stamina_joined = "".join(stamina_lst)

        if self.__powerup_active > 0:  # if a powerup is active, -1 for each frame, and give player speed boost
            self.__powerup_active -= 1
            self.__speed = 15

    def __character_movement(self):
        """
        Description:
            Moves the character by their movement vector, and checks for collisions in x and y directions.

            Plays walking sounds for whenever the character is moving.
        """
        # CLEAR CODE INSPIRED ---
        if self.__movement_vector.magnitude() != 0:  # if vector has length
            self.__movement_vector = self.__movement_vector.normalize()  # set length of vector to 1 no matter what
            # direction

        self.rect.x += self.__movement_vector.x * self.__speed
        self.__collision_direction = "x"
        self.__collisions_check()
        self.rect.y += self.__movement_vector.y * self.__speed
        self.__collision_direction = "y"
        self.__collisions_check()
        # CLEAR CODE INSPIRED ---

        if self.__move_count == 1:
            self.__walk_sound.play(999)  # if we start to walk, then play walking sound
            self.__walk_sound.set_volume(0.5)
        self.__move_count += 1

        if self.__movement_vector == [0, 0]:
            self.__walk_sound.stop()  # once we stop walking, stop the walking playing sound
            self.__move_count = 0

    def __damage_cooldown(self):
        """
        Description:
            After being attacked, prevents the character from being attacked again for a short time.
        """
        game_loop_time = pygame.time.get_ticks()  # gets current time
        # once the attack animation is on the final frame, kill the sword and stop the attack
        if self.__is_attacking and round(self.__attacking_frame, 1) == 3.9:
            self.__sword.kill()
            self.__is_attacking = False

        # if the character currently can't be damaged, and the amount of time damaged has exceeded max damage time, then
        # allow the character to be able to be damaged again.
        if not self.can_be_damaged and game_loop_time - self.time_damaged >= self.max_damage_time:
            self.can_be_damaged = True

    def __collisions_check(self):
        """
         Description:
             Checks if the character collides with walls, powerups, exit portals, health potions, coins.
         """
        # CLEAR CODE INSPIRED ---
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
        # CLEAR CODE INSPIRED ---

        # POWERUPS
        if self.__collision_direction in "xy":
            for sprite in self.__powerup_sprites:
                if sprite.rect.colliderect(self.rect):  # collision with powerup, and kills the sprite when they collide
                    self.__powerup_active = 300  # powerups last for 5 seconds (300 frames)
                    powerup_sound = pygame.mixer.Sound("../Audio/speed_powerup.mp3")  # plays powerup noise
                    powerup_sound.play()
                    powerup_sound.set_volume(0.5)
                    sprite.kill()

        # COINS
        if self.__collision_direction in "xy":
            for sprite in self.__coin_sprites:
                if sprite.rect.colliderect(self.rect):
                    # SOUND
                    coin_sound = pygame.mixer.Sound("../Audio/coin.mp3")
                    coin_sound.play()
                    coin_sound.set_volume(0.5)

                    # POINTS
                    self.points += 20
                    sprite.kill()

        # HEALTH POTION
        if self.__collision_direction in "xy":
            for sprite in self.__health_pot_sprites:
                if sprite.rect.colliderect(self.rect):
                    # SOUND
                    health_pot_sound = pygame.mixer.Sound("../Audio/health_pot.mp3")
                    health_pot_sound.play()
                    health_pot_sound.set_volume(0.5)

                    # POINTS
                    if self.__max_health != self.health:
                        self.health += 100
                    sprite.kill()

        # EXIT
        if self.__collision_direction in "xy":
            for sprite in self.__exit_sprites:
                if sprite.rect.colliderect(self.rect):
                    if not self.__level_up:
                        self.level_number += 1
                        self.__level_up = True

                    portal_sound = pygame.mixer.Sound("../Audio/portal.mp3")
                    portal_sound.play()
                    self.__walk_sound.stop()  # makes sure walking sound stops
                    portal_sound.set_volume(0.1)

                    self.in_level = False
                    sprite.kill()

    def __powerup_timer(self):
        """
         Description:
             Timer for how long a speed powerup effect will last for the character.
         """
        # fonts and colours
        if self.__powerup_active:
            # powerup graphic
            self.__powerup_timer_image = pygame.transform.scale(self.__powerup_timer_image, (100, 100))
            self.__screen.blit(self.__powerup_timer_image, (gf.screen_width // 15, gf.screen_height // 1.2))

            # powerup timer count
            timer = gf.font.render(str(self.__powerup_active), 1, gf.white)
            self.__screen.blit(timer, (gf.screen_width // 10 - timer.get_width() // 2, gf.screen_height // 1.2))

    def __frame_updates(self):
        """
         Description:
             Updates frame speed for animation depending on certain conditions, and resets frame number after an
             animation has finished.
        """
        # standard animation update
        self.__frame += self.__frame_speed
        if self.__frame >= len(self.__animation_dict["idle_right"]):  # could be any folder, but took the first one
            self.__frame = 0

        # special attack animation update
        self.__attacking_frame += self.__attacking_frame_speed
        if self.__attacking_frame >= len(self.__animation_dict["attack_down"]):
            self.__attacking_frame = 0

        # check for powerup
        if self.__powerup_active:  # increase frame speed if using speed powerup by a large amount
            self.__frame_speed = 0.5

        # check for sprint
        elif self.__sprinting:  # increase frame speed if using speed powerup
            self.__frame_speed = 0.2

        # walking speed
        else:  # default frame speed
            self.__frame_speed = 0.1

    def __animation(self):
        """
         Description:
             Animates the character when moving, idle, attacking, or when hit.
        """
        self.__key_press = pygame.key.get_pressed()
        # --- ATTACKING ANIMATION ---
        if self.__is_attacking:
            self.image = self.__animation_dict[self.__get_animation_state("attack")][int(self.__attacking_frame)]

        # --- MOVING ANIMATION ---
        elif self.__key_press[pygame.K_s] or self.__key_press[pygame.K_d] or self.__key_press[pygame.K_a] or \
                self.__key_press[pygame.K_w]:
            self.image = self.__animation_dict[self.__get_animation_state("moving")][int(self.__frame)]

        # --- IDLE ANIMATION ---
        else:
            self.image = self.__animation_dict[self.__get_animation_state("idle")][int(self.__frame)]

        # making the image
        if self.__character_direction == "left":  # if facing left, as need to flip image
            self.image = pygame.transform.flip(self.image, True, False)

        self.image = pygame.transform.scale(self.image,
                                            (self.__character_width, self.__character_height))  # resizing image

        # player flicker on hit
        flicker = math.cos(0.1 * pygame.time.get_ticks())
        if not self.can_be_damaged and flicker > 0:
            self.image.set_alpha(50)

        else:
            self.image.set_alpha(255)

    def __get_animation_state(self, state: str):  # finds what direction and action is happening to the character
        """
         Description:
             Gets the correct animation state for what the action the character is currently performing.

        Parameters:
            state (str): The current state of the character (idle, moving, attacking)

        Returns:
            animation_type (str): The animation state of the character, needed to retrieve from the animation dictionary
        """
        if self.__character_direction == "left":
            animation_type = f"{state}_right"
        else:
            animation_type = f"{state}_{self.__character_direction}"

        return animation_type

    def __points_timer(self):
        """
         Description:
             Timer that reduces points so points slowly go down every second while in the game
        """
        self.points -= (1 / 60)

    def damage_enemy(self):
        """
        Description:
            If an enemy is hit, then the character gains 5 points

        Returns:
            __character_damage(int): returns damage value, so enemies get hit by that amount
        """
        self.points += 5  # you get 5 points on enemy hit
        return self.__character_damage

    def __heads_up_display(self):
        """
        Description:
            Draws import information such as character health bar, stamina bar onto the screen
        """
        #  putting stats on the screen (health and stamina)
        stamina_index = (int(self.stamina_joined) // 100)
        health_index = (self.health // 100)

        self.stamina_image = self.__stats_animation_dict["stamina"][stamina_index]
        self.stamina_image = pygame.transform.scale(self.stamina_image, (400, 80))
        self.__screen.blit(self.stamina_image, (gf.screen_width // 70, gf.screen_height // 5))

        self.health_image = self.__stats_animation_dict["health"][health_index]
        self.health_image = pygame.transform.scale(self.health_image, (300, 50))
        self.__screen.blit(self.health_image, (gf.screen_width // 70, gf.screen_height // 7))

        # putting points on the screen
        self.point_display = gf.font.render(f"Points: {int(self.points)}", 1, gf.white)
        self.__screen.blit(self.point_display,
                           (gf.screen_width // 2 - self.point_display.get_width() // 2, gf.screen_height // 100))
        self.__screen.blit(self.__controls_instructions, (gf.screen_width // 20, gf.screen_height // 1.07))
        self.__screen.blit(self.__controls_instructions_txt, (gf.screen_width // 10, gf.screen_height // 1.05))

        # stuff to put on the hud if not in tutorial
        if not self.tutorial_mode:
            self.level_number_text = self.__controls_font.render(
                f"Level {self.level_number}/{gf.number_of_levels + 1}", 1, gf.white)
            self.__screen.blit(self.level_number_text,
                               (gf.screen_width // 2 - self.level_number_text.get_width() // 2,
                                         gf.screen_height // 10))

    def get_high_score(self):
        """
        Description:
            Reads the character high score file, and writes a new high score to the file if achieved
        """
        with open("high_score.txt", "r+") as high_score_file:  # if file is empty, set score to 0
            if high_score_file.read() == "":
                high_score_file.write("0")

        with open("high_score.txt", "r") as high_score_file:  # reads the file for the high score
            self.high_score = int(high_score_file.read())

        # if the points the user has is greater than the high score, then it becomes the high score
        if self.points > self.high_score:
            self.high_score = int(self.points)
            with open("high_score.txt", "w") as high_score_file:
                high_score_file.write(str(self.high_score))

    def update(self):  # runs everything
        """
        Description:
            Runs most methods, so that the character is constantly updates every frame
        """
        self.__character_input()
        self.__damage_cooldown()
        self.__animation()
        self.__frame_updates()
        self.__character_movement()
        self.__powerup_timer()
        self.__points_timer()
        self.__heads_up_display()
