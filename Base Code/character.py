import pygame, os, sys
from globalfunctions import screen_width, screen_height, import_graphics_dict
import numpy
from math import cos
from sword import Sword
from camera import GameCamera

class Character(pygame.sprite.Sprite):
    def __init__(self, pos, groups, wall_sprites, powerup_sprites, coin_sprites,health_pot_sprites,exit_sprites, sword_sprites):
        super().__init__(groups)
        # general setup
        self.key_press = pygame.key.get_pressed()
        self.tutorial_mode = False
        self.level_up = False  # have we reached the end of the level
        self.level_number = 1
        self.display_surface = pygame.display.get_surface()
        self.white = (255, 255, 255)
        self.font = pygame.font.Font("../Fonts/Pixel.ttf", 100)
        self.collision_direction = None

        # obstacles collision
        self.wall_sprites = wall_sprites
        self.powerup_sprites = powerup_sprites
        self.coin_sprites = coin_sprites
        self.exit_sprites = exit_sprites
        self.heath_pot_sprites = health_pot_sprites
        self.sword_sprites = sword_sprites
        self.game_camera = groups

        # player setup
        self.pos = pos
        self.rect_width = 50
        self.rect_height = 64
        self.character_width = 200
        self.character_height = 160

        # player animation state
        self.right = True
        self.left = False
        self.up = False
        self.down = False
        self.sprinting = False
        self.frame = 0
        self.attacking_frame = 0
        self.frame_speed = 0.1
        self.attacking_frame_speed = 0.1

        # movement
        self.speed = 5
        self.movement_vector = pygame.math.Vector2()
        self.max_stamina = 1500
        self.stamina = self.max_stamina

        # attacks
        # TUTORIAL CODE ---
        self.attack_state = False
        self.time_of_attack = None

        # TUTORIAL CODE ---

        self.character_damage = 25


        # powerup timer
        self.powerup_active = 0
        self.powerup_timer_image = pygame.image.load(
            f"../Graphics/powerups/speedpowerup1.png").convert_alpha()  # making a standard square surface

        # stats
        self.max_health = 700
        self.health = self.max_health
        self.points = 501
        self.in_level = True

        # damage timer
        self.can_be_damaged = True
        self.time_damaged = None
        self.max_damage_time = 1000

        # stats animation dictionary
        self.stats_animation_dict = {"health":[], "stamina":[]}
        self.stats_animation_dict = import_graphics_dict("stats", self.stats_animation_dict,"../Graphics")

        # making the character
        self.animation_dict = {"attack_down": [], "attack_right": [], "attack_up": [],
                           "idle_down": [], "idle_right": [], "idle_up": [],
                           "moving_down": [], "moving_right": [], "moving_up": []}

        self.animation_dict = import_graphics_dict("character", self.animation_dict, "../Graphics")
        self.state = "idle_right"  # default states
        self.character_direction = "down"
        self.image = self.animation_dict[self.state][self.frame]
        self.image = pygame.transform.scale(self.image, (self.rect_width, self.rect_height))
        self.rect = self.image.get_rect(topleft=pos)
        self.move_count = 0

        # walking audio
        self.walk_sound = pygame.mixer.Sound("../Audio/walk_sound.mp3")

        # other hud info
        self.controls_font = pygame.font.Font("../Fonts/Pixel.ttf", 30)
        self.controls_instructions = pygame.image.load("../Graphics/controls/controls_instruction.png").convert_alpha()
        self.controls_instructions = pygame.transform.scale(self.controls_instructions, (50,50))
        self.controls_instructions_txt = self.controls_font.render("Controls",1,self.white)


    def stop_attacks(self):
        if self.current_attack:
            self.current_attack.kill()

    def cause_attacks(self):
        self.positions = [self.rect.midright, self.rect.midleft, self.rect.midbottom, self.rect.midtop]
        self.current_attack = Sword(self.character_direction, self.positions, [self.game_camera, self.sword_sprites])


    def character_input(self):
        key_press = pygame.key.get_pressed()

        # movement
        if key_press[pygame.K_w]:
            self.movement_vector.y = -1
            self.character_direction = "up"

        elif key_press[pygame.K_s]:
            self.movement_vector.y = 1
            self.character_direction = "down"
        else:
            self.movement_vector.y = 0

        if key_press[pygame.K_d]:
            self.movement_vector.x = 1
            self.character_direction = "right"

        elif key_press[pygame.K_a]:
            self.movement_vector.x = -1
            self.character_direction = "left"

        else:
            self.movement_vector.x = 0

        # ATTACK INPUT
        if not self.attack_state:
            if key_press[pygame.K_SPACE]:
                self.attack_state = True
                self.time_of_attack = pygame.time.get_ticks()
                self.cause_attacks()
                self.attacking_frame = 0

        # sprint
        if key_press[pygame.K_LSHIFT] and self.stamina > 120 and (self.movement_vector.x != 0 or self.movement_vector.y != 0) and self.speed <= 10:  # if sprinting, and we have enough stamina
            self.speed = 10
            self.sprinting = True
            self.stamina -= 5
            if self.stamina <= 120:  # cutoff at 120, so that they cant sprint immediately after running out of stamina
                self.stamina = 0

        else:
            self.speed = 5
            self.sprinting = False
            if self.stamina < self.max_stamina:
                self.stamina += 6

        # code here round our value of stamina to the nearest 100, and puts in a format to be blitted to screen
        if len(str(self.stamina)) == 4:
            round_number = numpy.format_float_positional(self.stamina, precision=2, unique=False, fractional=False)

        else:
            round_number = numpy.format_float_positional(self.stamina, precision=1, unique=False, fractional=False)

        stamina_lst = []

        for i in range(len(round_number) - 1):
            stamina_lst.append(round_number[i])

        self.stamina_joined = "".join(stamina_lst)


        if self.powerup_active > 0:  # if a powerup is active, -1 for each frame, and give player speed boost
            self.powerup_active -= 1
            self.speed = 15


    def player_movement(self):
        # TUTORIAL CODE ---
        if self.movement_vector.magnitude() != 0:  # if vector has length
            self.movement_vector = self.movement_vector.normalize()  # set length of vector to 1 no matter what direction

        self.rect.x += self.movement_vector.x * self.speed
        self.collision_direction = "x"
        self.collisions_check()
        self.rect.y += self.movement_vector.y * self.speed
        self.collision_direction = "y"
        self.collisions_check()
        # TUTORIAL CODE ---

        if self.move_count == 1:
            self.walk_sound.play(999)  # if we start to walk, then play walking sound
            self.walk_sound.set_volume(0.5)
        self.move_count += 1

        if self.movement_vector == [0,0]:
            self.walk_sound.stop()  # once we stop walking, stop the walking playing sound
            self.move_count = 0



    def damage_cooldown(self):
        game_loop_time = pygame.time.get_ticks()
        if self.attack_state and round(self.attacking_frame, 1) == 3.9:
            self.stop_attacks()
            self.attack_state = False

        if not self.can_be_damaged and game_loop_time - self.time_damaged >= self.max_damage_time:
                self.can_be_damaged = True

    def collisions_check(self):
        # TUTORIAL CODE ---
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
        # TUTORIAL CODE ---

        # POWERUPS
        if self.collision_direction in "xy":
            for sprite in self.powerup_sprites:
                if sprite.rect.colliderect(self.rect):  # collision with powerup, and kills the sprite when they collide
                    self.powerup_active = 300  # powerups last for 5 seconds (300 frames)
                    powerup_sound = pygame.mixer.Sound("../Audio/speed_powerup.mp3")  # plays powerup noise
                    powerup_sound.play()
                    powerup_sound.set_volume(0.5)
                    sprite.kill()

        # COINS
        if self.collision_direction in "xy":
            for sprite in self.coin_sprites:
                if sprite.rect.colliderect(self.rect):
                    # SOUND
                    coin_sound = pygame.mixer.Sound("../Audio/coin.mp3")
                    coin_sound.play()
                    coin_sound.set_volume(0.5)

                    # POINTS
                    self.points += 20
                    sprite.kill()

        # HEALTH POTION
        if self.collision_direction in "xy":
            for sprite in self.heath_pot_sprites:
                if sprite.rect.colliderect(self.rect):
                    # SOUND
                    health_pot_sound = pygame.mixer.Sound("../Audio/health_pot.mp3")
                    health_pot_sound.play()
                    health_pot_sound.set_volume(0.5)

                    # POINTS
                    if self.max_health != self.health:
                        self.health += 100
                    sprite.kill()

        # EXIT
        if self.collision_direction in "xy":
            for sprite in self.exit_sprites:
                if sprite.rect.colliderect(self.rect):
                    if not self.level_up:
                        self.level_number += 1
                        self.level_up = True


                    portal_sound = pygame.mixer.Sound("../Audio/portal.mp3")
                    portal_sound.play()
                    self.walk_sound.stop()  # makes sure walking sound stops
                    portal_sound.set_volume(0.1)

                    self.in_level = False
                    sprite.kill()


    def powerup_timer(self):
        # fonts and colours
        if self.powerup_active != 0:
            # powerup graphic
            self.powerup_timer_image = pygame.transform.scale(self.powerup_timer_image, (100, 100))
            self.display_surface.blit(self.powerup_timer_image, (screen_width // 15, screen_height // 1.2))

            # powerup timer count
            timer = self.font.render(str(self.powerup_active), 1, self.white)
            self.display_surface.blit(timer, (screen_width // 10 - timer.get_width()//2, screen_height // 1.2))

    def frame_updates(self):
        # standard animation update
        self.frame += self.frame_speed
        if self.frame >= len(self.animation_dict["idle_right"]):  # could be any folder, but took the first one
            self.frame = 0

        # special attack animation update
        self.attacking_frame += self.attacking_frame_speed
        if self.attacking_frame >= len(self.animation_dict["attack_down"]):
            self.attacking_frame = 0

        # check for powerup
        if self.speed >= 15:
            self.frame_speed = 0.5

        # check for sprint
        elif self.key_press[pygame.K_LSHIFT] and self.stamina > 120 and (self.movement_vector.x != 0 or self.movement_vector.y != 0):
            self.frame_speed = 0.2

        # walking speed
        else:
            self.frame_speed = 0.1


    def animation(self):
        self.key_press = pygame.key.get_pressed()
        # attacking
        if self.attack_state:
            if self.character_direction == "left":
                self.state = f"attack_right"  # as "left" needs to be "right" first, then transformed
            else:
                self.state = f"attack_{self.character_direction}"
            self.image = self.animation_dict[self.state][int(self.attacking_frame)]

        # moving
        elif self.key_press[pygame.K_s] or self.key_press[pygame.K_d] or self.key_press[pygame.K_a] or self.key_press[pygame.K_w]:
            if self.character_direction == "left":
                self.state = f"moving_right"
            else:
                self.state = f"moving_{self.character_direction}"
            self.image = self.animation_dict[self.state][int(self.frame)]

        # idle
        else:
            if self.character_direction == "left":
                self.state = f"idle_right"

            else:
                self.state = f"idle_{self.character_direction}"
            self.image = self.animation_dict[self.state][int(self.frame)]


        # making the image
        if self.character_direction == "left":  # if facing left, as need to flip image
            self.image = pygame.transform.flip(self.image, True, False)

        self.image = pygame.transform.scale(self.image, (self.character_width, self.character_height))  # resizing image

        # player flicker on hit
        flicker = cos(0.1 * pygame.time.get_ticks())
        if not self.can_be_damaged and flicker < 0:
            self.image.set_alpha(255)

        elif not self.can_be_damaged:
            self.image.set_alpha(50)

        else:
            self.image.set_alpha(255)


    def points_timer(self):
        self.points -= (1/60)

    def damage_enemy(self):
        self.points += 5  # you get 5 points on enemy hit
        return self.character_damage

    def heads_up_display(self):
        #  putting stats on the screen (health and stamina)
        stamina_index = (int(self.stamina_joined)//100)
        health_index = (self.health//100)

        self.stamina_image = self.stats_animation_dict["stamina"][stamina_index]
        self.stamina_image = pygame.transform.scale(self.stamina_image, (400, 80))
        self.display_surface.blit(self.stamina_image, (screen_width//70, screen_height // 5))

        self.health_image = self.stats_animation_dict["health"][health_index]
        self.health_image = pygame.transform.scale(self.health_image, (300,50))
        self.display_surface.blit(self.health_image, (screen_width//70, screen_height // 7))


        # putting points on the screen
        self.point_display = self.font.render(f"Points: {int(self.points)}", 1, self.white)
        self.display_surface.blit(self.point_display, (screen_width // 2 - self.point_display.get_width() // 2, screen_height // 100))
        self.display_surface.blit(self.controls_instructions, (screen_width//20, screen_height//1.07))
        self.display_surface.blit(self.controls_instructions_txt, (screen_width//10, screen_height//1.05))

        # stuff to put on the hud if not in tutorial
        if not self.tutorial_mode:
            self.level_number_text = self.controls_font.render(f"Level {self.level_number}/8", 1, self.white)
            self.display_surface.blit(self.level_number_text,
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
        self.character_input()
        self.damage_cooldown()
        self.animation()
        self.frame_updates()
        self.player_movement()
        self.powerup_timer()
        self.points_timer()
        self.heads_up_display()



