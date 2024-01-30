import pygame, os, sys
from settings import screen_width, screen_height, weapon_data
import numpy
import time
from math import cos
from support import *
from gameover import GameOver

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, powerup_sprites, coin_sprites,health_pot_sprites,exit_sprites , create_attack, destroy_attack):
        super().__init__(groups)
        # general setup
        self.key_press = pygame.key.get_pressed()
        self.tutorial_mode = False

        # player setup
        self.pos = pos
        self.rect_width = 50
        self.rect_height = 64
        self.player_width = 200
        self.player_height = 160


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
        self.direction = pygame.math.Vector2()
        self.max_stamina = 1500

        # attacks
        self.attacking = False
        self.attack_cooldown = 300
        self.attack_time = None
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]

        # sprint
        self.stamina = self.max_stamina
        self.display_surface = pygame.display.get_surface()
        self.white = (255, 255, 255)
        self.font = pygame.font.Font("../Fonts/Pixel.ttf", 100)

        self.stamina_lst = []  # getting files for stamina
        for file in os.listdir("../Graphics/stamina/"):
            self.stamina_lst.append(file)

        self.health_lst = []
        for file in os.listdir("../Graphics/health/"):
            self.health_lst.append(file)


        # obstacles collision
        self.obstacle_sprites = obstacle_sprites
        self.powerup_sprites = powerup_sprites
        self.coin_sprites = coin_sprites
        self.exit_sprites = exit_sprites
        self.heath_pot_sprites = health_pot_sprites

        # powerups
        self.powerup_active = 0

        # stats
        self.stats = {"health":700, "attack":10}
        self.health = self.stats["health"]
        self.max_health = self.stats["health"]
        self.points = 501
        self.in_level = True

        # damage timer
        self.can_damage = True
        self.hurt_time = None
        self.invulnerability_duration = 1000

        # making the character
        self.import_graphics()
        self.state = "idle_right"  # default states
        self.player_direction = "down"
        self.image = self.animations[self.state][self.frame]
        self.image = pygame.transform.scale(self.image, (self.rect_width, self.rect_height))
        self.rect = self.image.get_rect(topleft=pos)

        self.move_count = 0

        # walking audio
        self.walk_sound = pygame.mixer.Sound("../Audio/walk_sound.mp3")

        # other hud stuff
        controls_font = pygame.font.Font("../Fonts/Pixel.ttf", 30)
        self.controls_instructions = pygame.image.load("../Graphics/controls/controls_instruction.png").convert_alpha()
        self.controls_instructions = pygame.transform.scale(self.controls_instructions, (50,50))
        self.controls_instructions_txt = controls_font.render("Controls",1,self.white)



    def import_graphics(self):
        self.animations = {"attack_down":[],"attack_right":[],"attack_up":[],
                           "idle_down":[],"idle_right":[],"idle_up":[],
                           "moving_down":[], "moving_right":[], "moving_up":[]}

        main_path = f"../Graphics/character/"
        for animation_type in self.animations.keys():  # for idle in dictionary: (loops through and imports everything)
            # import folder from support file
            self.animations[animation_type] = import_folder(main_path + animation_type)



    def input(self):
        keys = pygame.key.get_pressed()

        # movement
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.up = True
            self.down = False
            self.left = False
            self.right = False
            self.player_direction = "up"

        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.up = False
            self.down = True
            self.left = False
            self.right = False
            self.player_direction = "down"
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.up = False
            self.down = False
            self.left = False
            self.right = True
            self.player_direction = "right"

        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.up = False
            self.down = False
            self.left = True
            self.right = False
            self.player_direction = "left"

        else:
            self.direction.x = 0

        # ATTACK INPUT
        if not self.attacking:
        
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.attacking_frame = 0

        # sprint
        if keys[pygame.K_LSHIFT] and self.stamina > 120 and (self.direction.x != 0 or self.direction.y != 0) and self.speed <= 10:  # if sprinting, and we have enough stamina
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


    def move(self, speed):
        if self.direction.magnitude() != 0:  # if vector has length
            self.direction = self.direction.normalize()  # set length of vector to 1 no matter what direction

        self.rect.x += self.direction.x * speed
        self.collision("horizontal")
        self.rect.y += self.direction.y * speed
        self.collision("vertical")

        if self.move_count == 1:
            self.walk_sound.play(999)  # if we start to walk, then play walking sound
            self.walk_sound.set_volume(0.5)
        self.move_count += 1


        if self.direction == [0,0]:
            self.walk_sound.stop()  # once we stop walking, stop the walking playing sound
            self.move_count = 0



    def cooldown(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            #if current_time - self.attack_time >= 378 + weapon_data[self.weapon]["cooldown"]:
            #    self.destroy_attack()
            #    self.attacking = False
            if round(self.attacking_frame, 1) == 3.9:
                self.destroy_attack()
                self.attacking = False


        if not self.can_damage:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.can_damage = True



    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:  # moving right
                        self.rect.right = sprite.rect.left

                    if self.direction.x < 0:  # moving left
                        self.rect.left = sprite.rect.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:  # moving down
                        self.rect.bottom = sprite.rect.top

                    if self.direction.y < 0:  # moving up
                        self.rect.top = sprite.rect.bottom

        # POWERUPS
        if direction == "vertical" or direction == "horizontal":
            for sprite in self.powerup_sprites:
                if sprite.rect.colliderect(self.rect):  # collision with powerup, and kills the sprite when they collide
                    self.powerup_active = 300  # powerups last for 5 seconds (300 frames)
                    powerup_sound = pygame.mixer.Sound("../Audio/speed_powerup.mp3")  # plays powerup noise
                    powerup_sound.play()
                    powerup_sound.set_volume(0.5)
                    sprite.kill()

        # COINS
        if direction == "vertical" or direction == "horizontal":
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
        if direction == "vertical" or direction == "horizontal":
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
        if direction == "vertical" or direction == "horizontal":
            for sprite in self.exit_sprites:
                if sprite.rect.colliderect(self.rect):
                    portal_sound = pygame.mixer.Sound("../Audio/portal.mp3")
                    portal_sound.play()
                    self.walk_sound.stop()  # makes sure walking sound stops
                    portal_sound.set_volume(0.1)

                    self.in_level = False


                    # CLOSE GAME
                    #pygame.quit()
                    #sys.exit()


    def powerup_timer(self):
        # fonts and colours
        if self.powerup_active != 0:
            # powerup graphic
            self.powerup_timer_image = pygame.image.load(
                f"../Graphics/powerups/speedpowerup1.png").convert_alpha()  # making a standard square surface
            self.powerup_timer_image = pygame.transform.scale(self.powerup_timer_image, (100, 100))
            self.display_surface.blit(self.powerup_timer_image, (screen_width // 15, screen_height // 1.2))

            # powerup timer count
            timer = self.font.render(str(self.powerup_active), 1, self.white)
            self.display_surface.blit(timer, (screen_width // 10 - timer.get_width()//2, screen_height // 1.2))


    def animation_files(self, path):
        # returns a list of all files needed for animation, used in animation() function
        file_lst = []
        for file in os.listdir(path):
            file_lst.append(file)
        return file_lst


    def frame_updates(self):
        # standard animation update
        self.frame += self.frame_speed
        if self.frame >= len(self.animations["idle_right"]):  # could be any folder, but took the first one
            self.frame = 0

        # special attack animation update
        self.attacking_frame += self.attacking_frame_speed
        if self.attacking_frame >= len(self.animations["attack_down"]):
            self.attacking_frame = 0

        # check for powerup
        if self.speed >= 15:
            self.frame_speed = 0.5

        # check for sprint
        elif self.key_press[pygame.K_LSHIFT] and self.stamina > 120 and (self.direction.x != 0 or self.direction.y != 0):
            self.frame_speed = 0.2

        # walking speed
        else:
            self.frame_speed = 0.1


    def animation(self):
        self.key_press = pygame.key.get_pressed()
        # attacking (29 PIXELS FOR ATTACK ANIMATION, (50,64) IS STANDARD PLAYER TRANSFORM)
        if self.attacking:
            if self.player_direction == "left":
                self.state = f"attack_right"  # as "left" needs to be "right" first, then transformed
            else:
                self.state = f"attack_{self.player_direction}"
            self.image = self.animations[self.state][int(self.attacking_frame)]

        # moving
        elif self.key_press[pygame.K_s] or self.key_press[pygame.K_d] or self.key_press[pygame.K_a] or self.key_press[pygame.K_w]:
            if self.player_direction == "left":
                self.state = f"moving_right"
            else:
                self.state = f"moving_{self.player_direction}"
            self.image = self.animations[self.state][int(self.frame)]

        # idle
        else:
            if self.player_direction == "left":
                self.state = f"idle_right"

            else:
                self.state = f"idle_{self.player_direction}"
            self.image = self.animations[self.state][int(self.frame)]


        # making the image
        if self.player_direction == "left":  # if facing left, as need to flip image
            self.image = pygame.transform.flip(self.image, True, False)

        self.image = pygame.transform.scale(self.image, (self.player_width, self.player_height))  # resizing image


        # flickering player image when taking damage
        if not self.can_damage:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)

        else:
            self.image.set_alpha(255)

    def wave_value(self):  # for flickering an entity when they take damage
        value = cos(0.1*pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def points_timer(self):
        self.points -= (1/60)

    def points_out(self):
        if self.points <= 0:
            print("---GAME OVER ---!")
            pygame.quit()
            sys.exit()

    def get_full_weapon_damage(self):
        base_damage = self.stats["attack"]
        # weapon_damage NOT included
        weapon_damage = weapon_data[self.weapon]["damage"]
        self.points += 5  # you get 5 points on enemy hit
        return base_damage + weapon_damage

    def heads_up_display(self):
        #  putting stamina on the screen
        stamina_index = (int(self.stamina_joined)//100)
        self.stamina_image = pygame.image.load(f"../Graphics/stamina/stamina{stamina_index}.png").convert_alpha()
        self.stamina_image = pygame.transform.scale(self.stamina_image, (400,80))
        # STAMINA STRING IS CURRENTLY REDUNDANT !!
        self.display_surface.blit(self.stamina_image, (screen_width//70, screen_height // 5))

        # putting points on the screen
        self.point_display = self.font.render(f"Points: {int(self.points)}", 1, self.white)
        self.display_surface.blit(self.point_display, (screen_width // 2 - self.point_display.get_width() // 2, screen_height // 100))

        # putting health on the screen
        self.health_image = pygame.image.load(f"../Graphics/health/health_{self.health}.png").convert_alpha()
        self.health_image = pygame.transform.scale(self.health_image, (300,50))
        self.display_surface.blit(self.health_image,
                                  (screen_width//2 - 575, screen_height // 7))

        self.display_surface.blit(self.controls_instructions, (screen_width//20, screen_height//1.07))
        self.display_surface.blit(self.controls_instructions_txt, (screen_width//10, screen_height//1.05))

    def character_hurt(self):
        if self.health <= 0:
            if not self.tutorial_mode:
                self.get_high_score()
                print(self.high_score)


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
        self.input()
        self.cooldown()
        self.animation()
        self.frame_updates()
        self.move(self.speed)
        self.powerup_timer()
        self.points_timer()
        self.points_out()
        self.character_hurt()
        self.heads_up_display()


