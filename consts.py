#! /usr/bin/python

# consts.py
# List of Global Variables

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

#from settings import *
from specialfunctions import *

# Name of Game
GAME_NAME = "Sentience In Space"

# Non-Image Directories
CWD = os.path.split(os.path.abspath(__file__))[0]
ART_DIR = os.path.join( CWD, "art" )
SAVE_DIR = os.path.join(CWD, "saves")
SOUND_DIR = os.path.join(CWD, "sound")

# Framerate
FPS = 60

# Screen Stuff
BACKGROUND_IMAGE_DIR = os.path.join( ART_DIR, "background 1.png" )
SCREEN_WIDTH = 880                          # pixels
SCREEN_HEIGHT = 640                         # pixels

# Useful RGB Values
WHITE =   pygame.Color(0xff, 0xff, 0xff, 0xff)
BLACK =   pygame.Color(0x00, 0x00, 0x00, 0xff)
HOTPINK = pygame.Color(0xff, 0x69, 0xb4, 0xff)
YELLOW =  pygame.Color(0xff, 0xff, 0x00, 0xff)
CYAN =    pygame.Color(0x00, 0xff, 0xff, 0xff)
BLUE =    pygame.Color(0x00, 0x00, 0xff, 0xff)

COLOR_KEY = HOTPINK

# Keybindings Enum
# special case positioning of global variables
# should never be touched by users
KB_UP = 0
KB_LEFT = 1
KB_DOWN = 2
KB_RIGHT = 3
KB_USE = 4
KB_INVENTORY = 5
KB_JOURNAL = 6
KB_ENTER = 7
KB_ESCAPE = 8
KB_LIFT = 9
KB_MAP = 10

KB_NAMES = [    "UP",
                "LEFT",
                "DOWN",
                "RIGHT",
                "USE",
                "INVENTORY",
                "JOURNAL",
                "ENTER",
                "ESCAPE",
                "LIFT",
                "MAP"]

# default settings
# assumes variables are already global
def defaultsettings():
    return {KB_UP: pygame.K_w,
            KB_LEFT: pygame.K_a,
            KB_DOWN: pygame.K_s,
            KB_RIGHT: pygame.K_d,
            KB_USE: pygame.K_e,
            KB_INVENTORY: pygame.K_i,
            KB_JOURNAL: pygame.K_j,
            KB_ENTER: pygame.K_RETURN,
            KB_ESCAPE: pygame.K_ESCAPE,
            KB_LIFT: pygame.K_l,
            KB_MAP: pygame.K_m
            }, 1.0, 1.0

def readsettings(file_name):
    f = open(file_name, 'r')
    settings = f.readlines()
    f.close()
    i = 0
    keybindings, volume, brightness = defaultsettings()
    while i < len(settings):
        if settings[i][0] == '#':
            i += 1
            continue
        elif settings[i] == '-----BEGIN KEYBINDINGS-----\n':
            i += 1
            while settings[i] != '-----END KEYBINDINGS-----\n':
                line = settings[i]
                if line[0] == '#':
                    continue
                line = line[:-1]        # remove newline char
                if line[:2] == 'Up':
                    keybindings[KB_UP] = int(line[3:])
                elif line[:4] == 'Left':
                    keybindings[KB_LEFT] = int(line[5:])
                elif line[:4] == 'Down':
                    keybindings[KB_DOWN] = int(line[5:])
                elif line[:5] == 'Right':
                    keybindings[KB_RIGHT] = int(line[6:])
                elif line[:3] == 'Use':
                    keybindings[KB_USE] = int(line[4:])
                elif line[:9] == 'Inventory':
                    keybindings[KB_INVENTORY] = int(line[10:])
                elif line[:7] == "Journal":
                    keybindings[KB_JOURNAL] = int(line[8:])
                elif line[:5] == 'Enter':
                    keybindings[KB_ENTER] = int(line[6:])
                elif line[:6] == 'Escape':
                    keybindings[KB_ESCAPE] = int(line[7:])
                elif line[:4] == 'Lift':
                    keybindings[KB_LIFT] = int(line[5:])
                elif line[:3] == 'Map':
                    keybindings[KB_LIFT] = int(line[4:])
                i += 1
        elif settings[i] == '-----BEGIN MUSIC SETTINGS-----\n':
            i += 1
            while settings[i] != '-----END MUSIC SETTINGS-----\n':
                line = settings[i]
                if line[0] == '#':
                    continue
                line = line[:-1]        # remove newline char
                if line[:6] == 'Volume':
                    volume = int(line[7:])
                i += 1
        elif settings[i] == '-----BEGIN SCREEN SETTINGS-----\n':
            i += 1
            while settings[i] != '-----END SCREEN SETTINGS-----\n':
                line = settings[i]
                if line[0] == '#':
                    continue
                line = line[:-1]        # remove newline char
                if line[:10] == 'Brightness':
                    brightness = int(line[11:])
                i += 1
        i += 1
        return keybindings, volume, brightness

