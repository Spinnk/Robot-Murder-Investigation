# game.py
# Handles game information

import sys, pygame

from consts import *
from menu import *

class MainMenu:

    def __init__(self, screen):
        self.__menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                            [('New Game', 1, None),
                             ('Load Game', 2, None),
                             ('Exit', 3, None)])
        
        self.__menu.set_center(True, True)
        self.__menu.set_alignment('center', 'center')
 
    def update(self, event):
        self.__menu.update(event, 0)


    def display(self, event, screen):
        self.__menu.draw_buttons()



class Game:
        def __init__(self, screen):
            self.__mainMenu = MainMenu( screen )
            self.__mainMenu.update( pygame.event.Event(EVENT_CHANGE_STATE, key = 0) )
            
        def update(self, event):
            if (event.type == pygame.KEYDOWN or event.type == EVENT_CHANGE_STATE):
                self.__mainMenu.update(event)

                
        def display(self, screen):
            self.__mainMenu.display(pygame.event.Event(EVENT_CHANGE_STATE, key = 0), screen) 
            
