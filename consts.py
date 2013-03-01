# consts.py
# List of Game Constants / Global Variables
import os
import pygame

GAME_NAME = ""
SCREEN_WIDTH = 640          # pixels
SCREEN_HEIGHT = 480         # pixels
# SCREEN_BPP = 32

MAP_WIDTH = 1024            # change depending on pixel or tile
MAP_HEIGHT = 1024           # change depending on pixel or tile

TILE_WIDTH = 40             # pixels
TILE_HEIGHT = 40            # pixels

SPRITE_SHEETS = ["", ""]    # strings of file names
SPRITE_WIDTH = 0            # pixels
SPRITE_HEIGHT = 0           # pixels

CHARACTER_SPRITE_SHEET = os.path.join(os.getcwd(), "robot.png")
CHARACTER_WIDTH = 80        # pixels
CHARACTER_HEIGHT = 188      # pixels
#CHARACTER_VX = 250          # change depending on pixel or tile
#CHARACTER_VY = 250          # change depending on pixel or tile

# Random Useful RGB Values
WHITE = pygame.Color(0xff, 0xff, 0xff, 0xff)
BLACK = pygame.Color(0x00, 0x00, 0x00, 0xff)
HOTPINK = pygame.Color(0xff, 0x69, 0xb4, 0xff)

COLOR_KEY = HOTPINK

# Error Codes
NO_PROBLEM = 0
SURFACE_DOES_NOT_EXIST = 1
IMAGE_DOES_NOT_EXIST = 2
