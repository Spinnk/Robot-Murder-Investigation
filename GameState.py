#! /usr/bin/python

# GameState and all its inherited classes
#
# The GameState class provides the foundation for the possible game states.
# Included in this file are the LoadGameState, SaveGameState, IMJState (for
# displaying the inventory/map/journal), MainMenuState, InGameState and
# OptionsMenuState.
#
# These states each recieve input through an update() function and print to the
# screen using a display() function. The update() function returns an integer
# representation of the state the game should be in, given the input.

# GameState.py is part of Sentience in Space.
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

import os, sys, pygame, hashlib

from consts import *
from menu import *
from character import *
from npc import *
from shiplayout import *
from inventory import *
from keybinding import *


#-------------------------------------------------------------------------------
#---[ GameState Class ]---------------------------------------------------------
#-------------------------------------------------------------------------------
## This class is used as a template to allow easy transition between game states
## by declaring common functionality
class GameState:
    def __init__(self, screen):
        pass

    def update(self, event):
        pass

    def display(self):
        pass

#-------------------------------------------------------------------------------
#---[ LoadGameState Class ]-----------------------------------------------------
#-------------------------------------------------------------------------------
## This class handles loading a game from a save file
#
class LoadGameState (GameState):
    def __init__(self, screen = None):
        pass

    def load(self, save_location):
        f = open(save_location, 'rb')
	data = f.read()
	f.close()
	checksum = data[-64:]
	data = data[:-64]
	if hashlib.sha512(data).digest() != checksum:
		return CHECKSUMS_DO_NOT_MATCH, None, None, None
	c_len = int(binascii.hexlify(data[:2]), 16); data = data[2:]
	c = Character(CHARACTER_SPRITE_SHEET_DIR); c.load(data[:c_len]); data = data[c_len:]
	i_len = int(binascii.hexlify(data[:2]), 16); data = data[2:]
	i = Inventory(INVENTORY_BACKGROUND_SHEET_DIR, ITEM_SHEET_SMALL_DIR, ITEM_SHEET_LARGE_DIR, ITEM_BOX_DIR, INVENTORY_BUTTONS_DIR); i.load(data[:i_len]); data = data[i_len:]
	s_len = int(binascii.hexlify(data[:2]), 16); data = data[2:]
	s = ShipLayout(TILE_SHEET_DIR, ITEM_SHEET_SMALL_DIR); s.load(data[:s_len]); data = data[s_len:]
	npc_count = int(binascii.hexlify(data[:2]), 16); data = data[2:]

	ns = []
	for x in xrange(npc_count):
		n_len = int(binascii.hexlify(data[:2]), 16); data = data[2:]
		n = NPC(); n.load(data[:n_len]); data = data[n_len:]
	if len(data):
		return INCORRECT_DATA_LENGTH, None, None, None
	return c, i, s, ns



    def update(self, event):
        pass

    def display(self):
        pass

#-------------------------------------------------------------------------------
#---[ SaveGameState Class ]-----------------------------------------------------
#-------------------------------------------------------------------------------
## This class handles save
#
class SaveGameState (GameState):
    def __init__(self, screen = None):
        pass

    def update(self, event):
        pass

    def save(self, save_location, character, inventory, ship, npcs):
	c = character.save()
	i = inventory.save()
	s = ship.save()
	ns = [npc.save() for npc in npcs]
	out = binascii.unhexlify(makehex(len(c), 4)) + c + binascii.unhexlify(makehex(len(i), 4)) + i + binascii.unhexlify(makehex(len(s), 4)) + s + binascii.unhexlify(makehex(len(ns), 4)) + ''.join([binascii.unhexlify(makehex(len(n), 4)) + n for n in ns])
	out += hashlib.sha512(out).digest()
	f = open(save_location, 'wb')
	f.write(out)
	f.close()
	return NO_PROBLEM

    def display(self):
        pass


#-------------------------------------------------------------------------------
#---[ IMJState Class ]----------------------------------------------------------
#-------------------------------------------------------------------------------
## This class is used to handle the Inventory/Map/Journal State
#
class IMJState (GameState):
    def __init__(self, screen, keybindings):
        self.inventory = Inventory(INVENTORY_BACKGROUND_SHEET_DIR, ITEM_SHEET_SMALL_DIR, ITEM_SHEET_LARGE_DIR, ITEM_BOX_DIR, INVENTORY_BUTTONS_DIR)
        self.screen = screen
        self.keybindings = keybindings

    def update(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.keybindings[KB_INVENTORY]:
            return IN_GAME_STATE
        self.inventory.update(pygame.key.get_pressed(), self.keybindings)
        return INVENTORY_STATE

    def newinventory(self, inventory):
        self.inventory = inventory

    def display(self):
        self.inventory.display(self.screen)



#-------------------------------------------------------------------------------
#---[ MainMenuState Class ]-----------------------------------------------------
#-------------------------------------------------------------------------------
## This class handles the functionality for the main menu (allowing "new game,"
## "load game" and "exit" options)
#
class MainMenuState (GameState):

    def __init__(self, screen, save_exists):
        self.save_exists = save_exists

        self.menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                            [('New Game', IN_GAME_STATE, None, True),
                             ('Load Game', LOAD_STATE, None, self.save_exists),
                             ('Quit', EXIT_STATE, None, True)])

        self.menu.set_center(True, True)
        self.menu.set_alignment('center', 'center')

    def update(self, event):
        state = MAIN_MENU_STATE
        if event.type == pygame.KEYDOWN or event.type == EVENT_CHANGE_STATE:
            rectList, state = self.menu.update(event, MAIN_MENU_STATE)
        return state

    def display(self):
        self.menu.draw_buttons()

