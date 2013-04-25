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
        self.image = pygame.Surface((0, 0))
        self.camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setmarkers()
        self.setscale()

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
    def setmarkers(self, character_x = None, character_y = None, mission_x = None, mission_y = None):
        self.character_x = character_x
        self.character_y = character_y
        self.mission_x = mission_x
        self.mission_y = mission_y
        # center the camera
        if self.character_x and self.character_y:
            self.camera.x = self.character_x - TILE_SHOW_W / 2
            if self.camera.x < 0:
                self.camera.x = 0
            if (self.camera.x + TILE_SHOW_W) > MAP_WIDTH:
                self.camera.x = MAP_WIDTH - TILE_SHOW_W
            self.camera.y = self.character_y - TILE_SHOW_H / 2 + 1
            if self.camera.y < 0:
                self.camera.y = 0
            if (self.camera.y + TILE_SHOW_H + 1) > MAP_HEIGHT:
                self.camera.y = MAP_HEIGHT - TILE_SHOW_H - 1
        return NO_PROBLEM

    # default scale is 1. might want to change before calling draw
    # zoom   1,1 = show full map
    #      10, 5 = normal size
    #     18, 18 = max zoom
    def setscale(self, x_scale = 1, y_scale = 1):
        self.xscale = x_scale
        self.yscale = y_scale
        return NO_PROBLEM

    # draw map; call as few times as possible
    def draw(self):
        self.image = pygame.Surface((TILE_WIDTH * MAP_WIDTH, TILE_HEIGHT * MAP_HEIGHT))
        if self.image == None:
            return SURFACE_DOES_NOT_EXIST

        # draw entire map
        show = pygame.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)
        clip = pygame.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)
        for y in xrange(MAP_HEIGHT):
            for x in xrange(MAP_WIDTH):
                clip.x = TILE_WIDTH * self.ship[y][x]
                self.image.blit(self.tiles, show, clip)
                show.x += TILE_WIDTH
            show.x = 0
            show.y += TILE_HEIGHT

        # draw markers
        if (self.character_x is not None) and (self.character_y is not None):
            self.image.blit(self.character_marker, (self.character_x * TILE_WIDTH, self.character_y * TILE_HEIGHT))
        if (self.mission_x is not None) and (self.mission_y is not None):
            self.image.blit(self.mission_marker, (self.mission_x * TILE_WIDTH, self.mission_y * TILE_HEIGHT))

        # shrink image
        self.image = pygame.transform.scale(self.image, (self.xscale * SCREEN_WIDTH, self.yscale * SCREEN_HEIGHT))

        return NO_PROBLEM

    def update(self, event = None):
        keystates = pygame.key.get_pressed()
#        if event.key == KEYBINDINGS[KB_DOWN]:
        if keystates[KEYBINDINGS[KB_DOWN]]:
            self.camera.y += TILE_HEIGHT / self.yscale
#        elif event.key == KEYBINDINGS[KB_RIGHT]:
        elif keystates[KEYBINDINGS[KB_RIGHT]]:
            self.camera.x += TILE_WIDTH / self.xscale
#        elif event.key == KEYBINDINGS[KB_UP]:
        elif keystates[KEYBINDINGS[KB_UP]]:
            self.camera.y -= TILE_HEIGHT / self.yscale
#        elif event.key == KEYBINDINGS[KB_LEFT]:
        elif keystates[KEYBINDINGS[KB_LEFT]]:
            self.camera.x -= TILE_WIDTH / self.xscale
        if self.camera.x < 0:
            self.camera.x = 0
        if (self.camera.x + SCREEN_WIDTH) >= self.image.get_size()[0]:
            self.camera.x = self.image.get_size()[0] - SCREEN_WIDTH - 1
        if self.camera.y < 0:
            self.camera.y = 0
        if (self.camera.y + SCREEN_HEIGHT) >= self.image.get_size()[1]:
            self.camera.y = self.image.get_size()[1] - SCREEN_HEIGHT - 1
        return NO_PROBLEM

    def display(self, screen):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        screen.blit(self.background, (0, 0))
        screen.blit(self.image, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), self.camera)
        return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # create the screen
    if screen == 0:
        sys.exit(SCREEN_DOES_NOT_EXIST)

    pygame.display.set_caption("InGameMap Demo")
    pygame.key.set_repeat(100, 100)

    test = InGameMap()
    test.setmarkers(0, 1, 10, 6)
    test.setscale(10, 5)
    test.draw()

    quit = False
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True
            #if event.type == pygame.KEYDOWN:
        test.update()
        test.display(screen)
        pygame.display.flip()

    pygame.quit()
