# consts.py
# List of Game Constants / Global Variables
import os
import pygame

GAME_NAME = "Sentience In Space"

CWD = os.getcwd()
ART_LOCATION = os.path.join( CWD, "art" )

KEYBINDINGS = os.path.join(CWD, "settings.config")

SCREEN_WIDTH = 800                          # pixels
SCREEN_HEIGHT = 600                         # pixels

BACKGROUND_IMAGE = os.path.join( ART_LOCATION, "background 1.png" )

MAP_DEFAULT = os.path.join(CWD, "map.txt")  # default map configuration file
MAP_WIDTH = 1024                            # tiles
MAP_HEIGHT = 1024                           # tiles

NUM_TILE_TYPES = 256

TILE_SHEET = os.path.join(ART_LOCATION, "tiles.png")# sheet of non-animated images
TILE_WIDTH = 80                             # pixels
TILE_HEIGHT = 80                            # pixels
SHOW_TILES_W = SCREEN_WIDTH / TILE_WIDTH    # number of tiles across that are shown at any one time
SHOW_TILES_H = SCREEN_HEIGHT / TILE_HEIGHT  # number of tiles down that are shown at any one time

SPRITE_SHEETS = ["", ""]                    # strings of file names. probably going to create separate variables rather than use list
SPRITE_WIDTH = 80                           # pixels
SPRITE_HEIGHT = 80                          # pixels

CHARACTER_SPRITE_SHEET = os.path.join( ART_LOCATION, "robot.png")
CHARACTER_WIDTH = 80                        # pixels
CHARACTER_HEIGHT = 188                      # pixels

# Random Useful RGB Values
WHITE = pygame.Color(0xff, 0xff, 0xff, 0xff)
BLACK = pygame.Color(0x00, 0x00, 0x00, 0xff)
HOTPINK = pygame.Color(0xff, 0x69, 0xb4, 0xff)

COLOR_KEY = HOTPINK

# Error Codes
# maybe turn this into a map, and raise exception
NO_PROBLEM = 0
SURFACE_DOES_NOT_EXIST = 1
IMAGE_DOES_NOT_EXIST = 2
CHECKSUMS_DO_NOT_MATCH = 3
NO_DATA = 4
