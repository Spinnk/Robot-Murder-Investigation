#! /usr/bin/python

# NPC class
# Generic NPC class for basic storing of data,
# updating, and displaying

# Run this file to display random NPCs on screen
# Can move camera with up, down, left, and right keys

# npc.py is part of Sentience in Space.
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

import binascii
import random

import pygame

from consts import *
from keybinding import *

class NPC:
    def __init__(self):
        self.type = 0
        self.name = ""
        self.x = 0
        self.y = 0
        self.clip = 0                                # which image to clip from sprite sheet; also which direction player is facing
        self.frame = 0                               # which frame to show
        self.moved = False

        self.count = 0          # Count the number of times update was called
                                # to limit updates per second

    # Accessors and Modifiers

    # should run this function before using NPC
    def settype(self, new_type):
        self.type = new_type

        self.sprite = pygame.image.load(NPC_SHEETS_DIR[new_type])
        if self.sprite == None:
            return IMAGE_DOES_NOT_EXIST
        return NO_PROBLEM

    def gettype(self):
        return self.type

    def setname(self, name):
        self.name = name

    def getname(self):
        return self.name

    def setx(self, new_x):
        self.x = new_x

    def getx(self):
        return self.x

    def sety(self, new_y):
        self.y = new_y

    def gety(self):
        return self.y

    # set an initial NPC location
    def spawn(self, location = None):
        if not location:
            self.x = random.randint(0, MAP_WIDTH - 1)
            self.y = random.randint(0, MAP_HEIGHT - 1)
        else:
            self.x = location[0]
            self.y = location[1]

    # load from save string
    def load(self, data):
        self.type = ord(data[0])
        name_len = int(binascii.hexlify(data[1:3]), 16)
        data = data[3:]
        self.name = data[:name_len]
        data = data[name_len:]
        self.x = ord(data[0])
        self.y = ord(data[1])
        self.clip = ord(data[2])
        self.clip = ord(data[3])
        return NO_PROBLEM

    # save NPC to a string of specified format
    def save(self):
        '''
        Format:
            type | name_len | name | x | y | clip | frame
            type      - 1 byte
            name_len  - 2 bytes
            name      - name_len bytes
            x         - 1 byte
            y         - 1 byte
            clip      - 1 byte
            frame     - 1 byte
        '''
        return chr(self.type) + binascii.unhexlify(makehex(len(self.name), 4)) + self.name + chr(self.x) + chr(self.y) + chr(self.clip) + chr(self.frame)

    # move NPC and use grid to check for collisions
    # it will need to be changed if some NPCs can only
    # be in certain areas
    def update(self, grid):
        # Limit updates to once every 15 calls
        self.count += 1
        if self.count == 15:
            self.count = 0
        if self.count != 0:
            return
        
        direction = random.randint(0, 3)
        if direction == 0:
            self.x += 1
        if direction == 1:
            self.x -= 1
        if direction == 2:
            self.y += 1
        if direction == 3:
            self.y -= 1
        if self.x < 0:
            self.x = 0
        if self.x >= MAP_WIDTH:
            self.x = MAP_WIDTH - 1
        if self.y < 0:
            self.y = 0
        if self.y >= MAP_HEIGHT:
            self.y = MAP_HEIGHT - 1

    # display NPC
    def display(self, screen, camera):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        show = pygame.Rect((self.x - camera.x) * TILE_WIDTH, (self.y - camera.y) * TILE_HEIGHT, 0, 0)
#        if self.moved:
#            self.moved = False
#            self.frame += 1
#            self.frame %= 5
#        clip = pygame.Rect(self.frame * CHARACTER_WIDTH, self.clip * CHARACTER_HEIGHT, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        clip = pygame.Rect(self.clip, 0, NPC_WIDTH, NPC_HEIGHT)
        screen.blit(self.sprite, show, clip)
        return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # create the screen
    if screen == None:
        sys.exit(SCREEN_DOES_NOT_EXIST)

    pygame.display.set_caption("Character Demo")
    keybindings = default_keybindings()
    camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    test = [NPC() for x in xrange(4)]
    test[0].settype(0); test[1].settype(1)
    test[2].settype(2); test[3].settype(3)

    quit = False
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True

        keystates = pygame.key.get_pressed()
        if keystates[keybindings[KB_UP]]:
            camera.y -= 1
        elif keystates[keybindings[KB_LEFT]]:
            camera.x -= 1
        elif keystates[keybindings[KB_DOWN]]:
            camera.y += 1
        elif keystates[keybindings[KB_RIGHT]]:
            camera.x += 1
        if camera.x < 0:
            camera.x = 0
        if (camera.x + TILE_SHOW_W) > MAP_WIDTH:
            camera.x = MAP_WIDTH - TILE_SHOW_W
        if camera.y < 0:
            camera.y = 0
        if (camera.y + TILE_SHOW_H + 1) > MAP_HEIGHT:
            camera.y = MAP_HEIGHT - TILE_SHOW_H - 1

        screen.fill(WHITE)
        for npc in test:
            npc.update(None)
            npc.display(screen, camera)

        pygame.display.flip()
        pygame.time.Clock().tick(10)
    pygame.quit()
