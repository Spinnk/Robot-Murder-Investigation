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
    def __init__(self):   # taking in string to save memory + faster since surfaces are passed by value, not reference
        # remember sprite will be standing on tile y+1
        self.spawn()

        self.sprite = pygame.image.load(CHARACTER_SPRITE_SHEET_DIR)
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

    # set an initial character location
    def spawn(self):
        self.x = 0                                   # tile position on map
        self.y = 0                                   # tile position on map
        self.clip = 0                                # which image to clip from sprite sheet; also which direction player is facing
        self.moved = False

#    def interact(self):
#        pass

    # load from save string
    def load(self, data):
        if len(data) != 3:
            return INCORRECT_DATA_LENGTH
        self.x = ord(data[0])
        self.y = ord(data[1])
        self.clip = ord(data[2])
        self.moved = False
        return NO_PROBLEM

    # save character to a string of specified format
    def save(self):
        '''
        Format:
            x | y | clip
            x     - 1 byte
            y     - 1 byte
            clip  - 1 byte
        '''
        return chr(self.x) + chr(self.y) + chr(self.clip)

    # check for movement
    def update(self, keybindings): # add argument for collision detection?
        keystates = pygame.key.get_pressed()
        if keystates[keybindings[KB_DOWN]]:
            self.clip = 0
            self.moved = True
            if ((self.y + 3) >= MAP_HEIGHT):
                self.y = MAP_HEIGHT - 3
                self.moved = False
        elif keystates[keybindings[KB_RIGHT]]:
            self.clip = 1
            self.moved = True
            if ((self.x + 1) >= MAP_WIDTH):
                self.x = MAP_WIDTH - 1
                self.moved = False
        elif keystates[keybindings[KB_UP]]:
            self.clip = 2
            self.moved = True
            if ((self.y - 1) < 0):
                self.y = 0
                self.moved = False
        elif keystates[keybindings[KB_LEFT]]:
            self.clip = 3
            self.moved = True
            if ((self.x - 1) < 0):
                self.x = 0
                self.moved = False

    # display character
    def display(self, screen, camera):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST

        # if moved
        if self.moved:
            self.moved = False
            original = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            original.blit(screen, (0, 0))
            dx = TILE_WIDTH / CHARACTER_FRAMES
            dy = TILE_HEIGHT / CHARACTER_FRAMES
            show = pygame.Rect((self.x - camera.x) * TILE_WIDTH, (self.y - camera.y) * TILE_HEIGHT, 0, 0)
            clip = pygame.Rect(0, self.clip * CHARACTER_HEIGHT, CHARACTER_WIDTH, CHARACTER_HEIGHT)
            for frame in xrange(CHARACTER_FRAMES):
                if self.clip == 0: # down
                    show.y += dy
                if self.clip == 1: # right
                    show.x += dx
                if self.clip == 2: # up
                    show.y -= dy
                if self.clip == 3: # left
                    show.x -= dx
                clip.x += CHARACTER_WIDTH
                screen.blit(original, (0, 0))
                screen.blit(self.sprite, show, clip)
                pygame.time.delay(CHARACTER_WALK_TIME / CHARACTER_FRAMES)
                pygame.display.flip()

            if self.clip == 0: # down
                self.y += 1
            if self.clip == 1: # right
                self.x += 1
            if self.clip == 2: # up
                self.y -= 1
            if self.clip == 3: # left
                self.x -= 1

        # display at destination
        show = pygame.Rect((self.x - camera.x) * TILE_WIDTH, (self.y - camera.y) * TILE_HEIGHT, 0, 0)
        clip = pygame.Rect(0, self.clip * CHARACTER_HEIGHT, CHARACTER_WIDTH, CHARACTER_HEIGHT)
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

    test = Character()
    test.spawn()

    quit = False
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True
            test.update(keybindings)
        screen.fill(WHITE)
        test.display(screen, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.flip()

        pygame.time.Clock().tick(FPS)

    pygame.quit()
