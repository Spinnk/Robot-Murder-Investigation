
import copy
import sys

from consts import *
from keybinding import *

import pygame

class Puzzle:
    def __init__(self):
		self.x = 0
		self.y = 0
		self.selected = 0
		self.item = []
	
		# load background
		self.background = pygame.image.load(PUZZLE_BACKGROUND_DIR)
		if self.background == 0:
			sys.exit(IMAGE_DOES_NOT_EXIST)
		self.background.set_colorkey(COLOR_KEY)
		self.background = self.background.convert()
		
		# load puzzle tiles
		self.puzzle_item = pygame.image.load(PUZZLE_ITEM_DIR)
		if self.puzzle_item == 0:
			sys.exit(IMAGE_DOES_NOT_EXIST)
		self.puzzle_item.set_colorkey(COLOR_KEY)
		self.puzzle_item = self.puzzle_item.convert()
		
		# load puzzle selection
		self.puzzle_selected = pygame.image.load(PUZZLE_SELECTED_DIR)
		if self.puzzle_selected == 0:
			sys.exit(IMAGE_DOES_NOT_EXIST)
		self.puzzle_selected.set_colorkey(COLOR_KEY)
		self.puzzle_selected = self.puzzle_selected.convert()
	
    def update(self, keybinding):
		pass

    def display(self, screen):
        if screen == 0:
            return SURFACE_DOES_NOT_EXIST
        screen.blit(self.background, (0, 0))

        return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    if screen == 0:
        sys.exit(SCREEN_DOES_NOT_EXIST)

    pygame.display.set_caption("Puzzle Demo")
    pygame.key.set_repeat(100, 100)

    test = Puzzle()
    
    quit = False
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True
        test.display(screen)
        pygame.display.flip()

    pygame.quit()
