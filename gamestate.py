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
    def __init__(self, state_id):
        # self.state_id is the int id associated with the GameState subclass
        self.state_id = state_id

    ## ---[ update ]------------------------------------------------------------
    #  @param   self    The class itself, Python standard
    #  @param   event   A pygame event
    #
    # Updates the GameState, returns the (new) game state
    def update(self, event):
        pass
    
    ## ---[ display ]----------------------------------------------------------
    #  
    # Prints the game state's current image to the screen
    def display(self):
        pass

    ## ---[ checkstatechanges ]--------------------------------------------------
    #  @param   self    The class itself, Python standard
    #  @param   event   A pygame event
    #
    # Checks if the event indicates that the state should change and returns the
    # state associated with the given event
    def checkstatechange(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.keybindings[KB_INVENTORY]:
            if self.state_id == IMJ_STATE:
                return IN_GAME_STATE
            else:
                return IMJ_STATE
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.state_id == OPTIONS_MENU_STATE:
                return IN_GAME_STATE
            else:
                return OPTIONS_MENU_STATE


#-------------------------------------------------------------------------------
#---[ LoadGameState Class ]-----------------------------------------------------
#-------------------------------------------------------------------------------
## This class handles loading a game from a save file
#
class LoadGameState (GameState):

    def __init__(self, screen, state_id):
        self.state_id = state_id
        self.num_saves = 0
        load_state = 201                        # The first load_state
        self.screen = screen                    # A copy of the screen

        # self.menu provides the interface for loading a game
        self.menu = cMenu( 50, 50, 20, 5, 'vertical', 15, self.screen,
                           [('Resume Game', IN_GAME_STATE, None, True),
                            ('', IN_GAME_STATE, None, False)])
        self.menu.set_center(True, True)
        self.menu.set_alignment('center', 'center')

        # Iterate through the save directory and add a menu button for each
        #  saved game
        d = os.listdir( SAVE_DIR )
        for f in d:
            self.menu.add_buttons( [(f[:-5], load_state, None, True)])
            load_state += 1
            self.num_saves += 1
            
    ## ---[ update ]------------------------------------------------------------
    def update(self, event):
        state = self.state_id
        if event.type == pygame.KEYDOWN or event.type == EVENT_CHANGE_STATE:
            rectList, state = self.menu.update(event, self.state_id)
        return state

    ## ---[ display ]----------------------------------------------------------
    def display(self):
        #self.setmenu()
        self.menu.draw_buttons()

    ## ---[ updatemenu ]-------------------------------------------------------
    #
    # This updates the load menu to reflect any changes in the save directory
    def updatemenu(self, new_num_saves):
        # Return if the number of saves has not changed
        if self.num_saves == new_num_saves:
            return

        # remove all "saved game" buttons
        self.menu.remove_end( self.num_saves )
        
        load_state = 201                # The first save_state
        
        # Iterate through the save directory and add a menu button for each
        #  saved game
        d = os.listdir( SAVE_DIR )
        for f in d:
            self.menu.add_buttons( [(f[:-5], load_state, None, True)])
            load_state += 1

        self.num_saves = new_num_saves
        

    ## ---[ load ]------------------------------------------------------------
    #  @param   self            The class itself, Python standard
    #  @param   save_location   A string representing the save location
    #
    # loads the game from a given save location
    def load(self, save_location):
        print "Attempting to load from " + save_location
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



#-------------------------------------------------------------------------------
#---[ SaveGameState Class ]-----------------------------------------------------
#-------------------------------------------------------------------------------
## This class handles save
#
class SaveGameState (GameState):

    def __init__(self, screen, state_id):
        if not os.path.isdir(SAVE_DIR):
            os.mkdir(SAVE_DIR)
        self.save_location = os.path.join(SAVE_DIR, "Save 1")
        self.state_id = state_id
        self.num_saves = 0
        os.listdir( SAVE_DIR )
        save_state = 100
        self.menu = cMenu( 50, 50, 20, 5, 'vertical', 15, screen,
                           [('Resume Game', IN_GAME_STATE, None, True),
                            ('', IN_GAME_STATE, None, False),
                            ('New Save', save_state, None, True)])
        d = os.listdir( SAVE_DIR )
        save_state += 1
        for f in d:
            self.menu.add_buttons( [(f[:-5], save_state, None, True)])
            save_state += 1
            self.num_saves += 1
        self.menu.set_center(True, True)
        self.menu.set_alignment('center', 'center')

    def update(self, event):
        state = self.state_id
        if event.type == pygame.KEYDOWN or event.type == EVENT_CHANGE_STATE:
            rectList, state = self.menu.update(event, self.state_id)
        if state >= 100:
            if self.num_saves >= 9:
                self.menu.set_selectable('New Save', False)
            if state == 100:
                save_name = "Save " + str(self.num_saves + 1)
                self.menu.add_buttons([( save_name, 100 + self.num_saves + 1, None, True)])
                self.num_saves += 1
                self.save_location = os.path.join(SAVE_DIR, save_name + ".rmis")
                print "Saved Game as " + save_name
        return state

    ## ---[ display ]----------------------------------------------------------
    def display(self):
        self.menu.draw_buttons()

    def save(self, character, inventory, ship, npcs):
        c = character.save()
        i = inventory.save()
        s = ship.save()
        ns = [npc.save() for npc in npcs]
        out = binascii.unhexlify(makehex(len(c), 4)) + c + binascii.unhexlify(makehex(len(i), 4)) + i + binascii.unhexlify(makehex(len(s), 4)) + s + binascii.unhexlify(makehex(len(ns), 4)) + ''.join([binascii.unhexlify(makehex(len(n), 4)) + n for n in ns])
        out += hashlib.sha512(out).digest()
        f = open(self.save_location, 'wb')
        f.write(out)
        f.close()
        return self.num_saves


#-------------------------------------------------------------------------------
#---[ IMJState Class ]----------------------------------------------------------
#-------------------------------------------------------------------------------
## This class is used to handle the Inventory/Map/Journal State
#
class IMJState (GameState):
    def __init__(self, screen, keybindings, state_id):
        self.state_id = state_id
        self.inventory = None
        self.screen = screen
        self.keybindings = keybindings
        self.ship = None

        # The possible states that this state may change to
        self.state_changes = [IMJ_STATE, OPTIONS_MENU_STATE, IN_GAME_STATE]

    def update(self, event):
        self.inventory.update(self.keybindings)
        changed_state = self.checkstatechange(event)
        if changed_state in self.state_changes:
            return changed_state
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.inventory.removeitem()
        return IMJ_STATE


    ## ---[ display ]----------------------------------------------------------
    def display(self):
        try:
            self.inventory.display(self.screen)
        except AttributeError:
            print "Error: Inventory not set."
            exit(1)
            
    ## ---[ setinventory ]-----------------------------------------------------
    #  @param   self        The class itself, Python standard
    #  @param   inventory   The current game inventory
    #
    #  Sets the inventory to match the given inventory
    def setinventory(self, inventory):
        self.inventory = inventory

    def setship(self, ship):
        self.ship = ship

    def getship(self):
        return self.ship


#-------------------------------------------------------------------------------
#---[ MainMenuState Class ]-----------------------------------------------------
#-------------------------------------------------------------------------------
## This class handles the functionality for the main menu (allowing "new game,"
## "load game" and "exit" options)
#
class MainMenuState (GameState):

    def __init__(self, screen, save_exists, state_id):
        self.state_id = state_id
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
    
    ## ---[ display ]----------------------------------------------------------
    def display(self):
        self.menu.draw_buttons()

#-------------------------------------------------------------------------------
#---[ InGameState Class ]-------------------------------------------------------
#-------------------------------------------------------------------------------
## This class handles the functionality for in-game actions and display
#
class InGameState (GameState):
    # initialize with only map
    def __init__(self, screen, keybindings, state_id):
        self.state_id = state_id

        # load images, check if they exist, and apply colorkey
        self.character_sprite_sheet = pygame.image.load(CHARACTER_SPRITE_SHEET_DIR)
        if self.character_sprite_sheet == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        # don't do set_colorkey and convert on character image due to background already being transparent

        self.tile_sheet = pygame.image.load(TILE_SHEET_DIR)
        if self.tile_sheet == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.tile_sheet.set_colorkey(COLOR_KEY)
        self.tile_sheet = self.tile_sheet.convert()

        self.npc_sheets = [pygame.image.load(npc_file) for npc_file in NPC_SHEETS_DIR]
        for sheet in self.npc_sheets:
            if sheet == None:
                sys.exit(IMAGE_DOES_NOT_EXIST)
        for sheet in self.npc_sheets:
            sheet.set_colorkey(COLOR_KEY)
        for i in xrange(len(self.npc_sheets)):
            self.npc_sheets[i] = self.npc_sheets[i].convert()

        # set system stuff
        self.screen = screen
        self.keybindings = keybindings

        # create default objects
        self.user = Character(CHARACTER_SPRITE_SHEET_DIR)
        self.inventory = Inventory(INVENTORY_BACKGROUND_SHEET_DIR, ITEM_SHEET_SMALL_DIR, ITEM_SHEET_LARGE_DIR, ITEM_BOX_DIR, INVENTORY_BUTTONS_DIR)
        self.ship = ShipLayout(TILE_SHEET_DIR, ITEM_SHEET_SMALL_DIR)
        self.ship.loadmap(MAP_DEFAULT_DIR)
        self.npcs = []

        # temporary test items
        self.ship.additem((1,1), 1)
        self.ship.additem((1,4), 2)
        self.ship.additem((3,3), 0)

        self.camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) # tile index, not pixel

        # The possible states that this state may change to
        self.state_changes = [IMJ_STATE, OPTIONS_MENU_STATE]

    def update(self, event):
        if self.checkstatechange(event) in self.state_changes:
            return self.checkstatechange(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.removeitem()
        self.user.update(self.keybindings)
        return IN_GAME_STATE

    ## ---[ display ]----------------------------------------------------------
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

    def load(self, character, inventory, ship_layout, npcs):
        self.user = character
        self.inventory = inventory
        self.ship.setitems(ship_layout.getitems())
        self.npcs = npcs

    def save(self):
        return self.user, self.inventory, self.ship, self.npcs

    # modify items on floor
    # add single item to character location
    def additem(self, item):
        self.ship.additem((self.user.getx(), self.user.gety() + 1), item)

    # remove single item from character location and add to inventory
    def removeitem(self):
        item = self.ship.removeitem((self.user.getx(), self.user.gety() + 1))
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
    
    def getship(self):
        return self.ship

    def setship(self, ship):
        self.ship = ship


#-------------------------------------------------------------------------------
#---[ OptionsMenuState Class ]--------------------------------------------------
#-------------------------------------------------------------------------------
## This class handles the functionality for the options menu (allowing
## "resume game," "save game," "load game," "modify settings" and "exit" options)
#
class OptionsMenuState (GameState):
    def __init__(self, screen, save_exists, state_id):
        self.state_id = state_id
        self.save_exists = save_exists
        self.menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                            [('Resume Game', IN_GAME_STATE, None, True),
                            ('Save Game', SAVE_STATE, None, True),
                             ('Load Game', LOAD_STATE, None, save_exists),
                             ('Modify Settings', SETTINGS_STATE, None, True),
                             ('Quit', EXIT_STATE, None, True)])
        self.menu.set_center(True, True)
        self.menu.set_alignment('center', 'center')

    def loadable(self, save_exists = True):
        self.menu.set_selectable( 'Load Game', save_exists )

    def update(self, event):
        state = OPTIONS_MENU_STATE
        if event.type == pygame.KEYDOWN or event.type == EVENT_CHANGE_STATE:
            rectList, state = self.menu.update(event, OPTIONS_MENU_STATE)
        return state

    ## ---[ display ]----------------------------------------------------------
    def display(self):
        self.menu.draw_buttons()