#-------------------------------------------------------------------------------
#---[ InGameState Class ]-------------------------------------------------------
#-------------------------------------------------------------------------------
## This class handles the functionality for in-game actions and display
#
class InGameState (GameState):
    # initialize with only map
    def __init__(self, screen, keybindings):
        self.screen = screen
        self.keybindings = keybindings
        self.inventory = Inventory(INVENTORY_BACKGROUND_SHEET_DIR, ITEM_SHEET_SMALL_DIR, ITEM_SHEET_LARGE_DIR, ITEM_BOX_DIR, INVENTORY_BUTTONS_DIR)

        self.user = Character(CHARACTER_SPRITE_SHEET_DIR)
        self.ship = ShipLayout(TILE_SHEET_DIR, ITEM_SHEET_SMALL_DIR)
        self.ship.loadmap(MAP_DEFAULT_DIR)

        self.ship.additem((1,1), 1)
        self.ship.additem((1,4), 2)
        self.ship.additem((3,3), 0)

        self.character_sprite_sheet = pygame.image.load(CHARACTER_SPRITE_SHEET_DIR)
        self.tile_sheet = pygame.image.load(TILE_SHEET_DIR)
        self.npc_sheets = [pygame.image.load(npc_file) for npc_file in NPC_SHEETS_DIR]

        if self.character_sprite_sheet == None:
            return IMAGE_DOES_NOT_EXIST
        if self.tile_sheet == None:
            return IMAGE_DOES_NOT_EXIST
        for sheet in self.npc_sheets:
            if sheet == None:
                return IMAGE_DOES_NOT_EXIST

        self.tile_sheet.set_colorkey(COLOR_KEY)
        for sheet in self.npc_sheets:
            sheet.set_colorkey(COLOR_KEY)

        self.tile_sheet = self.tile_sheet.convert()

        for i in xrange(len(self.npc_sheets)):
            self.npc_sheets[i] = self.npc_sheets[i].convert()

        self.camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) # tile index, not pixel

    def update(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            return OPTIONS_MENU_STATE
        elif event.type == pygame.KEYDOWN and event.key == self.keybindings[KB_INVENTORY]:
            return INVENTORY_STATE
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.removeitem()
        self.user.update(pygame.key.get_pressed(), self.keybindings)
        return IN_GAME_STATE

    def load(self, character, inventory, ship_layout, npcs):
        self.user = character
        self.inventory = inventory
        self.ship = ship_layout
        self.npc_sheets = npcs

    def save(self):
        return self.user, self.inventory, self.ship, self.npc_sheets

    # modify items on floor
    # add single item to character location
    def additem(self, item):
        self.ship.additem((self.user.getx(), self.user.gety() + 1), item)

    # remove single item to character location
    def removeitem(self):
        item = self.ship.removeitem((self.user.getx(), self.user.gety() + 1))
        print item
        self.inventory.additem(item)

    # set all floor items
    def setitemsonfloor(self, itemsonfloor):
        self.items = itemsonfloor

    def removeitemsonfloor(self):
        self.items = []

    # get copy of items on floor
    def getitemsonfloor(self):
        return self.items

    def getinventory(self):
        return self.inventory

    def display(self):
        # reposition camera to center around character
        # limit camera to edge of map so character will be
        # not center for those cases
        self.camera.x = self.user.getx() - TILE_SHOW_W / 2
        if self.camera.x < 0:
            self.camera.x = 0
        if (self.camera.x + TILE_SHOW_W) > MAP_WIDTH:
            self.camera.x = MAP_WIDTH - TILE_SHOW_W
        self.camera.y = self.user.gety() - TILE_SHOW_H / 2 + 1
        if self.camera.y < 0:
            self.camera.y = 0
        if (self.camera.y + TILE_SHOW_H + 1) > MAP_HEIGHT:
            self.camera.y = MAP_HEIGHT - TILE_SHOW_H - 1
        self.ship.display(self.screen, self.camera)
        self.user.display(self.screen, self.camera)

#-------------------------------------------------------------------------------
#---[ OptionsMenuState Class ]--------------------------------------------------
#-------------------------------------------------------------------------------
## This class handles the functionality for the options menu (allowing
## "resume game," "save game," "load game," "modify settings" and "exit" options)
#
class OptionsMenuState (GameState):
    def __init__(self, screen, save_exists):
        self.save_exists = save_exists
        self.menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                            [('Resume Game', IN_GAME_STATE, None, True),
                            ('Save Game', SAVE_STATE, None, True),
                             ('Load Game', LOAD_STATE, None, save_exists),
                             ('Modify Settings', SETTINGS_STATE, None, True),
                             ('Quit', EXIT_STATE, None, True)])
        self.menu.set_center(True, True)
        self.menu.set_alignment('center', 'center')

    def update(self, event):
        state = OPTIONS_MENU_STATE
        if event.type == pygame.KEYDOWN or event.type == EVENT_CHANGE_STATE:
            rectList, state = self.menu.update(event, OPTIONS_MENU_STATE)
        return state

    def display(self):
        self.menu.draw_buttons()

