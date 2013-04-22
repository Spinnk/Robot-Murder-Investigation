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
import sys

from consts import *

import pygame

class Inventory:
    def __init__(self):
        self.items = [[0, 0, 0] for x in xrange(INVENTORY_SPACES)]
        self.index = 0              # which item cursor is on
        self.mode = 0               # 0 in items area; 1 in options area
        self.option = 0             # which "option" button is selected. 0 is use

        # load images and check to make sure they loaded properly
        self.background = pygame.image.load(INVENTORY_BACKGROUND_SHEET_DIR)
        if self.background == 0:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.background.set_colorkey(COLOR_KEY)
        self.background = self.background.convert()

        self.small = pygame.image.load(ITEM_SHEET_SMALL_DIR)
        if self.small == 0:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.small.set_colorkey(COLOR_KEY)
        self.small = self.small.convert()

        self.large = pygame.image.load(ITEM_SHEET_LARGE_DIR)
        if self.large == 0:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.large.set_colorkey(COLOR_KEY)
        self.large = self.large.convert()

        self.box = pygame.image.load(ITEM_BOX_DIR)
        if self.box == 0:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.box.set_colorkey(COLOR_KEY)
        self.box = self.box.convert()

        self.font_options = pygame.font.Font(INVENTORY_FONT_DIR, INVENTORY_FONT_SIZE)
        self.font_description = pygame.font.Font(ITEM_FONT_DIR, ITEM_FONT_DESCRIPTION)
        self.font_count = pygame.font.Font(ITEM_FONT_DIR, ITEM_FONT_COUNT)
        self.font_name = pygame.font.Font(ITEM_FONT_DIR, ITEM_FONT_NAME)

    # add item to inventory
    def additem(self, item, special = 0):# item is an integer
        found = False
        empty = INVENTORY_SPACES
        for i in xrange(INVENTORY_SPACES):
            if self.items[i][0] == 0:
                if i < empty:
                    empty = i
            if self.items[i][0] == item:
                found = True
                self.items[i][1] += 1
                break
        if not found:
            self.items[empty] = [item, 1, special]
        return NO_PROBLEM

    # remove item at [x, y]
    def removeitem(self):
        out = self.items[self.index][0]
        self.items[self.index][1] -= 1
        if self.items[self.index][1] <= 0:
            self.items[self.index] = [0, 0, False]
        if out == 0:
            return None
        return out

    # load inventory from string
    def load(self, data):
        if not (len(data) % 3): # not a multiple of three
            return INCORRECT_DATA_FORMAT
        if len(data) != (INVENTORY_X * INVENTORY_Y * 3):
            return INCORRECT_DATA_LENGTH
        for i in xrange(INVENTORY_SPACES):
            self.items[i] = [ord(data[i * 3]), ord(data[i * 3 + 1]), ord[data[i * 3 + 2]]]
        return NO_PROBLEM

    # save inventory into a string of the specified format
    def save(self):
        '''
        Format:
            item | count | special | item | count | special | ...
            item    - 1 byte
            count   - 1 byte
            special - 1 byte
        '''
        return ''.join([chr(item) + chr(count) + chr(special) for item, count, special in self.items])

    # update location of "cursor"
    def update(self, event):
        # cursor in items area
        if self.mode == 0:
            if event.key == KEYBINDINGS[KB_UP]:
                if self.index == 0:
                    self.index = INVENTORY_SPACES - 1
                elif (self.index / INVENTORY_X) == 0:
                    self.index -= INVENTORY_X + 1
                else:
                    self.index -= INVENTORY_X
            elif event.key == KEYBINDINGS[KB_DOWN]:
                if self.index == (INVENTORY_SPACES - 1):
                    self.index = 0
                elif (self.index / INVENTORY_X) == (INVENTORY_Y - 1):
                    self.index += INVENTORY_X + 1
                else:
                    self.index += INVENTORY_X
            elif event.key == KEYBINDINGS[KB_LEFT]:
                self.index -= 1
            elif event.key == KEYBINDINGS[KB_RIGHT]:
                self.index += 1
            elif event.key == KEYBINDINGS[KB_ENTER]:
                # if there is an item at that spot
                if self.items[self.index][0] != 0:
                    self.option = 0
                    self.mode = 1
            self.index %= INVENTORY_SPACES
            return None
        # cursor in buttons area
        elif self.mode == 1:
            if event.key == KEYBINDINGS[KB_UP]:
                self.option -= 1
                return None
            elif event.key == KEYBINDINGS[KB_DOWN]:
                self.option += 1
                return None
            if not len(ITEMS[self.items[self.index][0]][2]):
                self.mode = 0
                return None
            self.option %= len(ITEMS[self.items[self.index][0]][2])
            if event.key == KEYBINDINGS[KB_ENTER]:
                # Cancel
                if ITEMS[self.items[self.index][0]][2][self.option] == ITEM_OPTIONS[0]:
                    self.mode = 0
                    return None
                # Drop
                elif ITEMS[self.items[self.index][0]][2][self.option] == ITEM_OPTIONS[1]:
                    self.mode = 0
                    return self.removeitem()
                # Read
                elif ITEMS[self.items[self.index][0]][2][self.option] == ITEM_OPTIONS[2]:
                    self.items[self.index][2] = 2
                    return None
                # Use
                elif ITEMS[self.items[self.index][0]][2][self.option] == ITEM_OPTIONS[3]:
                    return self.removeitem()
                else:
                    return None
        return None

    # display inventory
    def display(self, screen):
        if screen == 0:
            return SURFACE_DOES_NOT_EXIST

        # display inventory background
        screen.blit(self.background, (0, 0))

        # display items
        dy = ITEM_SMALL_HEIGHT - self.font_count.size("")[1]
        for i in xrange(INVENTORY_SPACES):
            if self.items[i][0]:
                clip = pygame.Rect(ITEM_SMALL_WIDTH * self.items[i][0], 0, ITEM_SMALL_WIDTH, ITEM_SMALL_HEIGHT)
                show = pygame.Rect((ITEM_SMALL_WIDTH + 1) * (i % INVENTORY_X) + 1, (ITEM_SMALL_HEIGHT + 1) * (i / INVENTORY_X) + 37, ITEM_SMALL_WIDTH, ITEM_SMALL_HEIGHT)
                screen.blit(self.small, show, clip)
                show.y += dy
                show.x += 5
                text_image = self.font_count.render(str(self.items[i][1]), ITEM_FONT_ANTIALIAS, ITEM_FONT_COLOR)
                screen.blit(text_image, show)

        # display highlight
        show = pygame.Rect((ITEM_SMALL_WIDTH + 1)  * (self.index % INVENTORY_X) + 1, (ITEM_SMALL_HEIGHT + 1) * (self.index / INVENTORY_X) + 37, ITEM_SMALL_WIDTH, ITEM_SMALL_HEIGHT)
        screen.blit(self.box, show)

        # display buttons
        text_image = None
        show = copy.deepcopy(INVENTORY_BUTTON)
        dy = self.font_options.size("")[1]
        for i in xrange(len(ITEMS[self.items[self.index][0]][2])):
            # if an item is selected for usage
            if (self.mode == 1) and (self.option == i):
                text_image = self.font_options.render(ITEMS[self.items[self.index][0]][2][i], INVENTORY_FONT_ANTIALIAS, INVENTORY_FONT_COLOR, INVENTORY_BACKGROUND_COLOR)
            else:
                text_image = self.font_options.render(ITEMS[self.items[self.index][0]][2][i], INVENTORY_FONT_ANTIALIAS, INVENTORY_FONT_COLOR)
            screen.blit(text_image, show)
            show.y += dy

        # if there is an item
        if self.items[self.index][0] != 0:
            # display larger version of selected item
            clip = pygame.Rect(ITEM_LARGE_WIDTH * self.items[self.index][0], 0, ITEM_LARGE_WIDTH, ITEM_LARGE_HEIGHT)
            screen.blit(self.large, ITEM_IMAGE_BOX, clip)
            text_image = self.font_name.render(ITEMS[self.items[self.index][0]][0], ITEM_FONT_ANTIALIAS, ITEM_FONT_COLOR)
            screen.blit(text_image, ITEM_NAME_BOX)

            show = copy.deepcopy(ITEM_DESCRIPTION_BOX)
            dy = self.font_description.size("")[1]
            if self.items[self.index][2] != 1:
                for desc in ITEMS[self.items[self.index][0]][1]:
                    text_image = self.font_description.render(desc, ITEM_FONT_ANTIALIAS, ITEM_FONT_COLOR)
                    screen.blit(text_image, show)
                    show.y += dy

        return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # create the screen
    if screen == 0:
        sys.exit(SCREEN_DOES_NOT_EXIST)

    pygame.display.set_caption("Inventory Demo")
    pygame.key.set_repeat(100, 100)

    test = Inventory()

    # adda a bunch of items
    test.additem(1, 1)      # book
    test.additem(2)
    test.additem(3); test.additem(3); test.additem(3)

    # move cursor to (1, 0)
    test.index = 1

    # remove item 2
    test.removeitem()

    # test save and load
    test.load(test.save())

    quit = False
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True
            if event.type == pygame.KEYDOWN:
                test.update(event)
        test.display(screen)
        pygame.display.flip()

    pygame.quit()
