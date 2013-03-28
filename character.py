# character.py
# Generic Character class for basic storing of data,
# updating, and displaying

# need to figure out how to keep character
# centered except when near edges of map

import sys

import pygame

from consts import *
from keybinding import *

class character:
    # or instead of using file name, open all images in main, and clip with display()
    def __init__(self):   # taking in string to save memory + faster since surfaces are passed by value, not reference
        # remember sprite will be standing on tile x+1
        self.__x = 0.0                                 # tile position on map
        self.__y = 0.0                                 # tile position on map
        self.__clip = 0                                # which image to clip from sprite sheet; also which direction player is facing
        self.__frame = 0                               # use for animations

    # modifiers (for forcing movement)
    def setx(self, x):
        self.__x = x

    def sety(self, y):
        self.__y = y

    # accessors
    def x(self):
        return self.__x

    def y(self):
        return self.__y

    # other functions
    def save(self):
        pass

    def interact(self):
        pass

    def update(self, keystates): # add argument for collision detection?
        moved = False
        if keystates[KB_UP]:
            self.__y -= 1
            if (self.__y < 0):
                self.__y = 0
            moved = True
        elif keystates[KB_LEFT]:
            self.__x -= 1
            if (self.__x < 0):
                self.__x = 0
            moved = True
        elif keystates[KB_DOWN]:
            self.__y += 1
            if (self.__y >= MAP_HEIGHT):
                self.__y = MAP_HEIGHT - 1
            moved = True
        elif keystates[KB_RIGHT]:
            self.__x += 1
            if (self.__x >= MAP_WIDTH):
                self.__y = MAP_WIDTH - 1
            moved = True

        # something to prevent constant moving
        #if moved:
            #pygame.time.delay(100)

    def display(self, screen, sheet, camera):
        # maybe, instead of actually displaying, return clip # and Rect to display in main
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        if sheet == None:
            return SURFACE_DOES_NOT_EXIST
        clip = pygame.Rect(self.__clip, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        show = pygame.Rect((self.__x - camera.x) * TILE_WIDTH, (self.__y - camera.y) * TILE_HEIGHT, 0, 0)
        screen.blit(sheet, show, clip)
        return 0
