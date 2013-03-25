# shiplayout.py
# Generic map class for basic storing of data,
# updating, and displaying of a tile map

# Run this file to generate a random default map

# need to check within class whether or not map exists
# checksum usage is not really correct

import pygame

from consts import *
from hashlib import sha512

class ShipLayout:
    def __init__(self):
        self.data = []

    def change_tile(self, new_tile, location):
        self.data[location[0]][location[1]] = new_tile

    # generates a random map and saves it to self.data and a file
    def generaterandommap(self, file_name):
        self.data = []
        from random import randint
        for x in xrange(MAP_HEIGHT):
            self.data += [[randint(0, MAX_TILE_VALUE) for x in xrange(MAP_WIDTH)]]
        self.save(file_name)

    # load from file
    def load(self, file_name):
        self.data = []
        file = open(file_name, 'rb')
        data = file.read()
        file.close()

        if sha512(data[:-64]).digest() != data[-64:]:
            return CHECKSUMS_DO_NOT_MATCH

        for x in xrange(MAP_HEIGHT):
            self.data += [[ord(y) for y in data[:MAP_WIDTH]]]
            data = data[MAP_WIDTH:]
        return NO_PROBLEM

    # save to file
    def save(self, file_name):
        out = ''
        for row in self.data:
            for tile in row:
                 out += chr(tile)
        out += sha512(out).digest()
        file = open(file_name, 'wb')
        file.write(out)
        file.close()
        return NO_PROBLEM

    # display map on screen
    def display(self, screen, sheet, camera):
        # maybe, instead of actually displaying, return clip # and Rect to display in main
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        if sheet == None:
            return SURFACE_DOES_NOT_EXIST
        for x in xrange(SHOW_TILES_W):
            for y in xrange(SHOW_TILES_H):
                show = pygame.Rect(x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                clip = pygame.Rect(self.data[camera.x + x][camera.y + y] * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT)
                screen.blit(sheet, show, clip)
        return 0

if __name__ == '__main__':
    test = ShipLayout(TILE_SHEET, COLOR_KEY)
    test.generaterandommap(os.path.join(CWD, "map.txt"))
