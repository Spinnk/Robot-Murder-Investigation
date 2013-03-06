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
    def __init__(self, sprite_sheet_name, colorkey):   # taking in string to save memory + faster since surfaces are passed by value, not reference
        # remember sprite will be standing on tile x+1
        self.__x = 0.0                                 # tile position on map
        self.__y = 0.0                                 # tile position on map
        self.__clip = 0                                # which image to clip from sprite sheet; also which direction player is facing
        self.__sheet = pygame.image.load(sprite_sheet_name)
        self.__sheet.set_colorkey(colorkey)
        if self.__sheet == None:                       # error if file could not be opened
            sys.exit(IMAGE_DOES_NOT_EXIST)

#        self.__lasttick = 0                            # timer for frame independant animation

    # modifiers
    def setx(self, y):
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

    def update(self, keystates):
#        if self.__lasttick == 0:
#            self.__lasttick = pygame.time.get_ticks()
#            return
#        now = pygame.time.get_ticks()
#        dt = now - self.__lasttick
#        self.__lasttick = now
        moved = False
        if keystates[UP_KB]:
            self.__y -= 1#(CHARACTER_VY * dt) / 1000.
            if (self.__y < 0):
                self.__y = 0
            moved = True
        if keystates[LEFT_KB]:
            self.__x -= 1#(CHARACTER_VX * dt) / 1000.
            if (self.__x < 0):
                self.__x = 0
            moved = True
        if keystates[DOWN_KB]:
            self.__y += 1#(CHARACTER_VY * dt) / 1000.
#            if (self.__y > ):
#                self.__y =
            moved = True
        if keystates[RIGHT_KB]:
            self.__x += 1#(CHARACTER_VX * dt) / 1000.
#            if (self.__x > ):
#                self.__y =
            moved = True
        if moved:
            pygame.time.delay(100)

    def display(self, screen, camera):
        # maybe, instead of actually displaying, return clip # and Rect to display in main
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        clip = pygame.Rect(self.__clip, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        show = pygame.Rect((self.__x - camera.x) * TILE_WIDTH, (self.__y - camera.y) * TILE_HEIGHT, 0, 0)
        screen.blit(self.__sheet, show, clip)
        return 0
