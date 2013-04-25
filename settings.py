#! /usr/bin/python

# Settings
# Displayed in game and stored as integers

# Settings.py is part of Sentience in Space.
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

import pygame

from consts import *

# string names
class Button:
    def __init__(self, name, loc):
        self.name = name
        self.loc = loc
        self.font = pygame.font.Font(KEY_FONT_DIR, KEY_FONT_SIZE)

    def update(self, name):
        self.name = name

    def display(self, screen):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        screen.blit(self.font.render(self.name, KEY_FONT_ANTIALIAS, KEY_FONT_COLOR), self.loc)

# integer names
class Key:
    def __init__(self, value, loc):
        self.value = value
        self.loc = loc
        self.font = pygame.font.Font(KEY_FONT_DIR, KEY_FONT_SIZE)

    def update(self, value):
        self.value = value

    def display(self, screen):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        screen.blit(self.font.render(KB_NAMES[self.value] + ": " + str(KEYBINDINGS[self.value]), KEY_FONT_ANTIALIAS, KEY_FONT_COLOR), self.loc)

class Slider:
    def __init__(self, name = '', pos = pygame.Rect(0, 0, 0, 0), sections = 100, box = 0.0):
        self.name = name
        self.sections = sections
        self.setpos(pos)
        self.setsections(sections)
        self.setbox(box)
        self.font = pygame.font.Font(KEY_FONT_DIR, KEY_FONT_SIZE)

    # position of slider box
    def setpos(self, rect):
        self.pos = rect                                                                                 # position and size of entire slider
        self.box = pygame.Rect(self.pos.x, self.pos.y, self.pos.w / self.sections, self.pos.h)          # position and size of box

    def getpos(self):
        return self.pos

    # set where the box is at
    def setbox(self, box):
        self.box.x = self.pos.x + self.pos.w * box

    # number of divisions
    def setsections(self, sec):
        self.sections = sec
        self.box.w = self.pos.w / self.sections

    def getsections(self):
        return self.sections

    def update(self, event):
        if event.key == KEYBINDINGS[KB_RIGHT]:
            self.box.x += self.pos.w / self.sections
            if self.box.x >= (self.pos.x + self.pos.w):
                self.box.x = self.pos.x + self.pos.w
        elif event.key == KEYBINDINGS[KB_LEFT]:
            self.box.x -= self.pos.w / self.sections
            if self.box.x < self.pos.x:
                self.box.x = self.pos.x
        return float(self.box.x - self.pos.x) / self.pos.w

    def display(self, screen, color = (0xff, 0xff, 0xff)):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        self.pos.y -= self.font.size("")[1]
        screen.blit(self.font.render(self.name, KEY_FONT_ANTIALIAS, KEY_FONT_COLOR), self.pos)
        self.pos.y += self.font.size("")[1]
        pygame.draw.line(screen, color, (self.pos.x, self.pos.y + self.pos.h / 2), (self.pos.x + self.pos.w + self.pos.w / self.sections - 1, self.pos.y + self.pos.h / 2))
        pygame.draw.rect(screen, color, self.box)
        return NO_PROBLEM

