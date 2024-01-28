import pygame

tile_size = 150
screen_width = 1200
screen_height = 6 * tile_size  # 21 is len(maze_lst)
FPS = 60


# weapons
weapon_data = {
    "sword":{"cooldown":100, "damage":15, "graphic":"../Graphics/weapon/full.png"}
}

# enemy

monster_data = {"skeleton":
                    {"health":100, "damage":100, "speed":3, "resistance":3, "attack_radius":50, "notice_radius":360},
                "slime":
                    {"health":400, "damage":100, "speed":7, "resistance":3, "attack_radius":200, "notice_radius":760}
}






