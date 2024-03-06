import pygame
import os

tile_size = 150

screen_width = 1200
screen_height = 6 * tile_size  # 21 is len(maze_lst)

#screen_width = 3500
#screen_height = 9 * tile_size  # 21 is len(maze_lst)

FPS = 60
pygame.init()
font = pygame.font.Font("../Fonts/Pixel.ttf", 100)
high_score_font = pygame.font.Font("../Fonts/Pixel.ttf", 50)
tutorial_font = pygame.font.Font("../Fonts/Pixel.ttf", 20)

# colours
white = (255, 255, 255)

def img_centre(image):
    width = screen_width // 2 - image.get_width() // 2
    height = screen_height // 2 - image.get_height() // 2
    return [width, height]


def load_graphics(filepath):
    graphic_surface_list = []

    for image in os.listdir(filepath):  # for every image in a file location
        image_filepath = f"{filepath}/{image}"  # get images fill filepath

        loaded_image = pygame.image.load(image_filepath)  # load image
        graphic_surface_list.append(loaded_image)  # append loaded image to a list

    return graphic_surface_list  # returns the list of all loaded images

def import_graphics_dict(sprite_name, animation_dict, filepath):
    main_path = (f"{filepath}/{sprite_name}/")

    for animation_type in animation_dict.keys():
        animation_dict[animation_type] = load_graphics(main_path + animation_type)

    return animation_dict
