import pygame

# Default key bindings
UP_KB = pygame.K_w
LEFT_KB = pygame.K_a
DOWN_KB = pygame.K_s
RIGHT_KB = pygame.K_d
USE_KB = pygame.K_e

def default_settings():
    UP_KB = pygame.K_w
    LEFT_KB = pygame.K_a
    DOWN_KB = pygame.K_s
    RIGHT_KEB = pygame.K_d
    USE_KB = pygame.K_e

def read_settings(file_name):
    f = open(file_name, 'r')
    settings = f.readlines();
    for bind in settings:
        if bind[0] == '#':
            continue
        bind = bind[:-1]        # remove newline char
        if bind[:2] == 'UP':
            bind = 'UP = pygame.K_' + bind[3:]
        elif bind[:4] == 'LEFT':
            bind = 'LEFT = pygame.K_' + bind[5:]
        elif bind[:5] == 'RIGHT':
            bind = 'RIGHT = pygame.K_' + bind[6:]
        elif bind[:4] == 'DOWN':
            bind = 'DOWN = pygame.K_' + bind[5:]
        elif bind[:3] == 'USE':
            bind = 'DOWN = pygame.K_' + bind[4:]
        eval(bind)
    return
