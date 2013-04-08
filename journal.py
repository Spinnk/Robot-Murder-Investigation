#! /usr/bin/python

# Journal Class

# journal.py is part of Sentience in Space.
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
from keybinding import *

import pygame

class Journal:
    def __init__(self):
        self.mode = 0       # mode 0 = list, mode 1 = journal entry
        self.cursor = 0     # which entry cursor is at
        self.start = 0      # camera for side bar
        self.line = 0       # camera for data
        self.entries = []   # array of entries; just integers
        self.font_list = pygame.font.Font(JOURNAL_FONT_DIR, JOURNAL_FONT_LIST_SIZE)
        self.font_small = pygame.font.Font(JOURNAL_FONT_DIR, JOURNAL_FONT_SMALL_SIZE)
        self.font_large = pygame.font.Font(JOURNAL_FONT_DIR, JOURNAL_FONT_LARGE_SIZE)

        # load images and check to make sure they loaded properly
        self.background = pygame.image.load(JOURNAL_BACKGROUND_DIR)
        if self.background == 0:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.background.set_colorkey(COLOR_KEY)
        self.background = self.background.convert()

    def addentry(self, new_entry):
        if new_entry not in self.entries:
            self.entries += [new_entry]
        return NO_PROBLEM

    # shouldnt need this
    def removeentry(self, old_entry):
        if old_entry in self.entry:
            self.entry.remove(old_entry)
            return NO_PROBLEM
        return NOT_FOUND

    def load(self, data):
        self.entries = [ord(x) for x in data]
        return NO_PROBLEM

    def save(self):
        '''
        Format:
            entry | entry | ...
            entry - 1 byte
        '''
        return ''.join([chr(entry) for entry in self.entries])

    def update(self, keybinding):
        keystates = pygame.key.get_pressed()
        if self.mode == 0: # at side bar
            if keystates[keybinding[KB_UP]]:
                self.cursor -= 1
            elif keystates[keybinding[KB_DOWN]]:
                self.cursor += 1
            elif keystates[keybinding[KB_RIGHT]]:
                self.mode = 1
                self.line = 0
            # make sure cursor is within bound
            if self.cursor < 0:
                self.cursor = 0
            if self.cursor >= len(self.entries):
                self.cursor = len(self.entries) - 1
            # move camera
            if self.cursor - self.start < 0:
                self.start -= 1
            if self.cursor - self.start > 0:
                self.start += 1
            if self.start < 0:
                self.start = 0
            if (self.start + JOURNAL_MAX_SHOW) > len(self.entries):
                self.start = len(self.entries) - JOURNAL_MAX_SHOW
            if self.start < 0:
                self.start = 0
        elif self.mode == 1: # reading entry
            if keystates[keybinding[KB_UP]]:
                self.line -= 1
            elif keystates[keybinding[KB_DOWN]]:
                self.line += 1
            if keystates[keybinding[KB_LEFT]]:
                self.mode = 0
            # make sure camera is within bound
            if (self.line + JOURNAL_MAX_LINES) > len(JOURNAL[self.entries[self.cursor]][1]):
                self.line = len(JOURNAL[self.entries[self.cursor]][1]) - JOURNAL_MAX_LINES
            if self.line < 0:
                self.line = 0

    def display(self, screen):
        if screen == 0:
            return SURFACE_DOES_NOT_EXIST
        screen.blit(self.background, (0, 0))

        # display availible journal entries
        show = copy.deepcopy(JOURNAL_LIST_BOX)
        dy = self.font_list.size("")[1]
        for i in xrange(self.start, min(len(self.entries), self.start + JOURNAL_MAX_SHOW)):
            if i == self.cursor:
                text = self.font_list.render(JOURNAL[self.entries[i]][0], JOURNAL_FONT_ANTIALIAS, JOURNAL_FONT_COLOR, JOURNAL_FONT_BACKGROUND_COLORS[self.mode])
            else:
                text = self.font_list.render(JOURNAL[self.entries[i]][0], JOURNAL_FONT_ANTIALIAS, JOURNAL_FONT_COLOR)
            screen.blit(text, show)
            show.y += dy

        # if there is something to show
        if len(self.entries):
            # display title
            show = copy.deepcopy(JOURNAL_SHOW_BOX)
            text = self.font_large.render(JOURNAL[self.entries[self.cursor]][0], JOURNAL_FONT_ANTIALIAS, JOURNAL_FONT_COLOR)
            screen.blit(text, JOURNAL_SHOW_BOX)

            # display data
            dy = self.font_small.size("")[1]
            show.y += dy; show.y += dy
            for line in JOURNAL[self.entries[self.cursor]][1][self.line: min(len(JOURNAL[self.cursor][1]), self.line + JOURNAL_MAX_LINES)]:
                text = self.font_small.render(line, JOURNAL_FONT_ANTIALIAS, JOURNAL_FONT_COLOR)
                screen.blit(text, show)
                show.y += dy

        return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # create the screen
    if screen == 0:
        sys.exit(SCREEN_DOES_NOT_EXIST)

    pygame.display.set_caption("Journal Demo")
    pygame.key.set_repeat(100, 100)

    keybindings = default_keybindings()
    test = Journal()
    test.addentry(0)
    test.addentry(1)
    test.addentry(2)
    test.addentry(3)

    quit = False
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True
        test.update(keybindings)
        test.display(screen)
        pygame.display.flip()

    pygame.quit()
