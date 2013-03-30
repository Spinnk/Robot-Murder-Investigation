# NPC class
# Generic NPC class for basic storing of data,
# updating, and displaying

import binascii

import pygame

from consts import *

class NPC:
    def __init__(self):
        self.type = 255
        self.name = ""
        self.x = 0
        self.y = 0
        self.clip = 0                                # which image to clip from sprite sheet; also which direction player is facing
        self.frame = 0                               # which frame to show

    def settype(self, new_type):
        self.type = new_type

        self.sprite = pygame.image.load(NPC_SHEETS_DIR[new_type])
        if self.sprite == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)

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

    # load from save
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

    # grid is array Formatf squares around npc to check if can be moved there or not
    def update(self, grid):
        pass

    def display(self, screen, camera):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        clip = pygame.Rect(self.clip, 0, NPC_WIDTH, NPC_HEIGHT)
        show = pygame.Rect((self.x - camera.x) * TILE_WIDTH, (self.y - camera.y) * TILE_HEIGHT, 0, 0)
        screen.blit(self.sprite, show, clip)
        return NO_PROBLEM

if __name__=='__main__':
    pass