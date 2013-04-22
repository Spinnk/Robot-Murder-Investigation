#! /usr/bin/python

# GameState and all its inherited classes
#
# The GameState class provides the foundation for the possible game states.
# Included in this file are the MainMenuState and OptionsMenuState.
#
# These states each recieve input through an update() function and print to the
# screen using a display() function. The update() function returns an integer
# representation of the state the game should be in, given the input.
#
# gamestate.py is part of Sentience in Space.
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
from settings import *
from menu import *
from character import *
from inventory import *
from journal import *
from npc import *
from shiplayout import *

# States
MAIN_MENU_STATE = 0
IN_GAME_STATE = 1
LOAD_STATE = 2
SAVE_STATE = 3
EXIT_STATE = 4
SETTINGS_STATE = 5
# IMJ_STATE = 6 OLD FUNCTIONALITY
PUZZLE_STATE = 7
OPTIONS_MENU_STATE = 8
INVENTORY_STATE = 9
JOURNAL_STATE = 10
MAP_STATE = 11

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
        if event.type == pygame.KEYDOWN:
            # If Inventory key is pressed:
            if event.key == KEYBINDINGS[KB_INVENTORY]:
                if self.state_id == INVENTORY_STATE:
                    return IN_GAME_STATE
                return INVENTORY_STATE
            # If journal key is pressed
            elif event.key == KEYBINDINGS[KB_JOURNAL]:
                if self.state_id == JOURNAL_STATE:
                    return IN_GAME_STATE
                return JOURNAL_STATE
            # If map key is pressed
            elif event.key == KEYBINDINGS[KB_MAP]:
                if self.state_id == MAP_STATE:
                    return IN_GAME_STATE
                return MAP_STATE
            elif event.key == pygame.K_p:
                if self.state_id == PUZZLE_STATE:
                    return IN_GAME_STATE
                return PUZZLE_STATE
            # If Escape is pressed
            elif event.key == pygame.K_ESCAPE:
                if self.state_id == OPTIONS_MENU_STATE:
                    return IN_GAME_STATE
                return OPTIONS_MENU_STATE


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

        # Menu to display "New Game, "Load Game," and "Quit" options
        self.menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                            [('New Game', IN_GAME_STATE, None, True),
                             ('Load Game', LOAD_STATE, None, self.save_exists),
                             ('Modify Settings', SETTINGS_STATE, None, True),
                             ('Quit', EXIT_STATE, None, True)])
        self.menu.set_center(True, True)
        self.menu.set_alignment('center', 'center')

    ## ---[ update ]------------------------------------------------------------
    def update(self, event):
        state = MAIN_MENU_STATE
        if event.type == pygame.KEYDOWN or event.type == EVENT_CHANGE_STATE:
            rectList, state = self.menu.update(event, MAIN_MENU_STATE)
        return state

    ## ---[ display ]----------------------------------------------------------
    def display(self):
        self.menu.draw_buttons()


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

    ## ---[ loadable ]----------------------------------------------------------
    # Changes whether the "Load" option is available
    def loadable(self, save_exists = True):
        self.menu.set_selectable( 'Load Game', save_exists )

    ## ---[ update ]------------------------------------------------------------
    def update(self, event):
        state = OPTIONS_MENU_STATE
        if event.type == pygame.KEYDOWN or event.type == EVENT_CHANGE_STATE:
            rectList, state = self.menu.update(event, OPTIONS_MENU_STATE)

        if self.checkstatechange(event) == IN_GAME_STATE:
            return IN_GAME_STATE

        return state

    ## ---[ display ]----------------------------------------------------------
    def display(self):
        self.menu.draw_buttons()
        
#-------------------------------------------------------------------------------
#---[ SettingsState Class ]-----------------------------------------------------
#-------------------------------------------------------------------------------
## This class handles the functionality changing game settings

class SettingsState (GameState):

    def __init__(self, screen, state_id):
        self.screen = screen
        self.state_id = state_id
        self.settings = Settings()
        self.state_changes = [OPTIONS_MENU_STATE]
        

    ## ---[ update ]------------------------------------------------------------
    def update(self, event):
        changed_state = self.checkstatechange(event)
        if changed_state in self.state_changes:
            return changed_state
        
        if event.type == pygame.KEYDOWN:
            self.settings.update(event)
            
        return self.state_id

    ## ---[ display ]----------------------------------------------------------
    def display(self):
        self.settings.display(self.screen)






