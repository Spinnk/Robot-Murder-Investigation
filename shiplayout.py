#! /usr/bin/python
# shiplayout.py
# Generic map class for basic storing of data,
# updating, and displaying of a tile map

# Run this file to generate a random default map

# shiplayout.py is part of Sentience in Space.
#
# Sentience in Space is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sentience in Space is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sentience in Space.  If not, see <http://www.gnu.org/licenses/>.

import sys

import pygame

from consts import *

class ShipLayout:
    def __init__(self):
        self.data = []  # 2D array
        self.items = [] # [[x, y], item]

        self.floor_tiles = pygame.image.load(TILE_SHEET_DIR)
        if self.floor_tiles == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.floor_tiles.set_colorkey(COLOR_KEY)
        self.floor_tiles = self.floor_tiles.convert()

        self.item_tiles = pygame.image.load(ITEM_SHEET_SMALL_DIR)
        if self.item_tiles == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.item_tiles.set_colorkey(COLOR_KEY)
        self.item_tiles = self.item_tiles.convert()

    # change a tile type
    def changetile(self, newtile, location):
        self.data[location[0]][location[1]] = newtile

    # set items
    def setitems(self, items):
        self.items = items

    # get copy of all items
    def getitems(self):
        return self.items

    # add one item to the map
    def additem(self, location, item):
        self.items += [[location, item]]

    # remove item from map
    # might be changed: if a tile has multiple items stacked on top of it, include item type
    def removeitem(self, location, item = None):
        for i in xrange(len(self.items)):
            if self.items[i][0] == location:
                if item:
                    if self.items[i][1] == item:
                        out = self.items[i][1]
                        del self.items[i]
                        return out
                elif not item:
                    out = self.items[i][1]
                    del self.items[i]
                    return out
        return None

    # generates a random map with items
    def generaterandommap(self):
        self.data = []
        from random import randint
        for x in xrange(MAP_HEIGHT):
            self.data += [[randint(0, MAX_TILE_VALUE) for x in xrange(MAP_WIDTH)]]
        for x in xrange(3):
            self.items += [[[x, x], randint(0, len(ITEMS) - 1)]]

    # load a map file to memory
    def loadmap(self, file_name):
        f = open(file_name, 'rb')
        data = f.read()
        f.close()
        self.data = []
        for x in xrange(MAP_HEIGHT):
            self.data += [[ord(y) for y in data[:MAP_WIDTH]]]
            data = data[MAP_WIDTH:]
        if len(self.data) != MAP_HEIGHT:
            self.data = []
            return INCORRECT_DATA_LENGTH
        return NO_PROBLEM

    # save only the map
    def savemap(self, file_name):
        f = open(file_name, 'wb')
        # write every tile as an ASCII characters to a file
        for row in self.data:
            for tile in row:
                 f.write(chr(tile))
        f.close()
        return NO_PROBLEM

    # load items onto map
    def load(self, data):
        self.items = []
        while len(data):
            self.items += [[[ord(data[0]), ord(data[1])], ord(data[2])]]
            data = data[3:]
        return NO_PROBLEM

    # save items into a string of the specified format
    def save(self):
        '''
        Format:
            item_x | item_y | item_type | item_x | item_y | item_type | ...
            item_x       - 1 byte
            item_y       - 1 byte
            item_type    - 1 byte
        '''
        return ''.join([chr(item[0][0]) + chr(item[0][1]) + chr(item[1]) for item in self.items])

    # display map on screen
    def display(self, screen, camera):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        # display tiles
        for x in xrange(TILE_SHOW_W):
            for y in xrange(TILE_SHOW_H):
                show = pygame.Rect(x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                clip = pygame.Rect(self.data[camera.x + x][camera.y + y] * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT)
                screen.blit(self.floor_tiles, show, clip)
        # display items
        for item in self.items:
            # if item is in camera
            if (((camera.x <= item[0][0]) and (item[0][0] < (camera.x + TILE_SHOW_W))) and ((camera.y <= item[0][1]) and (item[0][1] < (camera.y + TILE_SHOW_H)))):
                try:
                    show = pygame.Rect((item[0][0] - camera.x) * TILE_WIDTH, (item[0][1] - camera.y) * TILE_HEIGHT, ITEM_SMALL_WIDTH, ITEM_SMALL_HEIGHT)
                    clip = pygame.Rect(ITEM_SMALL_WIDTH * item[1], 0 , ITEM_SMALL_WIDTH, ITEM_SMALL_HEIGHT)
                    screen.blit(self.item_tiles, show, clip)
                except TypeError:
                    print "Error displaying item: " + str(item)
        return 0

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    test = ShipLayout()
    test.generaterandommap()
    test.savemap(os.path.join(CWD, "map.txt"))
    pygame.quit()
