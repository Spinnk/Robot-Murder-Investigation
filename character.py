# character.py
# Generic Character class for basic storing of data,
# updating, and displaying
import sys

import pygame

from consts import *

class character:
    # need more variables for log, health?, etc

    def __init__(self, sprite_sheet_name):         # taking in string to save memory + faster since surfaces are passed by value, not reference
        self.__x = 0.0                             # position on map, change according to pixel/tile
        self.__y = 0.0                             # position on map, change according to pixel/tile
        self.__clip = 0                            # which image to clip from sprite sheet
        self.__sheet = pygame.image.load(sprite_sheet_name)
        if self.__sheet == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)

        self.__lasttick = 0                        # timer for frame independant animation

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

    def save(self):
	    pass

    def interact(self):
	    pass

    def update(self, keystates):
        if self.__lasttick == 0:
            self.__lasttick = pygame.time.get_ticks()
            return
        now = pygame.time.get_ticks()
        dt = now - self.__lasttick
        self.__lasttick = now

        # use WASD or arrow keys to move
        if keystates[pygame.K_w] ^ keystates[pygame.K_UP]:
            self.__y -= (CHARACTER_VY * dt) / 1000.
            if (self.__y < 0):
                self.__y = 0
        if keystates[pygame.K_a] ^ keystates[pygame.K_LEFT]:
            self.__x -= (CHARACTER_VX * dt) / 1000.
            if (self.__x < 0):
                self.__x = 0
        if keystates[pygame.K_s] ^ keystates[pygame.K_DOWN]:
            self.__y += (CHARACTER_VY * dt) / 1000.
#            if (self.__y > ):
#                self.__y =
        if keystates[pygame.K_d] ^ keystates[pygame.K_RIGHT]:
            self.__x += (CHARACTER_VX * dt) / 1000.
#            if (self.__x > ):
#                self.__y =

    def display(self, screen, camera):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        clip = pygame.Rect(0, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT) # modify first 0 to correct value
        show = pygame.Rect(self.__x - camera.x, self.__y - camera.y, 0, 0)
        screen.blit(self.__sheet, show, clip)
        return 0
