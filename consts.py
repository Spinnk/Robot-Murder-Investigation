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

CHARACTER_SPRITE_SHEET = os.path.join(os.getcwd(), "soldier.png")
CHARACTER_WIDTH = 40        # pixels
CHARACTER_HEIGHT = 40       # pixels
CHARACTER_VX = 250          # change depending on pixel or tile
CHARACTER_VY = 250          # change depending on pixel or tile

# RBG Value for Hot Pink
COLOR_KEY_R = 0xff
COLOR_KEY_G = 0x69
COLOR_KEY_B = 0xb4
COLOR_KEY_A = 0xff
COLOR_KEY = pygame.Color(COLOR_KEY_R, COLOR_KEY_G, COLOR_KEY_B, COLOR_KEY_A) 

# Error Codes
NO_PROBLEM = 0
SURFACE_DOES_NOT_EXIST = 1
IMAGE_DOES_NOT_EXIST = 2
