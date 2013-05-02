#! /usr/bin/python

# Dialogue Class

# dialogue.py is part of Sentience in Space.
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

class Dialogue:
    def __init__(self, dialogue = []):
        self.dialogue = dialogue    # entire single conversation
        self.mode = 0               # mode 0 = npc, mode 1 = user
        self.line = 0               # camera for text
        self.cursor = 0             # selected line; only used in mode 1
        self.index = 0              # where in the dialogue user is at
        self.dialogue = []          # array of array of strings
        self.choice = -1            # which stuff to say next
        self.font = pygame.font.Font(DIALOGUE_FONT_DIR, DIALOGUE_FONT_SIZE)

    def setdialogue(self, dialogue):
        self.index = 0;
        self.dialogue = dialogue

    # tells the class who is saying dialogue index 0
    def start(self, speaker = 0):
        self.mode = speaker

    def end(self):
        return 0        # maybe change this to return flags or something

    def update(self, event):
        if self.index < len(self.dialogue):
            if self.mode == 0: # NPC talking
                if event.key == KEYBINDINGS[KB_ENTER]:
                    self.choice = -1
                elif event.key == KEYBINDINGS[KB_UP]:
                    self.line -= 1
                elif event.key == KEYBINDINGS[KB_DOWN]:
                    self.line += 1
                if (self.line + DIALOGUE_MAX_LINES) > len(self.dialogue[self.index]):
                    self.line = len(self.dialogue[self.index]) - DIALOGUE_MAX_LINES
                if self.line < 0:
                    self.line = 0
            elif self.mode == 1: # user talking/picking:
                if event.key == KEYBINDINGS[KB_ENTER]:
                    self.choice = self.cursor + self.line
                if event.key == KEYBINDINGS[KB_UP]:
                    self.cursor -= 1
                    if self.cursor < 0:
                        self.cursor = 0
                        self.line -= 1
                        if self.line < 0:
                            self.line = 0
                elif event.key == KEYBINDINGS[KB_DOWN]:
                    self.cursor += 1
                    if self.cursor >= len(self.dialogue[self.index]):
                        self.cursor = len(self.dialogue[self.index]) - 1
                    else:
                        if self.cursor >= DIALOGUE_MAX_LINES:
                            self.cursor = DIALOGUE_MAX_LINES - 1
                            self.line += 1
                            if (self.line + DIALOGUE_MAX_LINES) > len(self.dialogue[self.index]):
                                self.line = len(self.dialogue[self.index]) - DIALOGUE_MAX_LINES
            if event.key == KEYBINDINGS[KB_ENTER]:
                self.mode ^= True
                self.line = 0
                self.cursor = 0
                self.index += 1
            return NO_PROBLEM
        return DIALOGUE_ENDED

    def display(self, screen):
        if screen == 0:
            return SURFACE_DOES_NOT_EXIST

        # display text box
        screen.fill(DIALOGUE_BACKGROUND, DIALOGUE_SHOW_BOX);

        if (self.index < len(self.dialogue)):
            # if the NPC is talking
            if self.mode == 0:
                show = copy.deepcopy(DIALOGUE_TEXT_BOX)
                dy = self.font.size("")[1]
                for line in self.dialogue[self.index][self.line: self.line + DIALOGUE_MAX_LINES]:
                    text = self.font.render(line, DIALOGUE_FONT_ANTIALIAS, DIALOGUE_FONT_COLOR)
                    screen.blit(text, show)
                    show.y += dy
            # if the user is choosing
            elif self.mode == 1:
                # display highlight
                dy = self.font.size("")[1]
                show = pygame.Rect(DIALOGUE_SHOW_BOX.x, DIALOGUE_TEXT_BOX.y + self.cursor * dy, SCREEN_WIDTH, dy)
                screen.fill(DIALOGUE_FONT_SELECTED, show)
                # display choices
                show = copy.deepcopy(DIALOGUE_TEXT_BOX)
                for line in self.dialogue[self.index][self.line: self.line + DIALOGUE_MAX_LINES]:
                    text = self.font.render(line, DIALOGUE_FONT_ANTIALIAS, DIALOGUE_FONT_COLOR)
                    screen.blit(text, show)
                    show.y += dy
        return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # create the screen
    if screen == 0:
        sys.exit(SCREEN_DOES_NOT_EXIST)

    pygame.display.set_caption("Dialogue Demo")
    pygame.key.set_repeat(100, 100)

    test = Dialogue()
    test.setdialogue([["Hello World", "Line 2", "Line3", "Line 4", "Line 5", "Line 6", "Line 7"], ["choice 1", "choice 2", "choice 3","choice 1", "choice 2", "choice 3" ]])
    test.start()

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
