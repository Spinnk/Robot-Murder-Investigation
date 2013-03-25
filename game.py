# game.py
# Handles game information

import sys, pygame

from consts import *
from menu import *

class MainMenu:

    def __init__(self, screen):
        self.menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                            [('New Game', 1, None),
                             ('Load Game', 2, None),
                             ('Exit', 3, None)])

        self.menu.set_center(True, True)
        self.menu.set_alignment('center', 'center')

    def update(self, event):
        rectList, state = self.menu.update(event, 0)
        return state

    def display(self):
        self.menu.draw_buttons()



class OptionsMenu:
    def __init__(self, screen):
        self.menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                            [('Save Game', 4, None),
                             ('Load Game', 2, None),
                             ('Modify Settings', 6, None),
                             ('Resume Game', 1, None),
                             ('Quit', 3, None)])
        self.menu.set_center(True, True)
        self.menu.set_alignment('center', 'center')

    def update(self, event):
        state = 8
        if(pygame.key.get_pressed()[pygame.K_ESCAPE]):
            rectList, state = self.menu.update(pygame.event.Event(EVENT_CHANGE_STATE, key = 0), 8)
        else:
            rectList, state = self.menu.update(event, 8)
        return state

    def display(self):
        self.menu.draw_buttons()
    

class Game:
        def __init__(self, screen):
            self.mainMenu = MainMenu( screen )
            self.mainMenu.update( pygame.event.Event(EVENT_CHANGE_STATE, key = 0) )
            self.optionsMenu = OptionsMenu( screen )

        def update(self, event, state):
            if state == 0:
                if event.type == pygame.KEYDOWN or event.type == EVENT_CHANGE_STATE:
                    return self.mainMenu.update(event)
            if state == 1:
                if (event.type == pygame.KEYDOWN) and pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    return self.optionsMenu.update(event)
            if state == 8:
                return self.optionsMenu.update(event)
   
            return state

        def display(self, screen, state):
            if state == 0:
                self.mainMenu.display()
            if state == 8:
                self.optionsMenu.display()
                
















