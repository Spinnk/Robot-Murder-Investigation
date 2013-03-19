# game.py
# Overall Game class to handle game framework


import sys
import pygame

from consts import *
from character import *


class game:
    def __init__(self, screen):
        self.main_bg_image = pygame.image.load( MAIN_BG_IMAGE );

    def draw_main_menu(self, screen):
        screen.fill( WHITE )
        screen.blit( self.main_bg_image, (0,0) )

    def new_game(self):
        print "New Game!"
        
        
