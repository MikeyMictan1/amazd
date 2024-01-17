import pygame
from settings import *
from entity import Entity
from support import *
class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player):
        super().__init__(groups)

        # general setup
        self.sprite_type = "enemy"
        self.pos = pos

        # graphics setup
        self.import_graphics(monster_name)
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]
        self.image = pygame.transform.scale(self.image, (50,64))

        # movement
        self.rect = self.image.get_rect(topleft = self.pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info["health"]
        self.speed = monster_info["speed"]
        self.attack_damage = monster_info["health"]
        self.resistance = monster_info["resistance"]
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player

        # undamageable frames
        self.can_damage = True  # vulnerable
        self.hit_time = None
        self.invincibility_duration = 300



    def import_graphics(self, name):
        self.animations = {"idle":[], "moving":[], "attacking":[]}
        main_path = f"../Graphics/enemy/{name}/"
        for animation_type in self.animations.keys():  # for idle in dictionary: (loops through and imports everything)
            # import folder from support file
            self.animations[animation_type] = import_folder(main_path + animation_type)

    def get_player_distance_direction(self, player):
        enemy_dir = pygame.math.Vector2(self.rect.center)
        player_dir = pygame.math.Vector2(player.rect.center)

        distance = (player_dir - enemy_dir).magnitude()

        if distance > 0:
            direction = (player_dir - enemy_dir).normalize()

        else:
            direction = pygame.math.Vector2()

        return (distance, direction)


    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attacking":
                self.frame_index = 0
            self.status  = "attacking"

        elif distance <= self.notice_radius:
            self.status = "moving"

        else:
            self.status = "idle"

    def actions(self, player):
        if self.status == "attacking":
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage)


        elif self.status == "moving":
            self.direction = self.get_player_distance_direction(player)[1]

        else:
            # once the enemy is no longer in range, their direction goes back to 0
            self.direction = pygame.math.Vector2()


    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attacking":
                self.can_attack = False

            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (50, 64))
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.can_damage:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)

        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.can_damage:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.can_damage = True

    def get_damage(self, player, attack_type):
        if self.can_damage:  # if enemy is vulnerable
            self.direction = self.get_player_distance_direction(player)[1]  # getting enemy direction and moving them in a different direction
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
            else:  # for other damage types
                pass

            self.hit_time = pygame.time.get_ticks()
            self.can_damage = False

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def hit_reaction(self):
        if not self.can_damage:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()


    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)






