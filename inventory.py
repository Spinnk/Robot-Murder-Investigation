# Inventory Class

# Currently displays inventory as list
# Maybe change to fixed size 2D array or something

# For displaying on map, maybe instead of having multiple
# tile types, just hold a list of items and their coordinates

from consts import *
from keybinding import *

class Inventory:
    def __init__(self):
        self.items = [] # list of (item #, count)
        self.selected = 0

    def add(self, new_item):# item is an integer
        found = False
        for item in self.items:
            if item[0] == new_item:
                found = True
                item[1] += 1
        if not found:
            self.items += [(item, 1)]
        return NO_PROBLEM

    def remove(self, to_rem):
        for i in len(self.items):
            if self.items[i][0] == to_rem:
                self.items[i][1] -= 1
                if self.items[i][1] == 0:
                    del self.items[i]
                return NO_PROBLEM
        return ITEM_DOES_NOT_EXIST

    # display selected, individual item
    # need to implement scrolling
    def update(self, keystates):
        if keystates[KB_UP]:
            selected -= 1
        if keystates[KB_DOWN]:
            selected += 1
        if selected == -1:
            selected = len(self.items) - 1
        if selected == len(self.items):
            selected = 0
        return NO_PROBLEM

    # display unselected items
    def display(self, screen):
        if screen == NULL:
            return SURFACE_DOES_NOT_EXIST

        # display inventory background
        screen.blit(INVENTORY_BACKGROUND, (0, 0))

        # display list of items
        # need to implement highlight box (or something) that moves

        # display selected item
        if len(self.items) > 0:
            # display image
            clip = pygame.Rect(self.selected * ITEM_WIDTH, 0, ITEM_WIDTH, ITEM_HEIGHT)
            screen.blit(image, ITEM_BOX, clip)

            # display name

            # display description

        return NO_PROBLEM