class Settings:
    def __init__(self):
        self.mode = 0               # 0 = going up and down; 1 = change
        self.line = 0
        self.lines = [  Key(KB_UP, SETTINGS_BOXES[0]),
                        Key(KB_LEFT, SETTINGS_BOXES[1]),
                        Key(KB_DOWN, SETTINGS_BOXES[2]),
                        Key(KB_RIGHT, SETTINGS_BOXES[3]),
                        Key(KB_USE, SETTINGS_BOXES[4]),
                        Key(KB_INVENTORY, SETTINGS_BOXES[5]),
                        Key(KB_JOURNAL, SETTINGS_BOXES[6]),
                        Key(KB_ENTER, SETTINGS_BOXES[7]),
                        Key(KB_ESCAPE, SETTINGS_BOXES[8]),
                        Key(KB_LIFT, SETTINGS_BOXES[9]),
                        Key(KB_MAP, SETTINGS_BOXES[10]),
                        Slider("Volume", SETTINGS_BOXES[11], 25),
                        Slider("Brightness", SETTINGS_BOXES[12], 25),
                        Button("Save", SETTINGS_BOXES[13]),
                        Button("Default", SETTINGS_BOXES[14])]

    def default(self):
        global KEYBINDINGS, SOUND_VOLUME, SCREEN_BRIGHTNESS
        KEYBINDINGS = { KB_UP: pygame.K_w,
                        KB_LEFT: pygame.K_a,
                        KB_DOWN: pygame.K_s,
                        KB_RIGHT: pygame.K_d,
                        KB_USE: pygame.K_e,
                        KB_INVENTORY: pygame.K_i,
                        KB_JOURNAL: pygame.K_j,
                        KB_ENTER: pygame.K_RETURN,
                        KB_ESCAPE: pygame.K_ESCAPE,
                        KB_LIFT: pygame.K_l,
                        KB_MAP: pygame.K_m}
        SOUND_VOLUME = 1.0
        SCREEN_BRIGHTNESS = 1.0

        self.lines[11].setbox(0)
        self.lines[12].setbox(0)

    def move(self, new_value):
        if self.line == 0:
            KEYBINDINGS[KB_UP] = new_value
        elif self.line == 1:
            KEYBINDINGS[KB_LEFT] = new_value
        elif self.line == 2:
            KEYBINDINGS[KB_DOWN] = new_value
        elif self.line == 3:
            KEYBINDINGS[KB_RIGHT] = new_value
        elif self.line == 4:
            KEYBINDINGS[KB_USE] = new_value
        elif self.line == 5:
            KEYBINDINGS[KB_INVENTORY] = new_value
        elif self.line == 6:
            KEYBINDINGS[KB_JOURNAL] = new_value
        elif self.line == 7:
            KEYBINDINGS[KB_ENTER] = new_value
        elif self.line == 8:
            KEYBINDINGS[KB_ESCAPE] = new_value
        elif self.line == 9:
            KEYBINDINGS[KB_LIFT] = new_value
        elif self.line == 10:
            KEYBINDINGS[KB_MAP] = new_value
        elif self.line == 11:
            global SOUND_VOLUME
            SOUND_VOLUME = new_value
            pygame.mixer.music.set_volume(SOUND_VOLUME)
        elif self.line == 12:
            global SCREEN_BRIGHTNESS
            SCREEN_BRIGHTNESS = 1.0 - new_value
            pygame.display.set_gamma(SCREEN_BRIGHTNESS)

    def load(self, file_name):
        f = open(file_name, 'r')
        settings = f.readlines()
        f.close()
        global KEYBINDINGS, SOUND_VOLUME, SCREEN_BRIGHTNESS
        i = 0
        while i < len(settings):
            if settings[i][0] == '#':
                i += 1
                continue
            elif settings[i] == '-----BEGIN KEYBINDINGS-----\n':
                i += 1
                while settings[i] != '-----END KEYBINDINGS-----\n':
                    line = settings[i]
                    if line[0] == '#':
                        continue
                    line = line[:-1]        # remove newline char
                    if line[:2] == 'Up':
                        KEYBINDINGS[KB_UP] = int(line[3:])
                    elif line[:4] == 'Left':
                        KEYBINDINGS[KB_LEFT] = int(line[5:])
                    elif line[:4] == 'Down':
                        KEYBINDINGS[KB_DOWN] = int(line[5:])
                    elif line[:5] == 'Right':
                        KEYBINDINGS[KB_RIGHT] = int(line[6:])
                    elif line[:3] == 'Use':
                        KEYBINDINGS[KB_USE] = int(line[4:])
                    elif line[:9] == 'Inventory':
                        KEYBINDINGS[KB_INVENTORY] = int(line[10:])
                    elif line[:7] == "Journal":
                        KEYBINDINGS[KB_JOURNAL] = int(line[8:])
                    elif line[:5] == 'Enter':
                        KEYBINDINGS[KB_ENTER] = int(line[6:])
                    elif line[:6] == 'Escape':
                        KEYBINDINGS[KB_ESCAPE] = int(line[7:])
                    elif line[:4] == 'Lift':
                        KEYBINDINGS[KB_LIFT] = int(line[5:])
                    elif line[:3] == 'Map':
                        KEYBINDINGS[KB_MAP] = int(line[4:])
                    i += 1
            elif settings[i] == '-----BEGIN MUSIC SETTINGS-----\n':
                i += 1
                while settings[i] != '-----END MUSIC SETTINGS-----\n':
                    line = settings[i]
                    if line[0] == '#':
                        continue
                    line = line[:-1]        # remove newline char
                    if line[:6] == 'Volume':
                        SOUND_VOLUME = float(line[7:])
                        self.lines[11].setbox(1 - SOUND_VOLUME)
                    i += 1
            elif settings[i] == '-----BEGIN SCREEN SETTINGS-----\n':
                i += 1
                while settings[i] != '-----END SCREEN SETTINGS-----\n':
                    line = settings[i]
                    if line[0] == '#':
                        continue
                    line = line[:-1]        # remove newline char
                    if line[:10] == 'Brightness':
                        SCREEN_BRIGHTNESS = float(line[11:])
                        self.lines[12].setbox(1 - SCREEN_BRIGHTNESS)
                    i += 1
            i += 1

    def save(self, file_name):
        f = open(file_name, 'w')
        f.write('# Sentience in Space\n' +
                '\n-----BEGIN KEYBINDINGS-----' +
                '\nUp=' + str(KEYBINDINGS[KB_UP]) +
                '\nLeft=' + str(KEYBINDINGS[KB_LEFT]) +
                '\nDown=' + str(KEYBINDINGS[KB_DOWN]) +
                '\nRight=' + str(KEYBINDINGS[KB_RIGHT]) +
                '\nUse=' + str(KEYBINDINGS[KB_USE]) +
                '\nInventory=' + str(KEYBINDINGS[KB_INVENTORY]) +
                '\nJournal=' + str(KEYBINDINGS[KB_JOURNAL]) +
                '\nEnter=' + str(KEYBINDINGS[KB_ENTER]) +
                '\nEscape=' + str(KEYBINDINGS[KB_ESCAPE]) +
                '\nLift=' + str(KEYBINDINGS[KB_LIFT]) +
                '\nMap=' + str(KEYBINDINGS[KB_MAP]) +
                '\n-----END KEYBINDINGS-----'
                '\n'
                '\n-----BEGIN MUSIC SETTINGS-----' +
                '\nVolume=' + str(SOUND_VOLUME) +
                '\n-----END MUSIC SETTINGS-----' +
                '\n'
                '\n-----BEGIN SCREEN SETTINGS-----' +
                '\nBrightness=' + str(SCREEN_BRIGHTNESS) +
                '\n-----END SCREEN SETTINGS-----' +
                '\n')
        f.close()

    def update(self, event):
        if self.mode == 0:
            if event.key == KEYBINDINGS[KB_DOWN]:
                self.line += 1
                if self.line >= len(SETTINGS_BOXES):
                    self.line = len(SETTINGS_BOXES) - 1
            elif event.key == KEYBINDINGS[KB_UP]:
                self.line -= 1
                if self.line < 0:
                    self.line = 0
            elif event.key == KEYBINDINGS[KB_RIGHT]:
                if self.line == 13:
                    self.save(SETTINGS_DIR)
                elif self.line == 14:
                    self.default()
                else:
                    self.mode = 1
        elif self.mode == 1:
            if self.line < 11:
                if event.key == KEYBINDINGS[KB_LEFT]:
                    self.mode = 0
                else:
                    self.move(event.key)
                    self.mode = 0
            elif (self.line == 11) or (self.line == 12):
                if event.key == KEYBINDINGS[KB_RIGHT]:
                    self.move(self.lines[self.line].update(event))
                elif event.key == KEYBINDINGS[KB_LEFT]:
                    self.move(self.lines[self.line].update(event))
                elif (event.key != KEYBINDINGS[KB_RIGHT]) and (event.key != KEYBINDINGS[KB_LEFT]):
                    self.mode = 0

    def display(self, screen):
        if screen == None:
            return SURFACE_DOES_NOT_EXIST
        SETTINGS_BACKGROUND_BOX.y = SETTINGS_BOXES[self.line].y - 5
        pygame.draw.rect(screen, SETTINGS_BACKGROUND_COLORS[self.mode], SETTINGS_BACKGROUND_BOX)

        for line in self.lines:
            line.display(screen)

        return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # create the screen
    if screen == None:
        sys.exit(SCREEN_DOES_NOT_EXIST)

    pygame.display.set_caption("Settings Demo")
    pygame.key.set_repeat(100, 100)

    test = Settings()
    test.load(SETTINGS_DIR)
#    test.default()
#    test.save(SETTINGS_DIR)

    quit = False
    while not(quit):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit when close window "X" is pressed
                quit = True
            if event.type == pygame.KEYDOWN:
                test.update(event)
        screen.fill(BLACK)
        test.display(screen)
        pygame.display.flip()

        pygame.time.Clock().tick(FPS)

    pygame.quit()
