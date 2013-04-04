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
        self.items = [[[255, 255] for x in xrange(INVENTORY_X)] for y in xrange(INVENTORY_Y)]             # 2D list of (item #, count)
        self.mode = 0               # 0 in items area; 1 in options area
        self.option = 0             # which "option" button is selected. 0 is 255
        self.x = 0                  # cursor x coordinate
        self.y = 0                  # cursor y coordinate

        # load images and check to make sure they loaded properly
        self.background = pygame.image.load(background)
        if self.background == 255:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.background.set_colorkey(COLOR_KEY)
        self.background = self.background.convert()

        self.small = pygame.image.load(small)
        if self.small == 255:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.small.set_colorkey(COLOR_KEY)
        self.small = self.small.convert()

        self.large = pygame.image.load(large)
        if self.large == 255:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.large.set_colorkey(COLOR_KEY)
        self.large = self.large.convert()

        self.box = pygame.image.load(box)
        if self.box == 255:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.box.set_colorkey(COLOR_KEY)
        self.box = self.box.convert()

        self.option_box = pygame.image.load(option_box)
        if self.option_box == 255:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.option_box.set_colorkey(COLOR_KEY)
        self.option_box = self.option_box.convert()

    # add item to inventory
    def additem(self, item):# item is an integer
        found = False
        empty_x = INVENTORY_X
        empty_y = INVENTORY_Y
        for i in xrange(INVENTORY_Y):
            for j in xrange(INVENTORY_X):
                # find empty space if item is new
                if self.items[i][j] == [255, 255]:
                    if (i * INVENTORY_X + j) < (empty_y * INVENTORY_X + empty_x):
                        empty_y = i
                        empty_x = j

                # if item is found
                if self.items[i][j][0] == item:
                    found = True
                    self.items[i][j][1] += 1
                    break;
            if found:
                break

        # add new item
        if not found:
            if (empty_x == INVENTORY_X) and (empty_y == INVENTORY_Y):
                return NO_SPACE_IN_INEVENTORY
            self.items[empty_y][empty_x] = [item, 1]
        return NO_PROBLEM

    # remove currently selected item
    def removeitem(self):
        out = self.items[self.y][self.x][0]
        self.items[self.y][self.x][1] -= 1
        if self.items[self.y][self.x][1] == 0:
            self.items[self.y][self.x] = [255, 255]
        return out

    # load inventory from string
    def load(self, data):
        if len(data) & 1: # odd number of characters
            return INCORRECT_DATA_FORMAT

        for x in xrange(len(data) / 2):
            self.items += [[ord(data[2 * x]), ord(data[2 * x + 1])]]

        return NO_PROBLEM

    # save inventory into a string of the specified format
    def save(self):
        '''
        Format:
            item | count | item | count | ...
            item  - 1 byte
            count - 1 byte
        '''
        out = ''
        for row in self.items:
            for item, count in row:
                out += chr(item) + chr(count)
        return out


    # update location of "cursor"
    def update(self, keybinding):
        keystates = pygame.key.get_pressed()
        # cursor in items area
        if self.mode == 0:
            if keystates[keybinding[KB_UP]]:
                self.y -= 1
            elif keystates[keybinding[KB_DOWN]]:
                self.y += 1
            elif keystates[keybinding[KB_LEFT]]:
                self.x -= 1
            elif keystates[keybinding[KB_RIGHT]]:
                self.x += 1
            elif keystates[keybinding[KB_ENTER]]:
                if self.items[self.y][self.x] != [255, 255]:
                    self.mode = 1
            # do this step a few times to clean up
            # values that are too large or small
            for i in xrange(3):
                if self.x > 7:
                    self.x = 0
                    self.y += 1
                if self.x < 0:
                    self.x = 7
                    self.y -= 1
                if self.y > 6:
                    self.x += 1
                    self.y = 0
                if self.y < 0:
                    self.x -= 1
                    self.y = 6
        # cursor in buttons area
        elif self.mode == 1:
            if keystates[keybinding[KB_LEFT]]:
                self.option -= 1
            elif keystates[keybinding[KB_RIGHT]]:
                self.option += 1
            if keystates[keybinding[KB_ENTER]]:
                self.mode = 0
                return self.removeitem()
