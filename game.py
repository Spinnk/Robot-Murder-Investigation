# game.py
# Handles game information

import sys, pygame
from pygame.locals import *

from consts import *
from menu import *
from character import *
from inventory import *
from npc import *
from shiplayout import *
from GameState import *

class Game:
    def __init__(self, screen, keybindings):
        self.mainMenuState = MainMenuState( screen )
        self.optionsMenuState = OptionsMenuState( screen )
        self.inGameState = InGameState(screen, keybindings)
#        self.inventory = Inventory(INVENTORY_BACKGROUND_SHEET_DIR, ITEM_SHEET_SMALL_DIR, ITEM_SHEET_LARGE_DIR, ITEM_BOX_DIR, INVENTORY_BUTTONS_DIR)

        self.currentState = self.mainMenuState
        self.currentStateID = MAIN_MENU_STATE

        self.saveExists = False
        self.keybindings = keybindings

	
    # Set the currentState to match the currentStateID
    def setState(self):
        if self.currentStateID == MAIN_MENU_STATE:
            self.currentState = self.mainMenuState
        elif self.currentStateID == IN_GAME_STATE:
            self.currentState = self.inGameState
        elif self.currentStateID == LOAD_STATE:
            pass
        elif self.currentStateID == SAVE_STATE:
            pass
        elif self.currentStateID == EXIT_STATE:
            pygame.event.post(pygame.event.Event(pygame.QUIT, key = 0))
        elif self.currentStateID == SETTINGS_STATE:
            pass
        elif self.currentStateID == INVENTORY_STATE:
            self.inventory.display(screen)
        elif self.currentStateID == PUZZLE_STATE:
            pass
        elif self.currentStateID == OPTIONS_MENU_STATE:
            self.currentState = self.optionsMenuState
        

    def update(self, event):
        newStateID = self.currentState.update(event)
        if newStateID != self.currentStateID:
            if newStateID == LOAD_STATE and not self.saveExists:
                pass
            self.currentStateID = newStateID
            self.setState()

    def display(self, screen, state):
        self.currentState.display()

        
class SaveGame:
    def __init__(self):
        pass
        

