def writesettings(file_name, keybindings, volume, brightness):
    f = open(file_name, 'w')
    f.write('# Sentience in Space\n' +
            '\n-----BEGIN KEYBINDINGS-----' +
            '\nUp=' + str(keybindings[KB_UP]) +
            '\nLeft=' + str(keybindings[KB_LEFT]) +
            '\nDown=' + str(keybindings[KB_DOWN]) +
            '\nRight=' + str(keybindings[KB_RIGHT]) +
            '\nUse=' + str(keybindings[KB_USE]) +
            '\nInventory=' + str(keybindings[KB_INVENTORY]) +
            '\nJournal=' + str(keybindings[KB_JOURNAL]) +
            '\nEnter=' + str(keybindings[KB_ENTER]) +
            '\nEscape=' + str(keybindings[KB_ESCAPE]) +
            '\nLift=' + str(keybindings[KB_LIFT]) +
            '\nMap=' + str(keybindings[KB_MAP]) +
            '\n-----END KEYBINDINGS-----'
            '\n'
            '\n-----BEGIN MUSIC SETTINGS-----' +
            '\nVolume=' + str(volume) +
            '\n-----END MUSIC SETTINGS-----' +
            '\n'
            '\n-----BEGIN SCREEN SETTINGS-----' +
            '\nBrightness=' + str(brightness) +
            '\n-----END SCREEN SETTINGS-----' +
            '\n')
    f.close()


# Settings
SETTINGS_DIR = os.path.join(CWD, "settings.config")
SETTINGS_SLIDER_WIDTH = 400
SETTINGS_SLIDER_HEIGHT = 20
SETTINGS_BOXES = [  pygame.Rect(220, 100, SETTINGS_SLIDER_WIDTH, SETTINGS_SLIDER_HEIGHT),   # KB_UP
                    pygame.Rect(220, 130, SETTINGS_SLIDER_WIDTH, SETTINGS_SLIDER_HEIGHT),   # KB_LEFT
                    pygame.Rect(220, 160, SETTINGS_SLIDER_WIDTH, SETTINGS_SLIDER_HEIGHT),   # KB_DOWN
                    pygame.Rect(220, 190, SETTINGS_SLIDER_WIDTH, SETTINGS_SLIDER_HEIGHT),   # KB_RIGHT
                    pygame.Rect(220, 220, SETTINGS_SLIDER_WIDTH, SETTINGS_SLIDER_HEIGHT),   # KB_USE
                    pygame.Rect(220, 250, SETTINGS_SLIDER_WIDTH, SETTINGS_SLIDER_HEIGHT),   # KB_INVENTORY
                    pygame.Rect(220, 280, SETTINGS_SLIDER_WIDTH, SETTINGS_SLIDER_HEIGHT),   # KB_JOURNAL
                    pygame.Rect(220, 310, SETTINGS_SLIDER_WIDTH, SETTINGS_SLIDER_HEIGHT),   # KB_ENTER
                    pygame.Rect(220, 340, SETTINGS_SLIDER_WIDTH, SETTINGS_SLIDER_HEIGHT),   # KB_ESCAPE
                    pygame.Rect(220, 370, SETTINGS_SLIDER_WIDTH, SETTINGS_SLIDER_HEIGHT),   # KB_LIFT
                    pygame.Rect(220, 400, SETTINGS_SLIDER_WIDTH, SETTINGS_SLIDER_HEIGHT),   # KB_MAP
                    pygame.Rect(220, 460, SETTINGS_SLIDER_WIDTH, SETTINGS_SLIDER_HEIGHT),   # volume
                    pygame.Rect(220, 500, SETTINGS_SLIDER_WIDTH, SETTINGS_SLIDER_HEIGHT)]   # brightness

