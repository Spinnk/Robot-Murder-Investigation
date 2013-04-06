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

# Turn an integer into a big endian hex string
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

# Useful RGB Values
WHITE = pygame.Color(0xff, 0xff, 0xff, 0xff)
BLACK = pygame.Color(0x00, 0x00, 0x00, 0xff)
HOTPINK = pygame.Color(0xff, 0x69, 0xb4, 0xff)
YELLOW = pygame.Color(0xff, 0xff, 0x00, 0xff)
CYAN = pygame.Color(0x00, 0xff, 0xff, 0xff)

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

# Inventory Info
INVENTORY_BACKGROUND_SHEET_DIR = os.path.join(ART_DIR, "inventory.png")
INVENTORY_X = 8                             # spaces across
INVENTORY_Y = 7                             # spaces down
INVENTORY_BUTTONS_DIR = os.path.join(ART_DIR, "option box.png")
INVENTORY_BUTTONS = [pygame.Rect(735, 566, 68, 38)] # location of buttons

# Items Info
ITEM_BOX_DIR = os.path.join(ART_DIR, "box.png")
ITEM_FONT_DIR = os.path.join(CWD, "comic.ttf")
ITEM_FONT_DESCRIPTION = 12
ITEM_FONT_COUNT = 12
ITEM_FONT_NAME = 24
ITEM_FONT_COLOR = BLACK
ITEM_FONT_ANTIALIAS = True

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
ITEMS = [   ["", ""], # Item 0 is Null Item
            ["Item 1", ["Item 1 Description", "Line 2", "Line 3"]],
            ["Item 2", ["Item 2 Description"]],
        	["Item 3", ["Item 3 Description", "Line 2"]]
        ]

ITEM_IMAGE_BOX = pygame.Rect(666, 37, 100, 100)        # location of items when displayed on screen; change as necessary
ITEM_NAME_BOX = pygame.Rect(665, 250, 100, 100)        # location of name when item is displayed
ITEM_DESCRIPTION_BOX = pygame.Rect(665, 300, 100, 100) # location of first line of descriptions

ITEMS_ON_MAP = 5

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
JOURNAL = [ # [title, array of lines]
            ["Farewell to the Old Guard", [ "Soldiers of my Old Guard:",
                                            "",
                                            "I bid you farewell. For twenty years I have constantly",
                                            "accompanied you on the road to honor and glory. In these",
                                            "latter times, as in the days of our prosperity, you have",
                                            "invariably been models of courage and fidelity. With men",
                                            "such as you our cause could not be lost; but the war",
                                            "would have been interminable; it would have been civil",
                                            "war, and that would have entailed deeper misfortunes on",
                                            "France.",
                                            "I have sacrificed all of my interests to those of the",
                                            "country.",
                                            "I go, but you, my friends, will continue to serve France.",
                                            "Her happiness was my only thought. It will still be the",
                                            "object of my wishes. Do not regret my fate; if I have",
                                            "consented to survive, it is to serve your glory. I intend",
                                            "to write the history of the great achievements we have",
                                            "performed together. Adieu, my friends. Would I could press",
                                            "you all to my heart.",
                                            "",
                                            "April 20, 1814."]],
            ["Title 2", ["Line 1", "Line 2"]],
            ["Title3", ["Line 1", "Line 2", "Line 3", "Line 4"]],
            ["The Gettysburg Address", ["Four score and seven years ago our fathers brought",
                                        "forth on this continent, a new nation, conceived in",
                                        "Liberty, and dedicated to the proposition that all",
                                        "men are created equal.",
                                        "",
                                        "Now we are engaged in a great civil war, testing",
                                        "whether that nation, or any nation so conceived and",
                                        "so dedicated, can long endure. We are met on a great",
                                        "battle-field of that war. We have come to dedicate a",
                                        "portion of that field, as a final resting place for",
                                        "those who here gave their lives that that nation",
                                        "might live. It is altogether fitting and proper that",
                                        "we should do this.",
                                        "",
                                        "But, in a larger sense, we can not dedicate -- we",
                                        "can not consecrate -- we can not hallow -- this",
                                        "ground. The brave men, living and dead, who",
                                        "struggled here, have consecrated it, far above our",
                                        "poor power to add or detract. The world will little",
                                        "note, nor long remember what we say here, but it can",
                                        "never forget what they did here. It is for us the",
                                        "living, rather, to be dedicated here to the unfinished",
                                        "work which they who fought here have thus far so nobly",
                                        "advanced. It is rather for us to be here dedicated to",
                                        "the great task remaining before us -- that from these honored",
                                        "dead we take increased devotion to that cause for which they",
                                        "gave the last full measure of devotion -- that we here",
                                        "highly resolve that these dead shall not have died in vain",
                                        "-- that this nation, under God, shall have a new birth of",
                                        "freedom -- and that government of the people, by the people,",
                                        "for the people, shall not perish from the earth."]]
            ]
