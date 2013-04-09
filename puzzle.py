
import copy
import sys
import string
import os

from consts import *
from keybinding import *

import pygame

class CircuitPuzzle:
    def __init__(self):
	self.x = 0
	self.y = 0
	self.selected = 0
	self.item = []
	self.item_table = []
	
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
		
	# load puzzle cursor
	self.cursor = pygame.image.load(PUZZLE_SELECTED_DIR)
	if self.cursor == 0:
		sys.exit(IMAGE_DOES_NOT_EXIST)
	self.cursor.set_colorkey(COLOR_KEY)
	self.cursor = self.cursor.convert()
		
    def load(self, f_path):
	item_w, item_h = self.puzzle_item.get_size()
	for item_x in range(0, item_w/TILE_WIDTH):
	    temp = []
            self.item_table.append(temp)
            for item_y in range(0, item_h/TILE_HEIGHT):
            	rect = (item_x * TILE_WIDTH, item_y * TILE_HEIGHT, TILE_WIDTH,TILE_HEIGHT)
		temp.append(self.puzzle_item.subsurface(rect))

        # open the file
	fd = open(f_path, "r")
	file_t = fd.read()
	
	for line_t in file_t:
            temp1 = []
            self.item.append(temp1)
            digits = string.split(line_t)
            for x in digits:
                num = string.atoi(x)
                temp1.append(num)

	fd.close()
	
    def update(self, keybinding):
	return PUZZLE_FAIL

    def display(self, screen):
        if screen == 0:
            return SURFACE_DOES_NOT_EXIST
        screen.blit(self.background, (0, 0))

        # print puzzle items to screen
        for x, row in enumerate(self.item_table):
            for y, item in enumerate(row):
                screen.blit(item, (x*TILE_WIDTH, y*TILE_HEIGHT))
    
        screen.blit(self.cursor, (0,0))

        return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    if screen == 0:
        sys.exit(SCREEN_DOES_NOT_EXIST)

    pygame.display.set_caption("Puzzle Demo")
    pygame.key.set_repeat(100, 100)

    test = CircuitPuzzle()
    test.load(PUZZLE_MAP)
    
    quit = False
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True
        test.display(screen)
        pygame.display.flip()

    pygame.quit()
