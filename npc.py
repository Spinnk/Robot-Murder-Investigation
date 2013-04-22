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

class NPC:
    def __init__(self, npc_id, pos_x, pos_y):
        self.id =  npc_id
        self.name = ""
        self.clip = 0           # which image to clip from sprite sheet; also which direction player is facing

        self.count = 0          # Count the number of times update was called
                                # to limit updates per second
        self.mode = 0           # 0 = not interacting, 1 =
        self.say = 0            # dialogue index;
        self.sayindex = -1
        self.font = pygame.font.Font(NPC_FONT_DIR, NPC_FONT_SIZE)

        self.dialogue = []      # dialogue is a list, where each element is an array of
                                # [mission, preconditions (including response flags),
                                # postconditions, dialogue, (response flag, response dialogue),
                                # (response flag, response dialogue), ...]
        # set the character position
        self.x = pos_x
        self.y = pos_y

        # determine npc "type" based on its id
        if npc_id == 0:
            self.type = 0
        self.sprite = pygame.image.load(NPC_SHEETS_DIR[0])
        if self.sprite == None:
            print "Error loading file: " + str(NPC_SHEETS_DIR[npc_type])

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

    # read in dialogue
    def readdialogue(self):
        dialogue_file = "dialogue" + self.id + ".txt"
        f = open(dialogue_file, 'r')    #open dialogue#.txt, where # is the ID of this NPC
        line = f.readline()
        while line != '':
            splitline = string.split(line, ',')
            if len(splitline) > 4:
                #there are response dialogues
                i = 5
                for i in xrange(len(splitline)):
                    #group response dialogues together
                    response = (splitline[i], splitline[i+1])
                    del splitline[5:7]
                    splitline.insert(i, response)

            self.dialogue.append(splitline)
            line = f.readline()

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
        return NO_PROBLEM

    # save NPC to a string of specified format
    def save(self):
        '''
        Format:
            type | name_len | name | x | y | clip
            type      - 1 byte
            name_len  - 2 bytes
            name      - name_len bytes
            x         - 1 byte
            y         - 1 byte
            clip      - 1 byte
        '''
        return chr(self.type) + binascii.unhexlify(makehex(len(self.name), 4)) + self.name + chr(self.x) + chr(self.y) + chr(self.clip)

    # move NPC and use grid to check for collisions
    # it will need to be changed if some NPCs can only
    # be in certain areas
    def update(self, grid):
        pass


    # display NPC
    def display(self, screen, camera):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        # if the NPC is out of camera focus

        #if (self.x < camera.x) or (camera.x < self.x) or (self.y < camera.y) or (camera.y < self.y):
        #    return NOTHING_DONE

        show = pygame.Rect((self.x - camera.x) * TILE_WIDTH, (self.y - camera.y) * TILE_HEIGHT, 0, 0)
        clip = pygame.Rect(self.clip, 0, NPC_WIDTH, NPC_HEIGHT)
        screen.blit(self.sprite, show, clip)

        # if the NPC is talking
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
    camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    # create NPCS
    test = [NPC() for x in xrange(1)]
    test[0].settype(0); #test[1].settype(1)
    #test[2].settype(2); test[3].settype(3)

    # set dialogue for all of them
    #for x in xrange(len(test)):
    #    test[x].setdialogue(1)

    quit = False
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == KEYBINDINGS[KB_UP]:
                    camera.y -= 1
                elif event.key == KEYBINDINGS[KB_LEFT]:
                    camera.x -= 1
                elif event.key == KEYBINDINGS[KB_DOWN]:
                    camera.y += 1
                elif event.key == KEYBINDINGS[KB_RIGHT]:
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