SETTINGS_BACKGROUND_COLORS = [YELLOW, CYAN]
SETTINGS_BACKGROUND_BOX = pygame.Rect(140, -5, 600, 40)
SETTINGS_FONT_DIR = os.path.join(CWD, "comic.ttf")
SETTINGS_FONT_SIZE = 24
SETTINGS_FONT_COLOR = BLACK
SETTINGS_FONT_ANTIALIAS = True

KEY_FONT_DIR = os.path.join(CWD, "comic.ttf")
KEY_FONT_SIZE = 24
KEY_FONT_COLOR = BLACK
KEY_FONT_ANTIALIAS = True

KEYBINDINGS, SOUND_VOLUME, SCREEN_BRIGHTNESS = readsettings(SETTINGS_DIR)

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
DIALOGUE_NOT_INITIALIZED = 10
NOTHING_DONE = 11

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
CHARACTER_FRAMES = 5
CHARACTER_WALK_TIME = 400                   # milliseconds to cross 1 tile
CHARACTER_TPF = CHARACTER_WALK_TIME / CHARACTER_FRAMES

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
PUZZLE_RULES = os.path.join(CWD, "puzzle rules.txt")
PUZZLE_FONT_DIR = os.path.join(CWD, "comic.ttf")
PUZZLE_FONT_TITLE_SIZE = 18
PUZZLE_FONT_RULES_SIZE = 16
PUZZLE_FONT_COLOR = BLACK
PUZZLE_FONT_BACKGROUND_COLORS = [YELLOW, CYAN]
PUZZLE_FONT_ANTIALIAS = True
PUZZLE_FAIL = 0
PUZZLE_WORKING = 1
PUZZLE_SUCCESS = 2

# Inventory Info
INVENTORY_BACKGROUND_SHEET_DIR = os.path.join(ART_DIR, "inventory.png")
INVENTORY_X = 8                             # spaces across
INVENTORY_Y = 7                             # spaces down
INVENTORY_SPACES = INVENTORY_X * INVENTORY_Y
INVENTORY_BUTTON = pygame.Rect(700, 500, 100, 100) # location and text of buttons
INVENTORY_FONT_DIR = os.path.join(CWD, "comic.ttf")
INVENTORY_FONT_SIZE = 18
INVENTORY_FONT_COLOR = BLACK
INVENTORY_FONT_ANTIALIAS = True
INVENTORY_BACKGROUND_COLOR = YELLOW

# Items Info
ITEM_SHEET_LARGE_DIR = os.path.join(ART_DIR, "large items.png")
ITEM_LARGE_WIDTH = 200                      # pixels
ITEM_LARGE_HEIGHT = 200                     # pixels

ITEM_SHEET_SMALL_DIR = os.path.join(ART_DIR, "small items.png")
ITEM_SMALL_WIDTH = 80                       # pixels
ITEM_SMALL_HEIGHT = 80                      # pixels

ITEM_BOX_DIR = os.path.join(ART_DIR, "item selected.png")        # box for highlighting selected item

ITEM_OPTIONS = ["Cancel", "Drop", "Read", "Use"]

# Items List
# Index is Item Type and Number
#   Subarray Indexes:
#       0 - Item Name
#       1 - Description (store in multiple strings)
#       2 - Inventory Buttons ("Cancel" must always be availible)
ITEMS = [   ["", [""], []], # Item 0 is Null Item
            ["Book", ["Read a book", "Read a book", "Read an important book"], ["Cancel", "Drop", "Read"]],
            ["Not Book", ["Not a book"], ["Cancel", "Drop", "Use"]],
        	["Not a book either", ["Not a book", "Still not a book"], ["Cancel", "Drop", "Use"]]
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
SOUND_DIRS = [os.path.join(SOUND_DIR, "tetris1.mid")]                                # list of music file names


# Journal Info
JOURNAL_BACKGROUND_DIR = os.path.join(ART_DIR, "journal.png")
JOURNAL_FILE_DIR = os.path.join(CWD, "journal entries.txt")
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
JOURNAL = parsejournal(JOURNAL_FILE_DIR)

# In Game Map Info
INGAMEMAP_CHARACTER_MARKER_DIR = os.path.join(ART_DIR, "robot marker.png")
INGAMEMAP_MISSION_MARKER_DIR = os.path.join(ART_DIR, "mission marker.png")

# Dialogue Info
DIALOGUE = parsedialogue('')
