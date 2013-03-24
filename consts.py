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
ART_LOCATION = os.path.join( CWD, "art" )

KEYBINDINGS = os.path.join(CWD, "settings.config")

SCREEN_WIDTH = 880                          # pixels
SCREEN_HEIGHT = 640                         # pixels

MAP_DEFAULT = os.path.join(CWD, "map.txt")  # default map configuration file
MAP_WIDTH = 1024                            # tiles
MAP_HEIGHT = 1024                           # tiles

MAX_TILE_VALUE = 2

TILE_SHEET = os.path.join(ART_LOCATION, "tiles.png") # tiles
TILE_WIDTH = 80                             # pixels
TILE_HEIGHT = 80                            # pixels
SHOW_TILES_W = SCREEN_WIDTH / TILE_WIDTH    # number of tiles across that are shown at any one time
SHOW_TILES_H = SCREEN_HEIGHT / TILE_HEIGHT  # number of tiles down that are shown at any one time

BACKGROUND_IMAGE = os.path.join( ART_LOCATION, "background 1.png" )

SPRITE_SHEETS = ["", ""]                    # strings of file names. probably going to create separate variables rather than use list
SPRITE_WIDTH = 80                           # pixels
SPRITE_HEIGHT = 80                          # pixels

CHARACTER_SPRITE_SHEET = os.path.join( ART_LOCATION, "robot.png")
CHARACTER_WIDTH = 80                        # pixels
CHARACTER_HEIGHT = 160                      # pixels

INVENTORY_BACKGROUND_SHEET = os.path.join(ART_LOCATION, "inventory.png") # main inventory screen
ITEM_COUNT = 6                              # max items in displayed list; reest are hidden
ITEM_LIST_BOX = pygame.Rect(0, 0, 0, 0)     # first line of unselected items list

ITEM_SHEET_LARGE = os.path.join(ART_LOCATION, "large items.png") # larger item images
ITEM_LARGE_WIDTH = 80                       # pixels
ITEM_LARGE_HEIGHT = 80                      # pixels

ITEM_SHEET_SMALL = os.path.join(ART_LOCATION, "small items.png") # smaller item images
ITEM_SMALL_WIDTH = 200                      # pixels
ITEM_SMALL_HEIGHT = 200                     # pixels

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

# Random Useful RGB Values
WHITE = pygame.Color(0xff, 0xff, 0xff, 0xff)
BLACK = pygame.Color(0x00, 0x00, 0x00, 0xff)
HOTPINK = pygame.Color(0xff, 0x69, 0xb4, 0xff)

COLOR_KEY = HOTPINK

# Error Codes
NO_PROBLEM = 0
SURFACE_DOES_NOT_EXIST = 1
IMAGE_DOES_NOT_EXIST = 2
CHECKSUMS_DO_NOT_MATCH = 3
INCORRECT_FILE_FORMAT = 4
ITEM_DOES_NOT_EXIST = 5
