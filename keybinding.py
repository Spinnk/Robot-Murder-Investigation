import pygame

# Default key bindings
KB_UP = pygame.K_w
KB_LEFT = pygame.K_a
KB_DOWN = pygame.K_s
KB_RIGHT = pygame.K_d
KB_USE = pygame.K_e

def default_settings():
    KB_UP = pygame.K_w
    KB_LEFT = pygame.K_a
    KB_DOWN = pygame.K_s
    KB_RIGHT_KEB = pygame.K_d
    KB_USE = pygame.K_e

def read_settings(file_name):
    f = open(file_name, 'r')
    settings = f.readlines();
    for bind in settings:
        if bind[0] == '#':
            continue
        bind = bind[:-1]        # remove newline char
        if bind[:2] == 'UP':
            KB_UP = eval('pygame.K_' + bind[3:])
        elif bind[:4] == 'LEFT':
            KB_LEFT = eval('pygame.K_' + bind[5:])
        elif bind[:5] == 'RIGHT':
            KB_RIGHT = eval('pygame.K_' + bind[6:])
        elif bind[:4] == 'DOWN':
            KB_DOWN = eval('pygame.K_' + bind[5:])
        elif bind[:3] == 'USE':
            KB_USE = eval('pygame.K_' + bind[4:])
    f.close()

# not sure how to do this
# cant just get the variable name 'pygame.K_w' from keybindings
# storing integers may not work for every platform
def write_settings():
    f = open(KEYBINDINGS, 'w')
    f.write('# Sentience in Space keybindings\n')
    f.write('\nUP=' + str(''))
    f.write('\nLEFT=' + str(''))
    f.write('\nDOWN=' + str(''))
    f.write('\nRIGHT=' + str(''))
    f.write('\nUSE=' + str(''))
    f.close()
