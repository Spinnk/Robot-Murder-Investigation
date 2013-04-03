#! /usr/bin/python

# Game Class
#
# The Game class recieves input from the main render loop (in main.py)
# and determines which GameState (from GameState.py) should be active.
# This is done by passing the input into the current game state
# (originally this is an instance of MainMenuState) and recieving an integer
# representation of the state the game should be in, given the input.
# If the game state integer has changed, Game changes the current game state
# accordingly.

# Game.py is part of Sentience in Space.
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

import sys, pygame

from consts import *
from gamestate import *

#-------------------------------------------------------------------------------
#---[ Game Class ]--------------------------------------------------------------
#-------------------------------------------------------------------------------
## This class is used to set the GameState and call GameState functions
#
class Game:
    ## ---[ __init__ ]-----------------------------------------------------------
    #  @param   self        The class itself, Python standard
    #  @param   screen      The screen which gets drawn to when the display()
    #                       function is called
    #  @param   keybindings  A map which determines which keys correspond to
    #                        specific events (such as state changes)
    #
    #  Initialize the class
    #
    def __init__(self, screen, keybindings):
        # Bool to determine if the "load game" option should be available
        self.save_exists = True

        # Create instances of each child of GameState:
        self.main_menu_state = MainMenuState( screen, self.save_exists, MAIN_MENU_STATE )
        self.options_menu_state = OptionsMenuState( screen, self.save_exists, OPTIONS_MENU_STATE )
        self.in_game_state = InGameState(screen, keybindings, IN_GAME_STATE)
        self.imj_state = IMJState(screen, keybindings, IMJ_STATE)
        self.save_game_state = SaveGameState(screen, SAVE_STATE)
        self.load_game_state = LoadGameState(screen, LOAD_STATE)

        # Set current_state to reference main_menu_state
        self.current_state = self.main_menu_state
        # An integer representation of the current state
        self.current_state_id = MAIN_MENU_STATE

        # See description above for keybindings
        self.keybindings = keybindings

    ## ---[ setstate ]-------------------------------------------------------
    # Set the current_state to match the current_state_id
    def setstate(self):
        if self.current_state_id == MAIN_MENU_STATE:
            self.current_state = self.main_menu_state
        elif self.current_state_id == IN_GAME_STATE:
            self.current_state = self.in_game_state
        elif self.current_state_id == LOAD_STATE:
            print "Loading Game..."
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            #c, i, s, ns = self.load_game_state
            #self.in_game_state.load(c, i, s, ns)
            self.current_state = self.load_game_state
            self.current_state_id = LOAD_STATE
        elif self.current_state_id == SAVE_STATE:
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            self.save_exists = True
            c, i, s, ns = self.in_game_state.save()
            self.save_game_state.save( c, i, s, ns)
            self.current_state = self.save_game_state
        elif self.current_state_id == EXIT_STATE:
            pygame.event.post(pygame.event.Event(pygame.QUIT, key = 0))
        elif self.current_state_id == SETTINGS_STATE:
            pass
        elif self.current_state_id == IMJ_STATE:
            self.imj_state.setinventory( self.in_game_state.getinventory() )
            self.current_state = self.imj_state
            pass
        elif self.current_state_id == PUZZLE_STATE:
            pass
        elif self.current_state_id == OPTIONS_MENU_STATE:
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            self.current_state = self.options_menu_state
        elif self.current_state_id > 100:
            save_location = os.path.join(SAVE_DIR, "Save " + str(self.current_state_id - 100) + ".rmis")
            c, i, s, ns = self.load_game_state.load( save_location )
            self.in_game_state.load(c, i, s, ns)
            self.current_state = self.in_game_state
            self.current_state_id = IN_GAME_STATE



    ## ---[ update ]-------------------------------------------------------
    #  @param   self    The class itself, Python standard
    #  @param   event   A pygame event
    #
    #  Calls the update function on the current_state and setstate() if
    #   the update returns a state id different from current_state_id
    #
    def update(self, event):
        newStateID = self.current_state.update(event)
        if newStateID != self.current_state_id:
            self.current_state_id = newStateID
            self.setstate()

    ## ---[ display ]-------------------------------------------------------
    #  Calls the display function on the current_state
    #
    def display(self):
        self.current_state.display()
