import pygame
from globalfunctions import *
import numpy
from math import cos
from sword import Sword

class Character(pygame.sprite.Sprite):
    def __init__(self, pos, groups, wall_sprites, powerup_sprites, coin_sprites,health_pot_sprites,exit_sprites, sword_sprites):
        super().__init__(groups)
        # general setup
        self.__key_press = pygame.key.get_pressed()
        self.tutorial_mode = False
        self.__level_up = False  # have we reached the end of the level
        self.level_number = 1
        self.__display_surface = pygame.display.get_surface()
        self.__collision_direction = None

        # obstacles collision
        self.__wall_sprites = wall_sprites
        self.__powerup_sprites = powerup_sprites
        self.__coin_sprites = coin_sprites
        self.__exit_sprites = exit_sprites
        self.__heath_pot_sprites = health_pot_sprites
        self.__sword_sprites = sword_sprites
        self.__game_camera = groups

        # player setup
        self.__pos = pos
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
        # TUTORIAL CODE ---
        self.__is_attacking = False
        self.__time_of_attack = None

        # TUTORIAL CODE ---
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
        self.__stats_animation_dict = {"health":[], "stamina":[]}
        self.__stats_animation_dict = import_graphics_dict("stats", self.__stats_animation_dict, "../Graphics")

        # making the character
        self.__animation_dict = {"attack_down": [], "attack_right": [], "attack_up": [],
                           "idle_down": [], "idle_right": [], "idle_up": [],
                           "moving_down": [], "moving_right": [], "moving_up": []}

        self.__animation_dict = import_graphics_dict("character", self.__animation_dict, "../Graphics")
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
        self.__controls_instructions = pygame.image.load("../Graphics/controls/controls_instruction.png").convert_alpha()
        self.__controls_instructions = pygame.transform.scale(self.__controls_instructions, (50, 50))
        self.__controls_instructions_txt = self.__controls_font.render("Controls", 1, white)

    def __cause_attacks(self):
        self.__is_attacking = True
        self.__time_of_attack = pygame.time.get_ticks()
        self.__positions = [self.rect.midright, self.rect.midleft, self.rect.midbottom, self.rect.midtop]
        self.__sword = Sword(self.__character_direction, self.__positions, [self.__game_camera, self.__sword_sprites])
        self.__attacking_frame = 0


    def __character_input(self):
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
        if __key_press[pygame.K_LSHIFT] and self.__stamina > 120 and (self.__movement_vector.x != 0 or self.__movement_vector.y != 0) and self.__speed <= 10:  # if sprinting, and we have enough stamina
            self.__speed = 10
            self.__sprinting = True
            self.__stamina -= 5
            if self.__stamina <= 120:  # cutoff at 120, so that they cant sprint immediately after running out of stamina
                self.__stamina = 0

        else:
            self.__speed = 5
            self.__sprinting = False
            if self.__stamina < self.__max_stamina:
                self.__stamina += 6

        # code here round our value of stamina to the nearest 100, and puts in a format to be blitted to screen
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
        # TUTORIAL CODE ---
        if self.__movement_vector.magnitude() != 0:  # if vector has length
            self.__movement_vector = self.__movement_vector.normalize()  # set length of vector to 1 no matter what direction

        self.rect.x += self.__movement_vector.x * self.__speed
        self.__collision_direction = "x"
        self.__collisions_check()
        self.rect.y += self.__movement_vector.y * self.__speed
        self.__collision_direction = "y"
        self.__collisions_check()
        # TUTORIAL CODE ---

        if self.__move_count == 1:
            self.__walk_sound.play(999)  # if we start to walk, then play walking sound
            self.__walk_sound.set_volume(0.5)
        self.__move_count += 1

        if self.__movement_vector == [0, 0]:
            self.__walk_sound.stop()  # once we stop walking, stop the walking playing sound
            self.__move_count = 0



    def __damage_cooldown(self):
        game_loop_time = pygame.time.get_ticks()
        if self.__is_attacking and round(self.__attacking_frame, 1) == 3.9:
            self.__sword.kill()
            self.__is_attacking = False

        if not self.can_be_damaged and game_loop_time - self.time_damaged >= self.max_damage_time:
                self.can_be_damaged = True

    def __collisions_check(self):
        # TUTORIAL CODE ---
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
        # TUTORIAL CODE ---

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
            for sprite in self.__heath_pot_sprites:
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
        # fonts and colours
        if self.__powerup_active:
            # powerup graphic
            self.__powerup_timer_image = pygame.transform.scale(self.__powerup_timer_image, (100, 100))
            self.__display_surface.blit(self.__powerup_timer_image, (screen_width // 15, screen_height // 1.2))

            # powerup timer count
            timer = font.render(str(self.__powerup_active), 1, white)
            self.__display_surface.blit(timer, (screen_width // 10 - timer.get_width() // 2, screen_height // 1.2))

    def __frame_updates(self):
        # standard animation update
        self.__frame += self.__frame_speed
        if self.__frame >= len(self.__animation_dict["idle_right"]):  # could be any folder, but took the first one
            self.__frame = 0

        # special attack animation update
        self.__attacking_frame += self.__attacking_frame_speed
        if self.__attacking_frame >= len(self.__animation_dict["attack_down"]):
            self.__attacking_frame = 0

        # check for powerup
        if self.__powerup_active:
            self.__frame_speed = 0.5

        # check for sprint
        elif self.__sprinting:
            self.__frame_speed = 0.2

        # walking speed
        else:
            self.__frame_speed = 0.1


    def __animation(self):
        self.__key_press = pygame.key.get_pressed()
        # --- ATTACKING ANIMATION ---
        if self.__is_attacking:
            self.image = self.__animation_dict[self.__get_animation_state("attack")][int(self.__attacking_frame)]

        # --- MOVING ANIMATION ---
        elif self.__key_press[pygame.K_s] or self.__key_press[pygame.K_d] or self.__key_press[pygame.K_a] or self.__key_press[pygame.K_w]:
            self.image = self.__animation_dict[self.__get_animation_state("moving")][int(self.__frame)]

        # --- IDLE ANIMATION ---
        else:
            self.image = self.__animation_dict[self.__get_animation_state("idle")][int(self.__frame)]


        # making the image
        if self.__character_direction == "left":  # if facing left, as need to flip image
            self.image = pygame.transform.flip(self.image, True, False)

        self.image = pygame.transform.scale(self.image, (self.__character_width, self.__character_height))  # resizing image

        # player flicker on hit
        flicker = cos(0.1 * pygame.time.get_ticks())
        if not self.can_be_damaged and flicker > 0:
            self.image.set_alpha(50)

        else:
            self.image.set_alpha(255)

    def __get_animation_state(self, state):
        if self.__character_direction == "left":
            animation_type = f"{state}_right"
        else:
            animation_type = f"{state}_{self.__character_direction}"

        return animation_type

    def __points_timer(self):
        self.points -= (1/60)

    def damage_enemy(self):
        self.points += 5  # you get 5 points on enemy hit
        return self.__character_damage

    def __heads_up_display(self):
        #  putting stats on the screen (health and stamina)
        stamina_index = (int(self.stamina_joined)//100)
        health_index = (self.health//100)

        self.stamina_image = self.__stats_animation_dict["stamina"][stamina_index]
        self.stamina_image = pygame.transform.scale(self.stamina_image, (400, 80))
        self.__display_surface.blit(self.stamina_image, (screen_width // 70, screen_height // 5))

        self.health_image = self.__stats_animation_dict["health"][health_index]
        self.health_image = pygame.transform.scale(self.health_image, (300,50))
        self.__display_surface.blit(self.health_image, (screen_width // 70, screen_height // 7))


        # putting points on the screen
        self.point_display = font.render(f"Points: {int(self.points)}", 1, white)
        self.__display_surface.blit(self.point_display, (screen_width // 2 - self.point_display.get_width() // 2, screen_height // 100))
        self.__display_surface.blit(self.__controls_instructions, (screen_width // 20, screen_height // 1.07))
        self.__display_surface.blit(self.__controls_instructions_txt, (screen_width // 10, screen_height // 1.05))

        # stuff to put on the hud if not in tutorial
        if not self.tutorial_mode:
            self.level_number_text = self.__controls_font.render(f"Level {self.level_number}/{number_of_levels + 1}", 1, white)
            self.__display_surface.blit(self.level_number_text,
                                        (screen_width // 2 - self.level_number_text.get_width() // 2, screen_height // 10))


    def get_high_score(self):
        with open("high_score.txt", "r+") as high_score_file:  # if file is empty, set score to 0
            if high_score_file.read() == "":
                high_score_file.write("0")

        with open("high_score.txt", "r") as high_score_file:  # reads the file for the high score
            self.high_score = int(high_score_file.read())

        if self.points > self.high_score:  # if the points the user has is greater than the high score, then it becomes the high score
            self.high_score = int(self.points)
            with open("high_score.txt", "w") as high_score_file:
                high_score_file.write(str(self.high_score))


    def update(self):
        self.__character_input()
        self.__damage_cooldown()
        self.__animation()
        self.__frame_updates()
        self.__character_movement()
        self.__powerup_timer()
        self.__points_timer()
        self.__heads_up_display()



