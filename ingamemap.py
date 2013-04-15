#! /usr/bin/python

# InGameMap Class

# ingamemap.py is part of Sentience in Space.
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

import copy

from consts import *

import pygame

class InGameMap:
    def __init__(self):
        self.update()

        # open files that will not change
        self.background = pygame.image.load(BACKGROUND_IMAGE_DIR)
        if self.background == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)

        self.tiles = pygame.image.load(TILE_SHEET_DIR)
        if self.tiles == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.tiles.set_colorkey(COLOR_KEY)
        self.tiles = self.tiles.convert()

        self.character_marker = pygame.image.load(INGAMEMAP_CHARACTER_MARKER_DIR)
        if self.character_marker == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.character_marker.set_colorkey(COLOR_KEY)
        self.character_marker = self.character_marker.convert()

        self.mission_marker = pygame.image.load(INGAMEMAP_MISSION_MARKER_DIR)
        if self.mission_marker == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.mission_marker.set_colorkey(COLOR_KEY)
        self.mission_marker = self.mission_marker.convert()

        # read in map from file
        f = open(MAP_DEFAULT_DIR, 'rb')
        data = f.read()
        f.close()
        self.ship = []
        for x in xrange(MAP_HEIGHT):
            self.ship += [[ord(y) for y in data[:MAP_WIDTH]]]
            data = data[MAP_WIDTH:]

    # call before displaying, or screen will not contain markers
    def update(self, character_x = None, character_y = None, mission_x = None, mission_y = None):
        self.character_x = character_x
        self.character_y = character_y
        self.mission_x = mission_x
        self.mission_y = mission_y
        return NO_PROBLEM

    def display(self, screen):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        image = pygame.Surface((TILE_WIDTH * MAP_WIDTH, TILE_HEIGHT * MAP_HEIGHT))
        if image == None:
            return SURFACE_DOES_NOT_EXIST

        # draw entire map
        image.blit(self.background, (0, 0))
        show = pygame.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)
        clip = pygame.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)
        for x in xrange(MAP_HEIGHT):
            for y in xrange(MAP_WIDTH):
                clip.x = TILE_WIDTH * self.ship[x][y]
                image.blit(self.tiles, show, clip)
                show.y += TILE_WIDTH
            show.y = 0
            show.x += TILE_HEIGHT

        if (self.character_x is not None) and (self.character_y is not None) and (self.mission_x is not None) and (self.mission_y is not None):
            image.blit(self.character_marker, (self.character_x * TILE_WIDTH, self.character_y * TILE_HEIGHT))
            image.blit(self.mission_marker, (self.mission_x * TILE_WIDTH, self.mission_y * TILE_HEIGHT))
        image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(image, (0, 0))
        return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # create the screen
    if screen == 0:
        sys.exit(SCREEN_DOES_NOT_EXIST)

    pygame.display.set_caption("InGameMap Demo")
    pygame.key.set_repeat(100, 100)

    test = InGameMap()
    test.update(0, 1, 10, 6)
    test.display(screen)
    pygame.display.flip()

    quit = False
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True

    pygame.quit()
