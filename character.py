#! /usr/bin/python

# character.py
# Generic Character class for basic storing of data,
# updating, and displaying

# Run this file to display a character on screen

# need frame independent animation and movement

# character.py is part of Sentience in Space.
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
from keybinding import *

class Character:
    # or instead of using file name, open all images in main, and clip with display()
    def __init__(self, sprite_sheet):   # taking in string to save memory + faster since surfaces are passed by value, not reference
        # remember sprite will be standing on tile x+1
        self.x = 0                                   # tile position on map
        self.y = 0                                   # tile position on map
        self.clip = 0                                # which image to clip from sprite sheet; also which direction player is facing
        self.frame = 0                               # use for animations
        self.moved = False

        self.sprite = pygame.image.load(sprite_sheet)
        if self.sprite == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)

    # Accessors and Modifiers
    def setx(self, x):
        self.x = x

    def getx(self):
        return self.x

    def sety(self, y):
        self.y = y

    def gety(self):
        return self.y

    def save(self):
        pass

    # set an initial character location
    def spawn(self):
        self.x = 0
        self.y = 0

#    def interact(self):
#        pass

    # load from save string
    def load(self, data):
        if len(data) != 4:
            return INCORRECT_DATA_LENGTH
        self.x = ord(data[0])
        self.y = ord(data[1])
        self.clip = ord(data[2])
        self.frame = ord(data[3])
        self.moved = False
        return NO_PROBLEM

    # save character to a string of specified format
    def save(self):
        '''
        Format:
            x | y | clip | frame
            x     - 1 byte
            y     - 1 byte
            clip  - 1 byte
            frame - 1 byte
        '''
        return chr(self.x) + chr(self.y) + chr(self.clip) + chr(self.frame)

    # check for movement
    def update(self, keybindings): # add argument for collision detection?
        keystates = pygame.key.get_pressed()
        self.moved = False
        if keystates[keybindings[KB_UP]]:
            self.y -= 1
            if (self.y < 0):
                self.y = 0
            self.moved = True
            self.clip = 2
        elif keystates[keybindings[KB_LEFT]]:
            self.x -= 1
            if (self.x < 0):
                self.x = 0
            self.moved = True
            self.clip = 3
        elif keystates[keybindings[KB_DOWN]]:
            self.y += 1
            if (self.y + 2 >= MAP_HEIGHT):
                self.y = MAP_HEIGHT - 3
            self.moved = True
            self.clip = 0
        elif keystates[keybindings[KB_RIGHT]]:
            self.x += 1
            if (self.x >= MAP_WIDTH):
                self.x = MAP_WIDTH - 1
            self.moved = True
            self.clip = 1

    # display character
    def display(self, screen, camera):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        show = pygame.Rect((self.x - camera.x) * TILE_WIDTH, (self.y - camera.y) * TILE_HEIGHT, 0, 0)
        if self.moved:
            self.moved = False
            self.frame += 1
            self.frame %= 5
        clip = pygame.Rect(self.frame * CHARACTER_WIDTH, self.clip * CHARACTER_HEIGHT, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        screen.blit(self.sprite, show, clip)
        return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # create the screen
    if screen == None:
        sys.exit(SCREEN_DOES_NOT_EXIST)

    pygame.display.set_caption("Character Demo")
    pygame.key.set_repeat(100, 100)
    keybindings = default_keybindings()

    test = Character(CHARACTER_SPRITE_SHEET_DIR)
    test.spawn()

    quit = False
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True
        screen.fill(WHITE)
        test.update(pygame.key.get_pressed(), keybindings)
        test.display(screen, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.flip()

        pygame.time.Clock().tick(FPS)

    pygame.quit()
