# NPC class
# does not quite work yet

import pygame

from consts import *

class NPC:
    def __init__(self, npc_type):
        self.type = npc_type
        self.name = ""
        self.__x = 0
        self.__y = 0
        self.__clip = 0                                # which image to clip from sprite sheet; also which direction player is facing

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_x(self, new_x):
        self.__x = new_x

    def set_y(self, new_y):
        self.__y = new_y

    def x(self):
        return self.__x

    def y(self):
        return self.__y

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
        clip = pygame.Rect(self.__clip, 0, NPC_WIDTH, NPC_HEIGHT)
        show = pygame.Rect((self.__x - camera.x) * TILE_WIDTH, (self.__y - camera.y) * TILE_HEIGHT, 0, 0)
        screen.blit(self.__sheet, show, clip)
        return 0
