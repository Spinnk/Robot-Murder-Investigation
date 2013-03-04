# map.py
# Generic map class for basic storing of data,
# updating, and displaying of a tile map

# probably need to change self.__data to array
# of tiles rather than array of integers

import pygame

from consts import *
from functions import *

class map:
    def __init__(self, map_file_name, tile_sheet_name):
        self.__sheet = pygame.image.load(tile_sheet_name)
#        self.__sheet.set_colorkey(colorkey)
        if self.__sheet == None:                       # error if file could not be opened
            sys.exit(IMAGE_DOES_NOT_EXIST)

        # read the map file
        file = open(map_file_name, 'r')
        data = file.readlines()
        file.close()

        # parse map by reading the entire file, replacing display characters, and splitting up the entire string
        # change depending on how the file is actually formatted
        self.__data = [line.replace("\n", " ").replace("\r", " ").split(" ") for line in data]

    def save(self, file_name):
        file = open(file_name, 'w')
        # copy self.__data to file
        file.close()
        return 0

    def display(self, screen, camera):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        for x in xrange(SHOW_TILES_W):
            for y in xrange(SHOW_TILES_H):
                show = pygame.rect(x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                clip = pygame.rect(self.__data[camera.x + x][camera.y + y] * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT)
                screen.blit(self.__sheet, show, clip)
        return 0
