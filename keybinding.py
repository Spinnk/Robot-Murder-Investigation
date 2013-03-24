# Key Bindings
# Displayed in game and stored as integers
# Different keyboards potentially have different values

# http://stackoverflow.com/questions/15595393/python-global-variable-scoping/15595447?noredirect=1#15595447

from consts import *

import pygame

# Default settings (mainly to allow for the variables to be global)
KB_UP = pygame.K_w
KB_LEFT = pygame.K_a
KB_DOWN = pygame.K_s
KB_RIGHT = pygame.K_d
KB_USE = pygame.K_e

# set default keybindings
def default_keybindings():
    global KB_UP, KB_LEFT, KB_DOWN, KB_RIGHT, KB_USE
    KB_UP = pygame.K_w
    KB_LEFT = pygame.K_a
    KB_DOWN = pygame.K_s
    KB_RIGHT = pygame.K_d
    KB_USE = pygame.K_e
    return NO_PROBLEM

# reads in keybindings from properly formatted settings file
def read_keybindings(file_name):
    f = open(file_name, 'r')
    settings = f.readlines()
    f.close()
    global KB_UP, KB_LEFT, KB_DOWN, KB_RIGHT, KB_USE
    for bind in settings:
        if bind[0] == '#':
            continue
        bind = bind[:-1]        # remove newline char
        if bind[:2] == 'UP':
            KB_UP = int(bind[3:])
        elif bind[:4] == 'LEFT':
            KB_LEFT = int(bind[5:])
        elif bind[:4] == 'DOWN':
            KB_DOWN = int(bind[5:])
        elif bind[:5] == 'RIGHT':
            KB_RIGHT = int(bind[6:])
        elif bind[:3] == 'USE':
            KB_USE = int(bind[4:])
    print KB_UP
    return NO_PROBLEM

# write keybindings to a settings file
def write_keybindings(file_name):
    f = open(file_name, 'w')
    f.write('# Sentience in Space keybindings\n')
    f.write('\nUP=' + str(KB_UP))
    f.write('\nLEFT=' + str(KB_LEFT))
    f.write('\nDOWN=' + str(KB_DOWN))
    f.write('\nRIGHT=' + str(KB_RIGHT))
    f.write('\nUSE=' + str(KB_USE))
    f.write('\n')   # final newline char
    f.close()
    return NO_PROBLEM

if __name__=='__main__':
    default_keybindings()
    write_keybindings(KEYBINDINGS)
