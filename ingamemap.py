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


from consts import *

import pygame

INGAMEMAP_CHARACTER_MARKER_DIR = os.path.join(ART_DIR, "robot marker.png")
INGAMEMAP_MISSION_MARKER_DIR = os.path.join(ART_DIR, "mission marker.png")

class InGameMap:
    def __init__(self):
        self.image = pygame.Surface((TILE_WIDTH * MAP_WIDTH, TILE_HEIGHT * MAP_HEIGHT))

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

        # read in map
        f = open(MAP_DEFAULT_DIR, 'rb')
        data = f.read()
        f.close()
        self.ship = []
        for x in xrange(MAP_HEIGHT):
            self.ship += [[ord(y) for y in data[:MAP_WIDTH]]]
            data = data[MAP_WIDTH:]

    # call before displaying, or else the screen will be blank
    def update(self, character_x = None, character_y = None, mission_x = None, mission_y = None):
        if (character_x == None) and (character_y == None) and (mission_x == None) and (mission_y == None):
            return NO_PROBLEM
        self.image.blit(self.background, (0, 0))
        # blit all tiles to surface
        # really shouldnt have to do this
        # should be able to position markers after scaling
        show = pygame.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)
        clip = pygame.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)
        for x in xrange(MAP_HEIGHT):
            for y in xrange(MAP_WIDTH):
                clip.x = TILE_WIDTH * self.ship[x][y]
                self.image.blit(self.tiles, show, clip)
                show.y += TILE_WIDTH
            show.y = 0
            show.x += TILE_HEIGHT
        self.image.blit(self.character_marker, (character_x * TILE_WIDTH, character_y * TILE_HEIGHT))
        self.image.blit(self.mission_marker, (mission_x * TILE_WIDTH, mission_y * TILE_HEIGHT))
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        return NO_PROBLEM

    def display(self, screen):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        screen.blit(self.image, (0, 0))
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

    quit = False
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True
        test.display(screen)
        pygame.display.flip()

    pygame.quit()
