import pygame, os, sys
from settings import screen_width, screen_height, weapon_data
import numpy
import time
from math import cos

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, powerup_sprites, coin_sprites,exit_sprites , create_attack, destroy_attack):
        super().__init__(groups)
        # player setup
        self.pos = pos
        self.player_width = 50
        self.player_height = 64
        self.image = pygame.image.load(
            f"../Graphics/character/idle_right/idleright1.png").convert_alpha()  # making a standard square surface
        self.image = pygame.transform.scale(self.image, (50, 64))

        self.rect = self.image.get_rect(topleft=pos)

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
        self.player_direction = ""

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

        # powerups
        self.powerup_active = 0

        # stats
        self.stats = {"health":700, "attack":10}
        self.health = self.stats["health"]
        self.points = 501
        self.in_level = True

        # damage timer
        self.can_damage = True
        self.hurt_time = None
        self.invulnerability_duration = 1000

        # animation attack files
        self.attack_right = ('../Graphics/character/attack_right/')
        self.attack_right_lst = self.animation_files(self.attack_right)

        self.attack_down = ('../Graphics/character/attack_down/')
        self.attack_down_lst = self.animation_files(self.attack_down)

        self.attack_up = ('../Graphics/character/attack_up/')
        self.attack_up_lst = self.animation_files(self.attack_down)

    def input(self):
        keys = pygame.key.get_pressed()

        # movement
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.up = True
            self.down = False
            self.left = False
            self.right = False
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.up = False
            self.down = True
            self.left = False
            self.right = False
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.up = False
            self.down = False
            self.left = False
            self.right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.up = False
            self.down = False
            self.left = True
            self.right = False
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
                    coin_sound = pygame.mixer.Sound("../Audio/powerup.mp3")
                    coin_sound.play()
                    coin_sound.set_volume(0.1)
                    print("Coin Collision!")

                    # POINTS
                    self.points += 20
                    sprite.kill()

        # EXIT
        if direction == "vertical" or direction == "horizontal":
            for sprite in self.exit_sprites:
                if sprite.rect.colliderect(self.rect):
                    self.in_level = False
                    print("Exit Collision!")

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

    def animation(self):
        keys = pygame.key.get_pressed()
        # all animation files
        # idle
        idle_right_path = ('../Graphics/character/idle_right/')
        idle_right_lst = self.animation_files(idle_right_path)

        idle_down_path = ('../Graphics/character/idle_down/')
        idle_down_lst = self.animation_files(idle_down_path)

        idle_up_path = ('../Graphics/character/idle_up/')
        idle_up_lst = self.animation_files(idle_up_path)

        # moving
        moving_right_path = ('../Graphics/character/moving_right/')
        moving_right_lst = self.animation_files(moving_right_path)

        moving_down_path = ('../Graphics/character/moving_down/')
        moving_down_lst = self.animation_files(moving_down_path)

        moving_up_path = ('../Graphics/character/moving_up/')
        moving_up_lst = self.animation_files(moving_up_path)

        # standard animation update
        self.frame += self.frame_speed
        if self.frame >= len(idle_right_lst):  # could be any folder, but took the first one
            self.frame = 0

        # special attack animation update
        self.attacking_frame += self.attacking_frame_speed
        if self.attacking_frame >= len(self.attack_right_lst):
            self.attacking_frame = 0


        # check for powerup
        if self.speed >= 15:
            self.frame_speed = 0.5

        # check for sprint
        elif keys[pygame.K_LSHIFT] and self.stamina > 120 and (self.direction.x != 0 or self.direction.y != 0):
            self.frame_speed = 0.2

        # walking speed
        else:
            self.frame_speed = 0.1


        # making the player face different ways
        new_width = 200
        new_height = 160
        # attacking (29 PIXELS FOR ATTACK ANIMATION, (50,64) IS STANDARD PLAYER TRANSFORM)
        if self.right and self.attacking == True:
            self.player_direction = "right"
            self.image = pygame.image.load(f"{self.attack_right}{self.attack_right_lst[int(self.attacking_frame)]}").convert_alpha()
            self.image = pygame.transform.scale(self.image, (new_width, new_height))

        elif self.left and self.attacking == True:
            self.player_direction = "left"
            self.image = pygame.image.load(f"{self.attack_right}{self.attack_right_lst[int(self.attacking_frame)]}").convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (new_width, new_height))

        elif self.down and self.attacking == True:
            self.player_direction = "down"
            self.image = pygame.image.load(f"{self.attack_down}{self.attack_down_lst[int(self.attacking_frame)]}").convert_alpha()
            self.image = pygame.transform.scale(self.image, (new_width, new_height))

        elif self.up and self.attacking == True:
            self.player_direction = "up"
            self.image = pygame.image.load(
                f"{self.attack_up}{self.attack_up_lst[int(self.attacking_frame)]}").convert_alpha()
            self.image = pygame.transform.scale(self.image, (new_width, new_height))


            #self.image = pygame.transform.scale_by(self.image, 2.2)
            #self.rect = self.image.get_rect(topright=self.pos)


        # moving
        elif self.down and keys[pygame.K_s]:
            self.player_direction = "down"
            self.image = pygame.image.load(f"{moving_down_path}{moving_down_lst[int(self.frame)]}").convert_alpha()
            self.image = pygame.transform.scale(self.image, (new_width, new_height))

        elif self.right and keys[pygame.K_d]:
            self.player_direction = "right"
            self.image = pygame.image.load(f"{moving_right_path}{moving_right_lst[int(self.frame)]}").convert_alpha()
            self.image = pygame.transform.scale(self.image, (new_width, new_height))

        elif self.left and keys[pygame.K_a]:
            self.player_direction = "left"
            print("FRAME: {self.frame}")
            self.image = pygame.image.load(f"{moving_right_path}{moving_right_lst[int(self.frame)]}").convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (new_width, new_height))

        elif self.up and keys[pygame.K_w]:
            self.player_direction = "up"
            self.image = pygame.image.load(f"{moving_up_path}{moving_up_lst[int(self.frame)]}").convert_alpha()
            self.image = pygame.transform.scale(self.image, (new_width, new_height))


        # idling
        elif self.down:
            self.player_direction = "down"
            self.image = pygame.image.load(f"{idle_down_path}{idle_down_lst[int(self.frame)]}").convert_alpha()
            self.image = pygame.transform.scale(self.image, (new_width, new_height))

        elif self.right:
            self.player_direction = "right"
            self.image = pygame.image.load(f"{idle_right_path}{idle_right_lst[int(self.frame)]}").convert_alpha()
            self.image = pygame.transform.scale(self.image, (new_width, new_height))

        elif self.left:
            self.player_direction = "left"
            self.image = pygame.image.load(f"{idle_right_path}{idle_right_lst[int(self.frame)]}").convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (new_width, new_height))

        elif self.up:
            self.player_direction = "up"
            self.image = pygame.image.load(f"{idle_up_path}{idle_up_lst[int(self.frame)]}").convert_alpha()
            self.image = pygame.transform.scale(self.image, (new_width, new_height))

        # ---------

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

    def character_hurt(self):
        if self.health <= 0:
            pygame.quit()
            sys.exit()

    def update(self):
        self.input()
        self.cooldown()
        self.animation()
        self.move(self.speed)
        self.powerup_timer()
        self.points_timer()
        self.points_out()
        self.character_hurt()
        self.heads_up_display()
        print("-----------")
        print(f"Attacking frame: {round(self.attacking_frame, 1)}")
        print(f"Animation frame: {self.attacking_frame}")
        print(f"are we attacking: {self.attacking}")



