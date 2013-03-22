# game.py
# Handles game information

import sys, pygame

from consts import *
from menu import *

class main_menu:

    def __init__(self, screen):
        self.__menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                            [('New Game', 1, None),
                             ('Load Game', 2, None),
                             ('Exit', 3, None)])
        
        self.__menu.set_center(True, True)
        self.__menu.set_alignment('center', 'center')


    def display(self, event, screen):
        rect_list, state = self.__menu.update(event, 0)
        pygame.display.update(rect_list)


class game:

        def __init__(self, screen):
            self.__main_menu = main_menu( screen )

        def display(self, screen):
            self.__main_menu.display(pygame.event.Event(EVENT_CHANGE_STATE, key = 0), screen) 
