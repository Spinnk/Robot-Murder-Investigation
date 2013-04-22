
import copy
import sys
import string
import os

from consts import *

import pygame

class CircuitPuzzle:
    def __init__(self):
	self.x = 0
	self.y = 0
	self.selected = False
	self.item = []
	self.rules = []
	self.item_table = []
	self.font_title = pygame.font.Font(PUZZLE_FONT_DIR, PUZZLE_FONT_TITLE_SIZE)
        self.font_rules = pygame.font.Font(PUZZLE_FONT_DIR, PUZZLE_FONT_RULES_SIZE)

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
    
    # load puzzle highlight
	self.cursor_on = pygame.image.load(PUZZLE_SELECTED_ON_DIR)
	if self.cursor_on == 0:
		sys.exit(IMAGE_DOES_NOT_EXIST)
	self.cursor_on.set_colorkey(COLOR_KEY)
	self.cursor_on = self.cursor_on.convert()

	# load puzzle items
	item_w, item_h = self.puzzle_item.get_size()
	for item_x in range(0, item_w/TILE_WIDTH):
	    rect = (item_x * TILE_WIDTH, 0, TILE_WIDTH,TILE_HEIGHT)
	    self.item_table.append(self.puzzle_item.subsurface(rect))

        # load puzzle map
	fd = open(PUZZLE_MAP, "r")
	for line_t in fd.readlines():
            temp1 = []
            self.item.append(temp1)
            digits = string.split(line_t)
            for x in digits:
                num = int(x)
                temp1.append(num)
        fd.close()

        # load puzzle rules
        fd = open(PUZZLE_RULES, "r")
	for line_t in fd.readlines():
            self.rules.append(line_t.rstrip())
        fd.close()

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == KEYBINDINGS[KB_LIFT] and self.item[self.x][self.y] == 3:
                if self.selected:
                    self.selected = False
                else:
                    self.selected = True
            elif event.key == KEYBINDINGS[KB_LEFT]:
                self.x -= 1
                if (self.x < 0):
                    self.x = 0
                elif self.selected:
                    if (self.item[self.x][self.y] == 2 or self.item[self.x][self.y] == 3):
                        self.x +=1
                    else:
                        swap = self.item[self.x+1][self.y]
                        self.item[self.x+1][self.y] = self.item[self.x][self.y]
                        self.item[self.x][self.y] = swap
            elif event.key == KEYBINDINGS[KB_DOWN]:
                self.y += 1
                if(self.y > 7):
                    self.y = 7
                elif self.selected:
                    if (self.item[self.x][self.y] == 2 or self.item[self.x][self.y] == 3):
                        self.y -= 1
                    else:
                        swap = self.item[self.x][self.y-1]
                        self.item[self.x][self.y-1] = self.item[self.x][self.y]
                        self.item[self.x][self.y] = swap
            elif event.key == KEYBINDINGS[KB_RIGHT]:
                self.x += 1
                if(self.x > 7):
                    self.x = 7
                elif self.selected:
                    if (self.item[self.x][self.y] == 2 or self.item[self.x][self.y] == 3):
                        self.x -= 1
                    else:
                        swap = self.item[self.x-1][self.y]
                        self.item[self.x-1][self.y] = self.item[self.x][self.y]
                        self.item[self.x][self.y] = swap
            elif event.key == KEYBINDINGS[KB_UP]:
                self.y -= 1
                if(self.y < 0):
                    self.y = 0
                elif self.selected:
                    if (self.item[self.x][self.y] == 2 or self.item[self.x][self.y] == 3):
                        self.y += 1
                    else:
                        swap = self.item[self.x][self.y+1]
                        self.item[self.x][self.y+1] = self.item[self.x][self.y]
                        self.item[self.x][self.y] = swap

        for row in self.item:
            if sum(row) == 24:
                return PUZZLE_SUCCESS

	return PUZZLE_WORKING

    def display(self, screen):
        if screen == 0:
            return SURFACE_DOES_NOT_EXIST
        screen.blit(self.background, (0, 0))

        # print puzzle items to screen
        for x in xrange(len(self.item)):
            for y in xrange(len(self.item[x])):
                screen.blit(self.item_table[self.item[x][y]], (x*TILE_WIDTH, y*TILE_HEIGHT))
        
        #display cursor
        if self.selected:        
            screen.blit(self.cursor_on, (self.x*TILE_WIDTH, self.y*TILE_HEIGHT))
        else:
            screen.blit(self.cursor, (self.x*TILE_WIDTH, self.y*TILE_HEIGHT))

        #print title and rules
        for x in xrange(len(self.rules)):
            box = pygame.Rect(TILE_WIDTH*len(self.item)+10, x*25, 0, 0)
            if x == 0:
                self.font_title.set_underline(1)
                show = self.font_title.render(self.rules[x], PUZZLE_FONT_ANTIALIAS, PUZZLE_FONT_COLOR)
            else:
                show = self.font_rules.render(self.rules[x], PUZZLE_FONT_ANTIALIAS, PUZZLE_FONT_COLOR)
            screen.blit(show, box)
            
        bridge_t = pygame.Rect(TILE_WIDTH*len(self.item)+10, 25* len(self.rules), 0, 0)
        screen.blit(self.item_table[3], bridge_t)

        return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    if screen == 0:
        sys.exit(SCREEN_DOES_NOT_EXIST)

    pygame.display.set_caption("Puzzle Demo")
    pygame.key.set_repeat(100, 100)

    test = CircuitPuzzle()

    quit = False
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True
            if test.update(event) == PUZZLE_SUCCESS:
                print "WIN!!!!!!!!!"
        test.display(screen)
        pygame.display.flip()

    pygame.quit()
