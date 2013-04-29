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
        self.image = pygame.Surface((INGAMEMAP_TILE_WIDTH * MAP_WIDTH, INGAMEMAP_TILE_HEIGHT * MAP_HEIGHT))
        self.camera = pygame.Rect(0, 0, INGAMEMAP_TILE_SHOW_W, INGAMEMAP_TILE_SHOW_H)
        self.markers = []       # (x, y, type)

        # open files that will not change
        self.background = pygame.image.load(BACKGROUND_IMAGE_DIR)
        if self.background == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)

        self.tiles = pygame.image.load(INGAMEMAP_TILE_SHEET_DIR)
        if self.tiles == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.tiles.set_colorkey(COLOR_KEY)
        self.tiles = self.tiles.convert()

        self.markerimages = pygame.image.load(INGAMEMAP_MARKERS_DIR)
        if self.markerimages == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.markerimages.set_colorkey(COLOR_KEY)
        self.markerimages = self.markerimages.convert()

        # read in map from file
        f = open(MAP_DEFAULT_DIR, 'rb')
        data = f.read()
        f.close()
        ship = []
        for x in xrange(MAP_HEIGHT):
            ship += [[ord(y) for y in data[:MAP_WIDTH]]]
            data = data[MAP_WIDTH:]

        show = pygame.Rect(0, 0, INGAMEMAP_TILE_WIDTH, INGAMEMAP_TILE_HEIGHT)
        clip = pygame.Rect(0, 0, INGAMEMAP_TILE_WIDTH, INGAMEMAP_TILE_HEIGHT)
        for y in xrange(MAP_HEIGHT):
            for x in xrange(MAP_WIDTH):
                clip.x = INGAMEMAP_TILE_WIDTH * ship[y][x]
                self.image.blit(self.tiles, show, clip)
                show.x += INGAMEMAP_TILE_WIDTH
            show.x = 0
            show.y += INGAMEMAP_TILE_HEIGHT

    def addmarker(self, x = None, y = None, type = None):
        if type is not None:
            self.markers += [(x, y, type)]
            if type == 0:
                self.camera.x = x - INGAMEMAP_TILE_SHOW_W / 2
                self.camera.y = y - INGAMEMAP_TILE_SHOW_H / 2
                self.update(None)
            return NO_PROBLEM
        return NOTHING_DONE

    def removemarker(self, x = None, y = None, type = None):
        if type is not None:
            if (x, y, type) in self.markers:
                self.markers.remove((x, y, type))
                return NO_PROBLEM
        return NOTHING_DONE

    def clearmarkers(self):
        self.markers = []
        return NOTHING_DONE

    def update(self, event):
        if event:
            keystates = pygame.key.get_pressed()
            if event.key == KEYBINDINGS[KB_DOWN]:
                self.camera.y += 1
            elif event.key == KEYBINDINGS[KB_RIGHT]:
                self.camera.x += 1
            elif event.key == KEYBINDINGS[KB_UP]:
                self.camera.y -= 1
            elif event.key == KEYBINDINGS[KB_LEFT]:
                self.camera.x -= 1
        if self.camera.x < 0:
            self.camera.x = 0
        if (self.camera.x + self.camera.w) >= MAP_WIDTH:
            self.camera.x = MAP_WIDTH - self.camera.w
        if self.camera.y < 0:
            self.camera.y = 0
        if (self.camera.y + self.camera.h) >= MAP_HEIGHT:
            self.camera.y = MAP_HEIGHT - self.camera.h
        return NO_PROBLEM

    def display(self, screen):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        screen.blit(self.background, (0, 0))

        # draw map
        screen.blit(self.image, (0, 0), pygame.Rect(self.camera.x * INGAMEMAP_TILE_WIDTH, self.camera.y * INGAMEMAP_TILE_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT))

        # draw markers
        for m in self.markers:
            # if the marker in the camera
            if (((self.camera.x <= m[0]) and (m[0] < (self.camera.x + self.camera.w))) and
               ((self.camera.y <= m[1]) and (m[1] < (self.camera.y + self.camera.h)))):
                show = pygame.Rect(INGAMEMAP_TILE_WIDTH * (m[0] - self.camera.x), INGAMEMAP_TILE_HEIGHT * (m[1] - self.camera.y), INGAMEMAP_TILE_WIDTH, INGAMEMAP_TILE_HEIGHT)
                clip = pygame.Rect(INGAMEMAP_TILE_WIDTH * m[2], 0, INGAMEMAP_TILE_WIDTH, INGAMEMAP_TILE_HEIGHT)
                screen.blit(self.markerimages, show, clip)

        return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # create the screen
    if screen == 0:
        sys.exit(SCREEN_DOES_NOT_EXIST)

    pygame.display.set_caption("InGameMap Demo")
    pygame.key.set_repeat(100, 100)

    test = InGameMap()
    test.addmarker(1, 1, 0)
    test.addmarker(5, 10, 1)

    quit = False
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True
            if event.type == pygame.KEYDOWN:
                test.update(event)
        test.display(screen)
        pygame.display.flip()

    pygame.quit()
