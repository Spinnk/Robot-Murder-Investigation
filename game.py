# game.py
# Handles game information

import sys, pygame

from consts import *
from menu import *

class Game:
    def __init__(self, screen):
        self.mainMenu = MainMenu( screen )
        self.optionsMenu = OptionsMenu( screen )

    def update(self, event, state):
        if event.type == pygame.KEYDOWN or event.type == EVENT_CHANGE_STATE:
            if state == 0:
                return self.mainMenu.update(event)
            elif state == 1:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    state = OPTIONS_MENU_STATE
                    self.optionsMenu.update(event)
            elif state == 8:
                return self.optionsMenu.update(event)
        return state

    def display(self, screen, state):
        if state == MAIN_MENU_STATE:
            self.mainMenu.display()
        if state == OPTIONS_MENU_STATE:
            self.optionsMenu.display()
                

class MainMenu:

    def __init__(self, screen):
        self.menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                            [('New Game', IN_GAME_STATE, None),
                             ('Load Game', LOAD_MENU_STATE, None),
                             ('Quit', EXIT_STATE, None)])

        self.menu.set_center(True, True)
        self.menu.set_alignment('center', 'center')
        
    def update(self, event):
        rectList, state = self.menu.update(event, MAIN_MENU_STATE)
        return state

    def display(self):
        self.menu.draw_buttons()



class OptionsMenu:
    def __init__(self, screen):
        self.menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                            [('Save Game', SAVE_MENU_STATE, None),
                             ('Load Game', LOAD_MENU_STATE, None),
                             ('Modify Settings', SETTINGS_STATE, None),
                             ('Resume Game', IN_GAME_STATE, None),
                             ('Quit', EXIT_STATE, None)])
        self.menu.set_center(True, True)
        self.menu.set_alignment('center', 'center')

    def update(self, event):
        state = OPTIONS_MENU_STATE
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            rectList, state = self.menu.update(pygame.event.Event(EVENT_CHANGE_STATE, key = 0), OPTIONS_MENU_STATE)
        else:
            rectList, state = self.menu.update(event, OPTIONS_MENU_STATE)
        return state

    def display(self):
        self.menu.draw_buttons()
    















