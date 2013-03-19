# map.py
# Generic map class for basic storing of data,
# updating, and displaying of a tile map

# probably need to change self.__data to array
# of tiles rather than array of integers

import sys

import pygame

from consts import *
from functions import *
from hashlib import *

class map:
    def __init__(self, tile_file_name):
        self.__sheet = pygame.image.load(tile_sheet_name)
        self.__sheet.set_colorkey(colorkey)
        if self.__sheet == None:                       # error if file could not be opened
            sys.exit(IMAGE_DOES_NOT_EXIST)

        self.__map = []

    def save(self, save_name):
        file = open(save_name, 'wb')
        for x in self.__map:
            for y in x:
                file.write(y);
        file.close()
        return NO_PROBLEM

    def load(self, open_name):
        try:
            file = open(open_name, 'rb')
            data = file.read()
            file.close()

            checksum = sha512(data[:-64]).digest()

            for x in xrange(MAP_HEIGHT):
                self.__map += [[y for y in data[:MAP_WIDTH]]]
                data = data[MAP_WIDTH:]

            if checksum != data:
                sys.exit(CHECKSUMS_DO_NOT_MATCH)

        except IOError, err:
            print err

        return NO_PROBLEM

    def display(self, screen, camera):
        # maybe, instead of actually displaying, return clip # and Rect to display in main
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        if self.__map == []:
            return NO_DATA

        for x in xrange(SHOW_TILES_W):
            for y in xrange(SHOW_TILES_H):
                show = pygame.rect(x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                clip = pygame.rect(self.__data[camera.x + x][camera.y + y] * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT)
                screen.blit(self.__sheet, show, clip)
        return 0
