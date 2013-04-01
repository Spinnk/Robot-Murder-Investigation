# game.py
# Handles game information

import sys, pygame
from pygame.locals import *

from consts import *
from menu import *
from character import *
from npc import *
from shiplayout import *
from GameState import *
from inventory import *



class Game:
    def __init__(self, screen, keybindings):
        self.main_menu_state = MainMenuState( screen, False )
        self.options_menu_state = OptionsMenuState( screen, False )
        self.in_game_state = InGameState(screen, keybindings)
        self.imj_state = IMJState(screen, keybindings)

        self.current_state = self.main_menu_state
        self.current_state_id = MAIN_MENU_STATE

        self.save_exists = False
        self.keybindings = keybindings

    # Set the currentState to match the currentStateID
    def setstate(self):
        if self.current_state_id == MAIN_MENU_STATE:
            self.current_state = self.main_menu_state
        elif self.current_state_id == IN_GAME_STATE:
            self.current_state = self.in_game_state
        elif self.current_state_id == LOAD_STATE:
            pass
        elif self.current_state_id == SAVE_STATE:
            pass
        elif self.current_state_id == EXIT_STATE:
            pygame.event.post(pygame.event.Event(pygame.QUIT, key = 0))
        elif self.current_state_id == SETTINGS_STATE:
            pass
        elif self.current_state_id == INVENTORY_STATE:
            self.current_state = self.imj_state
            pass
        elif self.current_state_id == PUZZLE_STATE:
            pass
        elif self.current_state_id == OPTIONS_MENU_STATE:
            self.current_state = self.options_menu_state


    def update(self, event):
        newStateID = self.current_state.update(event)
        if newStateID != self.current_state_id:
            if newStateID == LOAD_STATE and not self.save_exists:
                return NO_SAVED_GAMES
            self.current_state_id = newStateID
            self.setstate()

    def display(self, screen, state):
        self.current_state.display()
