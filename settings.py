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

import pygame

from consts import *

# Keybindings Enum
# special case positioning of global variables
# should never be touched by users
KB_UP = 0
KB_LEFT = 1
KB_DOWN = 2
KB_RIGHT = 3
KB_USE = 4
KB_INVENTORY = 5
KB_JOURNAL = 6
KB_ENTER = 7
KB_ESCAPE = 8
KB_LIFT = 9

# default settings
# assumes variables are already global
def defaultsettings():
    return {KB_UP: pygame.K_w,
            KB_LEFT: pygame.K_a,
            KB_DOWN: pygame.K_s,
            KB_RIGHT: pygame.K_d,
            KB_USE: pygame.K_e,
            KB_INVENTORY: pygame.K_i,
            KB_JOURNAL: pygame.K_j,
            KB_ENTER: pygame.K_RETURN,
            KB_ESCAPE: pygame.K_ESCAPE,
            KB_LIFT: pygame.K_l
            }, 1.0, 1.0

def readsettings(file_name):
    f = open(file_name, 'r')
    settings = f.readlines()
    f.close()
    i = 0
    keybindings, volume, brightness = defaultsettings()
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
                    keybindings[KB_UP] = int(line[3:])
                elif line[:4] == 'Left':
                    keybindings[KB_LEFT] = int(line[5:])
                elif line[:4] == 'Down':
                    keybindings[KB_DOWN] = int(line[5:])
                elif line[:5] == 'Right':
                    keybindings[KB_RIGHT] = int(line[6:])
                elif line[:3] == 'Use':
                    keybindings[KB_USE] = int(line[4:])
                elif line[:9] == 'Inventory':
                    keybindings[KB_INVENTORY] = int(line[10:])
                elif line[:7] == "Journal":
                    keybindings[KB_JOURNAL] = int(line[8:])
                elif line[:5] == 'Enter':
                    keybindings[KB_ENTER] = int(line[6:])
                elif line[:6] == 'Escape':
                    keybindings[KB_ESCAPE] = int(line[7:])
                elif line[:4] == 'Lift':
                    keybindings[KB_LIFT] = int(line[5:])
                i += 1
        elif settings[i] == '-----BEGIN MUSIC SETTINGS-----\n':
            i += 1
            while settings[i] != '-----END MUSIC SETTINGS-----\n':
                line = settings[i]
                if line[0] == '#':
                    continue
                line = line[:-1]        # remove newline char
                if line[:6] == 'Volume':
                    volume = int(line[7:])
                i += 1
        elif settings[i] == '-----BEGIN SCREEN SETTINGS-----\n':
            i += 1
            while settings[i] != '-----END SCREEN SETTINGS-----\n':
                line = settings[i]
                if line[0] == '#':
                    continue
                line = line[:-1]        # remove newline char
                if line[:10] == 'Brightness':
                    brightness = int(line[11:])
                i += 1
        i += 1
        return keybindings, volume, brightness

def writesettings(file_name, keybindings, volume, brightness):
    f = open(file_name, 'w')
    f.write('# Sentience in Space\n' +
            '\n-----BEGIN KEYBINDINGS-----' +
            '\nUp=' + str(keybindings[KB_UP]) +
            '\nLeft=' + str(keybindings[KB_LEFT]) +
            '\nDown=' + str(keybindings[KB_DOWN]) +
            '\nRight=' + str(keybindings[KB_RIGHT]) +
            '\nUse=' + str(keybindings[KB_USE]) +
            '\nInventory=' + str(keybindings[KB_INVENTORY]) +
            '\nJournal=' + str(keybindings[KB_JOURNAL]) +
            '\nEnter=' + str(keybindings[KB_ENTER]) +
            '\nEscape=' + str(keybindings[KB_ESCAPE]) +
            '\nLift=' + str(keybindings[KB_LIFT]) +
            '\n-----END KEYBINDINGS-----'
            '\n'
            '\n-----BEGIN MUSIC SETTINGS-----' +
            '\nVolume=' + str(volume) +
            '\n-----END MUSIC SETTINGS-----' +
            '\n'
            '\n-----BEGIN SCREEN SETTINGS-----' +
            '\nBrightness=' + str(brightness) +
            '\n-----END SCREEN SETTINGS-----' +
            '\n')
    f.close()

if __name__=='__main__':
    keybindings, volume, brightness = defaultsettings()
    writesettings(SETTINGS_DIR, keybindings, volume, brightness)
    readsettings(SETTINGS_DIR)
