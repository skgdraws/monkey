from os import walk
from csv import *
from settings import tile_size
import pygame

def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    
    return surface_list

def import_csv_layout(path):
    terrain_map = []
    # Opening up the csv File
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_scores(path):
    score_list = []
    # Opening up the csv File
    with open(path) as map:

        scores = reader(map, delimiter = ',')
        for row in scores:
            score_list.append(list(row))
            
        return score_list

def import_cut_graphics(path):

    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size

            new_surf = pygame.Surface((tile_size, tile_size))
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles

def save_data(score, name):

    file = open('assets/data/scores.csv', "a", newline="")

    data = (score, name)
    data_writer = writer(file)
    data_writer.writerow(data)
    file.close()