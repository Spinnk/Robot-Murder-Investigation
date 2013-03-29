# NPC class
# does not quite work yet

import pygame

from consts import *

class NPC:
    def __init__(self, npc_type, sprite_sheet):
        self.type = npc_type
        self.name = ""
        self.x = 0
        self.y = 0
        self.clip = 0                                # which image to clip from sprite sheet; also which direction player is facing
        self.frame = 0                               # which frame to show

        self.sprite = pygame.image.load(sprite_sheet)
        if self.sprite == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)

    def setname(self, name):
        self.name = name

    def getname(self):
        return self.name

    def setx(self, new_x):
        self.x = new_x

    def sety(self, new_y):
        self.y = new_y

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    # load npcs from save
    def load(self, data):
        pass

    # save npcs to file or something (need other arguments)
    def save(self):
        psss

    # grid is array of squares around npc to check if can be moved there or not
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