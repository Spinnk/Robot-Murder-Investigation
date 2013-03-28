# Key Bindings
# Displayed in game and stored as integers
# Different keyboards potentially have different values

from consts import *

import pygame

# set default keybindings
def default_keybindings():
    return {KB_UP: pygame.K_w,
            KB_LEFT: pygame.K_a,
            KB_DOWN: pygame.K_s,
            KB_RIGHT: pygame.K_d,
            KB_USE: pygame.K_e}

# reads in keybindings from properly formatted settings file
def read_keybindings(file_name):
    f = open(file_name, 'r')
    settings = f.readlines()
    f.close()
    keybindings = {}
    for bind in settings:
        if bind[0] == '#':
            continue
        bind = bind[:-1]        # remove newline char
        if bind[:2] == 'UP':
            keybindings[KB_UP] = int(bind[3:])
        elif bind[:4] == 'LEFT':
            keybindings[KB_LEFT] = int(bind[5:])
        elif bind[:4] == 'DOWN':
            keybindings[KB_DOWN] = int(bind[5:])
        elif bind[:5] == 'RIGHT':
            keybindings[KB_RIGHT] = int(bind[6:])
        elif bind[:3] == 'USE':
            keybindings[KB_USE] = int(bind[4:])
    return keybindings

# write keybindings to a settings file
def write_keybindings(file_name, keybindings):
    f = open(file_name, 'w')
    f.write('# Sentience in Space keybindings\n')
    f.write('\nUP=' + str(keybindings[KB_UP]))
    f.write('\nLEFT=' + str(keybindings[KB_LEFT]))
    f.write('\nDOWN=' + str(keybindings[KB_DOWN]))
    f.write('\nRIGHT=' + str(keybindings[KB_RIGHT]))
    f.write('\nUSE=' + str(keybindings[KB_USE]))
    f.write('\n')   # final newline char
    f.close()
    return NO_PROBLEM

if __name__=='__main__':
    default_keybindings()
    write_keybindings(KEYBINDINGS)
