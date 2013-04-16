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
import copy
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
        self.clip = 0           # which image to clip from sprite sheet; also which direction player is facing

        self.count = 0          # Count the number of times update was called
                                # to limit updates per second
        self.mode = 0           # 0 = not interacting, 1 =
        self.say = 0            # dialogue index;
        self.sayindex = -1
        self.font = pygame.font.Font(NPC_FONT_DIR, NPC_FONT_SIZE)

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
    def spawn(self, x, y):
        self.x = x
        self.y = y

    # start dialogue
    def setdialogue(self, inventory, d):
        self.say = d
        self.sayindex = 0

    # load from save string
    def load(self, data):
        self.type = ord(data[0])
        self.settype(self.type)
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
        pass
        # if talking
#        if self.say:


    # display NPC
    def display(self, screen, camera):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        show = pygame.Rect((self.x - camera.x) * TILE_WIDTH, (self.y - camera.y) * TILE_HEIGHT, 0, 0)
        clip = pygame.Rect(self.clip, 0, NPC_WIDTH, NPC_HEIGHT)
        screen.blit(self.sprite, show, clip)

        if self.say:
            show = copy.deepcopy(NPC_TEXT_BOX)
            show.y += 10
            dy = self.font.size("")[1]
            screen.fill(WHITE, show)
            for line in DIALOGUE[self.say]:
                text = self.font.render(line, NPC_FONT_ANTIALIAS, NPC_FONT_COLOR)
                screen.blit(text, show)
                show.y += dy
        return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # create the screen
    if screen == None:
        sys.exit(SCREEN_DOES_NOT_EXIST)

    pygame.display.set_caption("Character Demo")
    keybindings = default_keybindings()
    camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    test = [NPC() for x in xrange(1)]
    test[0].settype(0); #test[1].settype(1)
    #test[2].settype(2); test[3].settype(3)

    for x in xrange(len(test)):
        test[x].setdialogue(1)

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
#            npc.update(None)
            npc.display(screen, camera)

        pygame.display.flip()
        pygame.time.Clock().tick(10)
    pygame.quit()
