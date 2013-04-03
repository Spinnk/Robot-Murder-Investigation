#! /usr/bin/python

# consts.py
# List of Game Constants / Global Variables

# consts.py is part of Sentience in Space.
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
import os

import pygame

# Turn an integer into a hex string
makehex = lambda value, size = 1: eval(('"%.' + str(size)) + 'x"%' + str(value))

# Name of Game
GAME_NAME = "Sentience In Space"

# Non-Image Directories
CWD = os.path.split(os.path.abspath(__file__))[0]
ART_DIR = os.path.join( CWD, "art" )
KEYBINDINGS_DIR = os.path.join(CWD, "settings.config")
SAVE_DIR = os.path.join(CWD, "saves")
MUSIC_DIR = os.path.join(CWD, "music")

# Some quick scripting
os.environ['SDL_VIDEO_CENTERED'] = '1'
os.chdir(CWD)

# Framerate
FPS = 60

# Screen Stuff
BACKGROUND_IMAGE_DIR = os.path.join( ART_DIR, "background 1.png" )
SCREEN_WIDTH = 880                          # pixels
SCREEN_HEIGHT = 640                         # pixels

# Map Info
MAP_DEFAULT_DIR = os.path.join(CWD, "map.txt")
MAP_WIDTH = 15                              # tiles
MAP_HEIGHT = 15                             # tiles

# Tile Info
MAX_TILE_VALUE = 2

TILE_SHEET_DIR = os.path.join(ART_DIR, "tiles.png")
TILE_WIDTH = 80                             # pixels
TILE_HEIGHT = 80                            # pixels
TILE_SHOW_W = SCREEN_WIDTH / TILE_WIDTH     # number of tiles across that are shown at any one time
TILE_SHOW_H = SCREEN_HEIGHT / TILE_HEIGHT   # number of tiles down that are shown at any one time

TILE_SOLID = 0x01                           # mask for whether or not the tile can be walked through

TILE_INFO = [0,                             # index = tile type, clip; value is properties mask
             0,
             0]

# Character Info
CHARACTER_SPRITE_SHEET_DIR = os.path.join( ART_DIR, "robot.png")
CHARACTER_WIDTH = 80                        # pixels
CHARACTER_HEIGHT = 160                      # pixels

# NPC Info
NPCS = ["puppy", "panda", "koala", "spock"]
NPC_SHEETS_DIR = [os.path.join(ART_DIR, fname + ".png") for fname in NPCS]
NPC_WIDTH = 80                              # pixels
NPC_HEIGHT = 80                             # pixels
NPC_MAX_VALUE = 3
NPC_COUNT = 4

# Inventory Info
INVENTORY_BACKGROUND_SHEET_DIR = os.path.join(ART_DIR, "inventory.png")
INVENTORY_BUTTONS_DIR = os.path.join(ART_DIR, "option box.png")
INVENTORY_BUTTONS = [pygame.Rect(735, 566, 68, 38)] # location of buttons

# Items Info
ITEM_BOX_DIR = os.path.join(ART_DIR, "box.png")
ITEM_SHEET_LARGE_DIR = os.path.join(ART_DIR, "large items.png")
ITEM_LARGE_WIDTH = 200                      # pixels
ITEM_LARGE_HEIGHT = 200                     # pixels

ITEM_SHEET_SMALL_DIR = os.path.join(ART_DIR, "small items.png")
ITEM_SMALL_WIDTH = 80                       # pixels
ITEM_SMALL_HEIGHT = 80                      # pixels

# Items List
# Item Index = Type, Tile on sheet
# Item Name = first value
# item Descirption = second value; store in multiple strings to display nicely
ITEMS = [   ["Item 1", ["Item 1 Description", "Line 2", "Line 3"]],
            ["Item 2", ["Item 2 Description"]],
        	["Item 3", ["Item 3 Description", "Line 2"]]
        ]

ITEM_IMAGE_BOX = pygame.Rect(666, 37, 100, 100)        # location of items when displayed on screen; change as necessary
ITEM_NAME_BOX = pygame.Rect(665, 250, 100, 100)        # location of name when item is displayed
ITEM_DESCRIPTION_BOX = pygame.Rect(665, 300, 100, 100) # location of first line of descriptions

ITEMS_ON_MAP = 5

# Useful RGB Values
WHITE = pygame.Color(0xff, 0xff, 0xff, 0xff)
BLACK = pygame.Color(0x00, 0x00, 0x00, 0xff)
HOTPINK = pygame.Color(0xff, 0x69, 0xb4, 0xff)
YELLOW = pygame.Color(0xff, 0xff, 0x00, 0xff)

COLOR_KEY = HOTPINK

# States
MAIN_MENU_STATE = 0
IN_GAME_STATE = 1
LOAD_STATE = 2
SAVE_STATE = 3
EXIT_STATE = 4
SETTINGS_STATE = 5
IMJ_STATE = 6
PUZZLE_STATE = 7
OPTIONS_MENU_STATE = 8

# Keybindings Enum
KB_UP = 0
KB_LEFT = 1
KB_DOWN = 2
KB_RIGHT = 3
KB_USE = 4
KB_INVENTORY = 5
KB_ENTER = 6
KB_ESCAPE = 7

# Error Codes
NO_PROBLEM = 0
SURFACE_DOES_NOT_EXIST = 1
IMAGE_DOES_NOT_EXIST = 2
CHECKSUMS_DO_NOT_MATCH = 3
INCORRECT_FILE_FORMAT = 4
ITEM_DOES_NOT_EXIST = 5
INCORRECT_DATA_FORMAT = 6
INCORRECT_DATA_LENGTH = 7

# Music Info
MUSIC_FILES = []                                # list of music file names

# Font Info
FONT_DIR = os.path.join(CWD, "comic.ttf")
FONT_SIZE_LARGE = 24
FONT_SIZE_SMALL = 12
FONT_COLOR = BLACK
FONT_ANTIALIAS = True

# Save GUI Info
# might not be used
SAVE_SHOW = 5
SAVE_SHOW_BOX = pygame.Rect(300, 200, 100, 100)
SAVE_BACKGROUND_COLOR = YELLOW
SAVE_FONT_SIZE_LARGE = 32
SAVE_DISPLAY_BOX = pygame.Rect(150, 100, 100, 100)
SAVE_FONT_SIZE = 24
SAVE_INPUT_BOX = pygame.Rect(200, 300, 100, 100)
