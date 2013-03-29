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
    def __init__(self, sprite_sheet):   # taking in string to save memory + faster since surfaces are passed by value, not reference
        # remember sprite will be standing on tile x+1
        self.x = 0.0                                 # tile position on map
        self.y = 0.0                                 # tile position on map
        self.clip = 0                                # which image to clip from sprite sheet; also which direction player is facing
        self.frame = 0                               # use for animations

        self.sprite = pygame.image.load(sprite_sheet)
        if self.sprite == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)

    # modifiers (for forcing movement)
    def setx(self, x):
        self.x = x

    def sety(self, y):
        self.y = y

    # accessors
    def getx(self):
        return self.x

    def gety(self):
        return self.y

    # other functions
    def save(self):
        pass

    # default location
    def spawn():
        self.x = 0
        self.y = 0

    def interact(self):
        pass

    def update(self, keystates, keybindings): # add argument for collision detection?
        moved = False
        if keystates[keybindings[KB_UP]]:
            self.y -= 1
            if (self.y < 0):
                self.y = 0
            moved = True
        elif keystates[keybindings[KB_LEFT]]:
            self.x -= 1
            if (self.x < 0):
                self.x = 0
            moved = True
        elif keystates[keybindings[KB_DOWN]]:
            self.y += 1
            if (self.y >= MAP_HEIGHT):
                self.y = MAP_HEIGHT - 1
            moved = True
        elif keystates[keybindings[KB_RIGHT]]:
            self.x += 1
            if (self.x >= MAP_WIDTH):
                self.x = MAP_WIDTH - 1
            moved = True

    def display(self, screen, camera):
        # maybe, instead of actually displaying, return clip # and Rect to display in main
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        clip = pygame.Rect(self.clip, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        show = pygame.Rect((self.x - camera.x) * TILE_WIDTH, (self.y - camera.y) * TILE_HEIGHT, 0, 0)
        screen.blit(self.sprite, show, clip)
        return 0
