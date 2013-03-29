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
            KB_USE: pygame.K_e,
            KB_INVENTORY: pygame.K_i,
            KB_ENTER: pygame.K_RETURN,
            KB_ESCAPE: pygame.K_ESCAPE
            }

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
        if bind[:2] == 'Up':
            keybindings[KB_UP] = int(bind[3:])
        elif bind[:4] == 'Left':
            keybindings[KB_LEFT] = int(bind[5:])
        elif bind[:4] == 'Down':
            keybindings[KB_DOWN] = int(bind[5:])
        elif bind[:5] == 'Right':
            keybindings[KB_RIGHT] = int(bind[6:])
        elif bind[:3] == 'Use':
            keybindings[KB_USE] = int(bind[4:])
        elif bind[:9] == 'Inventory':
            keybindings[KB_INVENTORY] = int(bind[10:])
        elif bind[:5] == 'Enter':
            keybindings[KB_ENTER] = int(bind[6:])
        elif bind[:6] == 'Escape':
            keybindings[KB_ESCAPE] = int(bind[7:])
    return keybindings

# write keybindings to a settings file
def write_keybindings(file_name, keybindings):
    f = open(file_name, 'w')
    f.write('# Sentience in Space keybindings\n')
    f.write('\nUp=' + str(keybindings[KB_UP]))
    f.write('\nLeft=' + str(keybindings[KB_LEFT]))
    f.write('\nDown=' + str(keybindings[KB_DOWN]))
    f.write('\nRight=' + str(keybindings[KB_RIGHT]))
    f.write('\nUse=' + str(keybindings[KB_USE]))
    f.write('\nInventory=' + str(keybindings[KB_INVENTORY]))
    f.write('\nEnter=' + str(keybindings[KB_ENTER]))
    f.write('\nEscape=' + str(keybindings[KB_ESCAPE]))
    f.write('\n')   # final newline char
    f.close()
    return NO_PROBLEM

if __name__=='__main__':
    keybindings = default_keybindings()
    write_keybindings(KEYBINDINGS_DIR, keybindings)
