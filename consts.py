# consts.py
# List of Game Constants / Global Variables
import os
import pygame

CWD = os.getcwd()

GAME_NAME = "Sentience In Space"

KEYBINDINGS = os.path.join(CWD, "settings.config")

SCREEN_WIDTH = 640                          # pixels
SCREEN_HEIGHT = 480                         # pixels

MAP_DEFAULT = ""                            # default map configuration file
MAP_WIDTH = 1024                            # tiles
MAP_HEIGHT = 1024                           # tiles

TILE_SHEET = ""                             # sheet of non-animated images
TILE_WIDTH = 80                             # pixels
TILE_HEIGHT = 80                            # pixels
SHOW_TILES_W = SCREEN_WIDTH / TILE_WIDTH    # number of tiles across that are shown at any one time
SHOW_TILES_H = SCREEN_HEIGHT / TILE_HEIGHT  # number of tiles down that are shown at any one time

SPRITE_SHEETS = ["", ""]                    # strings of file names. probably going to create separate variables rather than use list
SPRITE_WIDTH = 80                           # pixels
SPRITE_HEIGHT = 80                          # pixels

CHARACTER_SPRITE_SHEET = os.path.join(CWD, "robot.png")
CHARACTER_WIDTH = 80                        # pixels
CHARACTER_HEIGHT = 188                      # pixels

MAIN_BG_IMAGE = os.path.join(CWD, "panda.png")

# Random Useful RGB Values
WHITE = pygame.Color(0xff, 0xff, 0xff, 0xff)
BLACK = pygame.Color(0x00, 0x00, 0x00, 0xff)
HOTPINK = pygame.Color(0xff, 0x69, 0xb4, 0xff)

COLOR_KEY = HOTPINK

# Error Codes
NO_PROBLEM = 0
SURFACE_DOES_NOT_EXIST = 1
IMAGE_DOES_NOT_EXIST = 2
