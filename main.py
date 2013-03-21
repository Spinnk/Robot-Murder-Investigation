# main.py
# Main program to combine everything together

import os
import random

import pygame

from consts import *
from character import *
from keybinding import *
from map import *

def main():
    # Set up screen #######
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)    # create the screen
    if screen == None:
        return SCREEN_DOES_NOT_EXIST

    pygame.display.set_caption(GAME_NAME)                   # give the screen a title
    # #####################

    read_settings(KEYBINDINGS)

    # Set up variables ####
    # they probably need ##
    # better names ########
    quit = False
    camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) # tile index, not pixel

    background = pygame.image.load(BACKGROUND_IMAGE)
    user = character(CHARACTER_SPRITE_SHEET, COLOR_KEY)

    ship = map(TILE_SHEET, COLOR_KEY)
    ship.load(MAP_DEFAULT)

    # #####################
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and pygame.key.get_pressed()[pygame.K_ESCAPE]): # exit when close window "X" is pressed or escape key
                quit = True
        # multi key presses
        pressed = pygame.key.get_pressed()

        # update objects
        user.update(pressed)
        # map.update
        # npcs.update
        # etc

        # refresh screen
        # display background
        screen.blit(background, (0, 0))
        # display map/world
        ship.display(screen, camera)
        # display player
        user.display(screen, camera)                # display user sprite
        # display NPCs
        # etc

        pygame.display.set_caption(GAME_NAME + ' (' + str(user.x()) + ',' + str(user.y()) + ')')
        pygame.display.flip()                       # show screen

    return NO_PROBLEM

if __name__=='__main__':
    os.chdir(os.path.dirname(sys.argv[0]))
    pygame.init()
    main()
    pygame.quit()
