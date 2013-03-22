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
        self.mainState = 0
 
    def update(self, event):
        rectList, self.mainState = self.menu.update(event, 0)
        return self.mainState
            



    def display(self):
        self.menu.draw_buttons()



class Game:
        def __init__(self, screen):
            self.mainMenu = MainMenu( screen )
            self.mainMenu.update( pygame.event.Event(EVENT_CHANGE_STATE, key = 0) )
            
        def update(self, event):
            if event.type == pygame.KEYDOWN or event.type == EVENT_CHANGE_STATE:
                return self.mainMenu.update(event)
            else:
                return 0

                
        def display(self, screen):
            self.mainMenu.display() 
            
