# Inventory Class

# Currently displays inventory as list
# Maybe change to fixed size 2D array or something

# For displaying on map, maybe instead of having multiple
# tile types, just hold a list of items and their coordinates

from consts import *
from keybinding import *

class Inventory:
    def __init__(self, background, small, large):
        self.items = [] # list of (item #, count)
        self.selected = 0

        self.background = pygame.image.load(background)
        if self.background == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.background.set_colorkey(COLORKEY)
        self.background = self.background.convert()

        self.small = pygame.image.load(small)
        if self.small == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.small.set_colorkey(COLORKEY)
        self.small = self.background.convert()

        self.large = pygame.image.load(large)
        if self.large == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.large.set_colorkey(COLORKEY)
        self.large = self.background.convert()

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
    def update(self, keystates, keybinding):
        '''if keystates[keybinding[KB_UP]]:
            selected -= 6
        if keystates[keybinding[KB_DOWN]]:
            selected += 6
        if keystates[keybinding[KB_LEFT]]:
            selected -= 1
        if keystates[keybinding[KB_RIGHT]]:
            selected += 1    
        if selected == -1:
            selected = len(self.items) - 1
        if selected == len(self.items):
            selected = 0'''
        return NO_PROBLEM

    # display unselected items
    def display(self, screen):
        if screen == NULL:
            return SURFACE_DOES_NOT_EXIST

        # display inventory background
        screen.blit(background, (0, 0))

        # display items
        # should display count of items too
        count = 0
        for item in self.items:
            clip = pygame.Rect(ITEM_SMALL_WIDTH * (count % 6), ITEM_SMALL_HEIGHT * (count / 8), ITEM_SMALL_WIDTH, ITEM_SMALL_HEIGHT)
            show = pygame.Rect(ITEM_SMALL_WIDTH * item[0], 0, ITEM_SMALL_WIDTH, ITEM_SMALL_HEIGHT)
            screen.blit(self.small, show, clip)

        # display highlight

        # display selected item
        clip = pygame.Rect(ITEM_LARGE_WIDTH * self.items[self.selected][0], ITEM_LARGE_HEIGHT * (count / 8), ITEM_LARGE_WIDTH, ITEM_LARGE_HEIGHT)
        show = pygame.Rect(639, 41, ITEM_LARGE_WIDTH, ITEM_LARGE_HEIGHT)
        screen.blit(self.large, show, clip)

        return NO_PROBLEM

if __name__=='__main__':
    pass
