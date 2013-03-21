# Key Bindings
# Displayed in game and stored as integers
# Different keyboards potentially have different values

import pygame

# Default settings (mainly to allow for the variables to be global)
KB_UP = pygame.K_w
KB_LEFT = pygame.K_a
KB_DOWN = pygame.K_s
KB_RIGHT = pygame.K_d
KB_USE = pygame.K_e

def default_settings():
    global KB_UP, KB_LEFT, KB_DOWN, KB_RIGHT, KB_USE
    KB_UP = pygame.K_w
    KB_LEFT = pygame.K_a
    KB_DOWN = pygame.K_s
    KB_RIGHT = pygame.K_d
    KB_USE = pygame.K_e

def read_settings(file_name):
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

def write_settings():
    f = open(KEYBINDINGS, 'w')
    f.write('# Sentience in Space keybindings\n')
    f.write('\nUP=' + str(KB_UP))
    f.write('\nLEFT=' + str(KB_LEFT))
    f.write('\nDOWN=' + str(KB_DOWN))
    f.write('\nRIGHT=' + str(KB_RIGHT))
    f.write('\nUSE=' + str(KB_USE))
    f.close()