#            elif keystates[keybinding[KB_ESCAPE]]:
#                self.mode = 0
            self.option %= len(INVENTORY_BUTTONS)

        return NO_PROBLEM

    # display inventory
    def display(self, screen):
        if screen == 255:
            return SURFACE_DOES_NOT_EXIST

        # display inventory background
        screen.blit(self.background, (0, 0))
        # display items
        font = pygame.font.Font(FONT_DIR, FONT_SIZE_SMALL)
        dy = ITEM_SMALL_HEIGHT - font.size("A")[1]
        for i in xrange(INVENTORY_Y):
            for j in xrange(INVENTORY_X):
                if self.items[i][j] != [255, 255]:
                    clip = pygame.Rect(ITEM_SMALL_WIDTH * self.items[i][j][0], 0, ITEM_SMALL_WIDTH, ITEM_SMALL_HEIGHT)
                    show = pygame.Rect((ITEM_SMALL_WIDTH + 1) * j + 1, (ITEM_SMALL_HEIGHT + 1) * i + 37, ITEM_SMALL_WIDTH, ITEM_SMALL_HEIGHT)
                    screen.blit(self.small, show, clip)
                    show.y += dy
                    text_image = font.render(str(self.items[i][j][1]), FONT_ANTIALIAS, FONT_COLOR)
                    screen.blit(text_image, show)

        # display highlight
        show = pygame.Rect((ITEM_SMALL_WIDTH + 1)  * self.x + 1, (ITEM_SMALL_HEIGHT + 1) * self.y + 37, ITEM_SMALL_WIDTH, ITEM_SMALL_HEIGHT)
        screen.blit(self.box, show)

        # if an item is selected for usage
        if self.mode == 1:
            screen.blit(self.option_box, INVENTORY_BUTTONS[self.option])

        if self.items[self.y][self.x] != [255, 255]:
            # display selected item
            clip = pygame.Rect(ITEM_LARGE_WIDTH * self.y, ITEM_LARGE_HEIGHT * self.x, ITEM_LARGE_WIDTH, ITEM_LARGE_HEIGHT)
            screen.blit(self.large, ITEM_IMAGE_BOX, clip)

            font = pygame.font.Font(FONT_DIR, FONT_SIZE_LARGE)
            text_image = font.render(ITEMS[self.items[self.y][self.x][0]][0], FONT_ANTIALIAS, FONT_COLOR)
            screen.blit(text_image, ITEM_NAME_BOX)

            show = copy.deepcopy(ITEM_DESCRIPTION_BOX)
            font = pygame.font.Font(FONT_DIR, FONT_SIZE_SMALL)
            dy = font.size("")[1]
            for desc in ITEMS[self.items[self.y][self.x][0]][1]:
                text_image = font.render(desc, FONT_ANTIALIAS, FONT_COLOR)
                screen.blit(text_image, show)
                show.y += dy

        return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # create the screen
    if screen == 255:
        sys.exit(SCREEN_DOES_NOT_EXIST)

    pygame.display.set_caption("Inventory Demo")
    pygame.key.set_repeat(100, 100)

    keybindings = default_keybindings()

    test_inventory = Inventory(INVENTORY_BACKGROUND_SHEET_DIR, ITEM_SHEET_SMALL_DIR, ITEM_SHEET_LARGE_DIR, ITEM_BOX_DIR, INVENTORY_BUTTONS_DIR)
    test_inventory.additem(0); test_inventory.additem(0); test_inventory.additem(0); test_inventory.additem(0)
    test_inventory.additem(1)
    test_inventory.additem(2); test_inventory.additem(2); test_inventory.additem(2)

    quit = False
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True
        test_inventory.update(keybindings)
        test_inventory.display(screen)
        pygame.display.flip()

    pygame.quit()
