#! /usr/bin/python

# Inventory Class

# should change storage to array 8 * 7
# should add timer or check for only keydown events

# inventory.py is part of Sentience in Space.
#
# Sentience in Space is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sentience in Space is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sentience in Space.  If not, see <http://www.gnu.org/licenses/>.

import copy

from consts import *
from keybinding import *

import pygame

class Inventory:
    def __init__(self, background, small, large, box, option_box):
        self.items = []             # list of (item #, count)
        self.mode = 0               # 0 in items area; 1 in options area
        self.selected = 0           # which items is selected
        self.option = 0             # which "option" button is selected. 0 is none

        # load images and check to make sure they loaded properly
        self.background = pygame.image.load(background)
        if self.background == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.background.set_colorkey(COLOR_KEY)
        self.background = self.background.convert()

        self.small = pygame.image.load(small)
        if self.small == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.small.set_colorkey(COLOR_KEY)
        self.small = self.small.convert()

        self.large = pygame.image.load(large)
        if self.large == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.large.set_colorkey(COLOR_KEY)
        self.large = self.large.convert()

        self.box = pygame.image.load(box)
        if self.box == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.box.set_colorkey(COLOR_KEY)
        self.box = self.box.convert()

        self.option_box = pygame.image.load(option_box)
        if self.option_box == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.option_box.set_colorkey(COLOR_KEY)
        self.option_box = self.option_box.convert()

    # add item to inventory
    def add(self, item):# item is an integer
        found = False
        for i in xrange(len(self.items)):
            if self.items[i][0] == item:
                found = True
                self.items[i][1] += 1
                break;
        if not found:
            self.items += [[item, 1]]
        return NO_PROBLEM

    # remove item from inventory
    def remove(self, to_rem):
        for i in xrange(len(self.items)):
            if self.items[i][0] == to_rem:
                self.items[i][1] -= 1
                if self.items[i][1] == 0:
                    del self.items[i]
                return NO_PROBLEM
        return ITEM_DOES_NOT_EXIST

    # load inventory from string
    def load(self, data):
        if len(data) & 1: # odd number of characters
            return INCORRECT_DATA_FORMAT

        for x in xrange(len(data) / 2):
            self.items += [(ord(data[2 * x]), ord(data[2 * x + 1]))]

        return NO_PROBLEM

    # save inventory into a string of the specified format
    def save(self):
        '''
        Format:
            item | count | item | count | ...
            item  - 1 byte
            count - 1 byte
        '''
        return ''.join([chr(item) + chr(count) for item, count in self.items])

    # update location of "cursor"
    def update(self, keystates, keybinding):
        # cursor in items area
        if self.mode == 0:
            if keystates[keybinding[KB_UP]]:
                self.selected -= 8
            elif keystates[keybinding[KB_DOWN]]:
                self.selected += 8
            elif keystates[keybinding[KB_LEFT]]:
                self.selected -= 1
            elif keystates[keybinding[KB_RIGHT]]:
                self.selected += 1
            elif keystates[keybindings[KB_ENTER]]:
#                if not (self.items[self.selected] == None):
#                    self.mode = 1
                if self.selected < len(self.items):
                    self.mode = 1
            self.selected %= 56
        # cursor in buttons area
        elif self.mode == 1:
            if keystates[keybinding[KB_LEFT]]:
                self.option -= 1
            elif keystates[keybinding[KB_RIGHT]]:
                self.option += 1
            if keystates[keybindings[KB_ENTER]]:
                self.mode = 0
                out = self.items[self.selected][0]
                self.remove(out)
                return out
            elif keystates[keybindings[KB_ESCAPE]]:
                self.mode = 0
            self.option %= len(INVENTORY_BUTTONS)

        return NO_PROBLEM

    # display inventory
    def display(self, screen):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST

        # display inventory background
        screen.blit(self.background, (0, 0))

        # display items
        count = 0
        font = pygame.font.Font(FONT_DIR, FONT_SIZE_SMALL)
        dy = ITEM_SMALL_HEIGHT - font.size("A")[1]
        for item in self.items:
            clip = pygame.Rect(ITEM_SMALL_WIDTH * item[0], 0, ITEM_SMALL_WIDTH, ITEM_SMALL_HEIGHT)
            show = pygame.Rect((ITEM_SMALL_WIDTH + 1)  * (count % 8) + 1, (ITEM_SMALL_HEIGHT + 1) * (count / 8) + 37, ITEM_SMALL_WIDTH, ITEM_SMALL_HEIGHT)
            screen.blit(self.small, show, clip)
            show.y += dy
            text_image = font.render(str(item[1]), FONT_ANTIALIAS, FONT_COLOR)
            screen.blit(text_image, show)
            count += 1

        # display highlight
        show = pygame.Rect((ITEM_SMALL_WIDTH + 1)  * (self.selected % 8) + 1, (ITEM_SMALL_HEIGHT + 1) * (self.selected / 8) + 37, ITEM_SMALL_WIDTH, ITEM_SMALL_HEIGHT)
        screen.blit(self.box, show)

        # if an item is selected for usage
        if self.mode == 1:
            screen.blit(self.option_box, INVENTORY_BUTTONS[self.option])

        if self.selected < len(self.items):
            # display selected item
            clip = pygame.Rect(ITEM_LARGE_WIDTH * self.items[self.selected][0], ITEM_LARGE_HEIGHT * (count / 8), ITEM_LARGE_WIDTH, ITEM_LARGE_HEIGHT)
            screen.blit(self.large, ITEM_IMAGE_BOX, clip)

            font = pygame.font.Font(FONT_DIR, FONT_SIZE_LARGE)
            text_image = font.render(ITEMS[self.selected][0], FONT_ANTIALIAS, FONT_COLOR)
            screen.blit(text_image, ITEM_NAME_BOX)

            show = copy.deepcopy(ITEM_DESCRIPTION_BOX)
            font = pygame.font.Font(FONT_DIR, FONT_SIZE_SMALL)
            dy = font.size("A")[1]
            for desc in ITEMS[self.selected][1]:
                text_image = font.render(desc, FONT_ANTIALIAS, FONT_COLOR)
                screen.blit(text_image, show)
                show.y += dy

        return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # create the screen
    if screen == None:
        sys.exit(SCREEN_DOES_NOT_EXIST)

    pygame.display.set_caption("Inventory Demo")

    test_inventory = Inventory(INVENTORY_BACKGROUND_SHEET_DIR, ITEM_SHEET_SMALL_DIR, ITEM_SHEET_LARGE_DIR, ITEM_BOX_DIR, INVENTORY_BUTTONS_DIR)

    test_inventory.add(0); test_inventory.add(0); test_inventory.add(0); test_inventory.add(0)
    test_inventory.add(1)
    test_inventory.add(2); test_inventory.add(2); test_inventory.add(2)

    keybindings = default_keybindings()
    pygame.key.set_repeat(100, 100)

    quit = False
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True
        test_inventory.update(pygame.key.get_pressed(), keybindings)
        test_inventory.display(screen)
        pygame.display.flip()

    pygame.quit()
