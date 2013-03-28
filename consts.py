# consts.py
# List of Game Constants / Global Variables

# maybe use this file as initializer
# open images here and import them
# into other files

from math import ceil
import os

import pygame

GAME_NAME = "Sentience In Space"

CWD = os.path.split(os.path.abspath(__file__))[0]
os.chdir(CWD)
ART_DIR = os.path.join( CWD, "art" )

FPS = 60

KEYBINDINGS_DIR = os.path.join(CWD, "settings.config")

BACKGROUND_IMAGE_DIR = os.path.join( ART_DIR, "background 1.png" )
SCREEN_WIDTH = 880                          # pixels
SCREEN_HEIGHT = 640                         # pixels

MAP_DEFAULT_DIR = os.path.join(CWD, "map.txt")  # default map configuration file
MAP_WIDTH = 128                             # tiles
MAP_HEIGHT = 128                            # tiles

MAX_TILE_VALUE = 2

TILE_SHEET_DIR = os.path.join(ART_DIR, "tiles.png") # tiles
TILE_WIDTH = 80                             # pixels
TILE_HEIGHT = 80                            # pixels
SHOW_TILES_W = SCREEN_WIDTH / TILE_WIDTH    # number of tiles across that are shown at any one time
SHOW_TILES_H = SCREEN_HEIGHT / TILE_HEIGHT  # number of tiles down that are shown at any one time

TILE_SOLID = 0x01                           # mask for whether or not the tile can be walked through

TILE_INFO = [0,                             # index = tile type, clip; value is properties mask
             0,
             0
            ]

NPC_SHEETS_DIR = []                         # strings of file names. probably going to create separate variables rather than use list
NPC_WIDTH = 80                              # pixels
NPC_HEIGHT = 80                             # pixels
NPC_MAX_VALUE = 0
NPC_COUNT = 0
NPC_DIRS = [os.path.join(ART_DIR, "puppy.png"), # nams of "extra" npcs
            os.path.join(ART_DIR, "panda.png"),
            os.path.join(ART_DIR, "koala.png"),
            os.path.join(ART_DIR, "spock.png")
            ]
	    
CHARACTER_SPRITE_SHEET_DIR = os.path.join( ART_DIR, "robot.png")
CHARACTER_WIDTH = 80                        # pixels
CHARACTER_HEIGHT = 160                      # pixels

INVENTORY_BACKGROUND_SHEET_DIR = os.path.join(ART_DIR, "inventory.png") # main inventory screen

ITEM_SHEET_LARGE_DIR = os.path.join(ART_DIR, "large items.png") # larger item images (displaying in inventory menu)
ITEM_LARGE_WIDTH = 200                       # pixels
ITEM_LARGE_HEIGHT = 200                      # pixels

ITEM_SHEET_SMALL_DIR = os.path.join(ART_DIR, "small items.png") # smaller item images (maybe for displaying on tiles)
ITEM_SMALL_WIDTH = 80                      # pixels
ITEM_SMALL_HEIGHT = 80                     # pixels

# Items list
# Item Index = Type, Tile on sheet
# Item Name = first value
# item Descirption = second value; store in multiple strings to display nicely
ITEMS = [   ["Item 0", ["Item 0 Description"]],
            ["Item 1", ["Item 1 Description"]]
        ]

ITEM_IMAGE_BOX = pygame.Rect(0, 0, 100, 100)        # location of items when displayed on screen; change as necessary
ITEM_NAME_BOX = pygame.Rect(0, 0, 100, 100)         # location of name when item is displayed
ITEM_DESCRIPTION_BOX = pygame.Rect(0, 0, 100, 100)  # location of first line of descriptions

# Useful RGB Values
WHITE = pygame.Color(0xff, 0xff, 0xff, 0xff)
BLACK = pygame.Color(0x00, 0x00, 0x00, 0xff)
HOTPINK = pygame.Color(0xff, 0x69, 0xb4, 0xff)

COLOR_KEY = HOTPINK

#Save Info
SAVE_FILE = os.path.join( CWD, "save.txt" )



# States
MAIN_MENU_STATE = 0
IN_GAME_STATE = 1
LOAD_STATE = 2
SAVE_STATE = 3
EXIT_STATE = 4
SETTINGS_STATE = 5
INVENTORY_STATE = 6
PUZZLE_STATE = 7
OPTIONS_MENU_STATE = 8

# Keybindings
KB_UP = 0
KB_LEFT = 1
KB_DOWN = 2
KB_RIGHT = 3
KB_USE = 4

# Error Codes
NO_PROBLEM = 0
SURFACE_DOES_NOT_EXIST = 1
IMAGE_DOES_NOT_EXIST = 2
CHECKSUMS_DO_NOT_MATCH = 3
INCORRECT_FILE_FORMAT = 4
ITEM_DOES_NOT_EXIST = 5

MUSIC_FILES = []                                # list of music file names
