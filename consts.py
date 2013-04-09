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
import sys

import pygame

from specialfunctions import *

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

# Useful RGB Values
WHITE = pygame.Color(0xff, 0xff, 0xff, 0xff)
BLACK = pygame.Color(0x00, 0x00, 0x00, 0xff)
HOTPINK = pygame.Color(0xff, 0x69, 0xb4, 0xff)
YELLOW = pygame.Color(0xff, 0xff, 0x00, 0xff)
CYAN = pygame.Color(0x00, 0xff, 0xff, 0xff)

COLOR_KEY = HOTPINK

# Keybindings Enum
KB_UP = 0
KB_LEFT = 1
KB_DOWN = 2
KB_RIGHT = 3
KB_USE = 4
KB_INVENTORY = 5
KB_JOURNAL = 6
KB_ENTER = 7
KB_ESCAPE = 8

# Error Codes
NO_PROBLEM = 0
SURFACE_DOES_NOT_EXIST = 1
IMAGE_DOES_NOT_EXIST = 2
CHECKSUMS_DO_NOT_MATCH = 3
INCORRECT_FILE_FORMAT = 4
ITEM_DOES_NOT_EXIST = 5
INCORRECT_DATA_FORMAT = 6
INCORRECT_DATA_LENGTH = 7
NO_SPACE_IN_INEVENTORY = 8
NOT_FOUND = 9

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
NPC_FONT_DIR = os.path.join(CWD, "comic.ttf")
NPC_FONT_SIZE = 24
NPC_FONT_COLOR = BLACK
NPC_FONT_ANTIALIAS = True
NPC_TEXT_BOX = pygame.Rect(0, 500, 880, 40)

# Puzzle Info
PUZZLE_BACKGROUND_DIR = os.path.join(ART_DIR, "puzzle.png")
PUZZLE_ITEM_DIR = os.path.join(ART_DIR, "puzzle items.png")
PUZZLE_SELECTED_DIR = os.path.join(ART_DIR, "puzzle selected.png")
PUZZLE_MAP = os.path.join(CWD, "puzzle map.txt")
PUZZLE_FAIL = 0
PUZZLE_WORKING = 1
PUZZLE_SUCCESS = 2

# Inventory Info
INVENTORY_BACKGROUND_SHEET_DIR = os.path.join(ART_DIR, "inventory.png")
INVENTORY_X = 8                             # spaces across
INVENTORY_Y = 7                             # spaces down
INVENTORY_BUTTONS_DIR = os.path.join(ART_DIR, "option box.png")
INVENTORY_BUTTONS = [pygame.Rect(735, 566, 68, 38)] # location of buttons

# Items Info
ITEM_SHEET_LARGE_DIR = os.path.join(ART_DIR, "large items.png")
ITEM_LARGE_WIDTH = 200                      # pixels
ITEM_LARGE_HEIGHT = 200                     # pixels

ITEM_SHEET_SMALL_DIR = os.path.join(ART_DIR, "small items.png")
ITEM_SMALL_WIDTH = 80                       # pixels
ITEM_SMALL_HEIGHT = 80                      # pixels

ITEM_BOX_DIR = os.path.join(ART_DIR, "box.png")        # box for highlighting selected item

# Items List
# Item Index = Type, Tile on sheet
# Item Name = first value
# item Descirption = second value; store in multiple strings to display nicely
ITEMS = [   ["", ""], # Item 0 is Null Item
            ["Item 1", ["Item 1 Description", "Line 2", "Line 3"]],
            ["Item 2", ["Item 2 Description"]],
        	["Item 3", ["Item 3 Description", "Line 2"]]
        ]

ITEM_IMAGE_BOX = pygame.Rect(666, 37, 100, 100)        # location of items when displayed on screen; change as necessary
ITEM_NAME_BOX = pygame.Rect(665, 250, 100, 100)        # location of name when item is displayed
ITEM_DESCRIPTION_BOX = pygame.Rect(665, 300, 100, 100) # location of first line of descriptions
ITEM_FONT_DIR = os.path.join(CWD, "comic.ttf")
ITEM_FONT_DESCRIPTION = 12
ITEM_FONT_COUNT = 12
ITEM_FONT_NAME = 24
ITEM_FONT_COLOR = BLACK
ITEM_FONT_ANTIALIAS = True

# Music Info
MUSIC_FILES = []                                # list of music file names

# Journal Info
JOURNAL_BACKGROUND_DIR = os.path.join(ART_DIR, "journal.png")
JOURNAL_LIST_BOX = pygame.Rect(10, 0, 0, 0)      # where to start displaying titles
JOURNAL_SHOW_BOX = pygame.Rect(350, 0, 0, 0)     # where to start displaying data
JOURNAL_MAX_SHOW = 25                            # max number of entries to list
JOURNAL_MAX_LINES = 25                           # max lines to display in data area
JOURNAL_FONT_DIR = os.path.join(CWD, "comic.ttf")
JOURNAL_FONT_LIST_SIZE = 20
JOURNAL_FONT_SMALL_SIZE = 16
JOURNAL_FONT_LARGE_SIZE = 24
JOURNAL_FONT_COLOR = BLACK
JOURNAL_FONT_BACKGROUND_COLORS = [YELLOW, CYAN]
JOURNAL_FONT_ANTIALIAS = True
JOURNAL = parsejournal(os.path.join(CWD, "journal entries.txt"))

# In Game Map Info
INGAMEMAP_CHARACTER_MARKER_DIR = os.path.join(ART_DIR, "robot marker.png")
INGAMEMAP_MISSION_MARKER_DIR = os.path.join(ART_DIR, "mission marker.png")

# Dialogue Info
DIALOGUE = parsedialogue('')
