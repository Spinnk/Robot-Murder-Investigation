# main.py
# Main program to combine everything together

import os
import random

import pygame

from consts import *
from game import *
from keybinding import *


def main():
    # Set up screen #######
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)    # create the screen
    if screen == None:
        return SCREEN_DOES_NOT_EXIST

    pygame.display.set_caption(GAME_NAME)                   # give the screen a title

    # Set up variables ####
    quit = False
    clock = pygame.time.Clock()

    background = pygame.image.load(BACKGROUND_IMAGE_DIR)

    keybindings = default_keybindings()
    keybindings = read_keybindings(KEYBINDINGS_DIR)
    gameInstance = Game(screen, keybindings)

    #camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) # tile index, not pixel
    #user = character()
    #npcs = [NPC(random.randint(0, NPC_MAX_VALUE)) for x in xrange(NPC_COUNT)]
    #npcs += [] # add special npcs
    #ship = ShipLayout()
    #ship.load(MAP_DEFAULT_DIR)


    gameInstance.update( pygame.event.Event(EVENT_CHANGE_STATE, key = 0) )

    pygame.key.set_repeat(100, 100)

    # #####################
    while not(quit):
        clock.tick(FPS)
        
        # single key presses
        for event in pygame.event.get():
            if (event.type == pygame.QUIT): # exit when close window "X" is pressed
                quit = True

            gameInstance.update( event )

        # display background
        screen.blit(background, (0, 0))

        
        gameInstance.display(screen, 0)

        gameInstance.display(screen, IN_GAME_STATE)
           
        pygame.display.set_caption(GAME_NAME)
        pygame.display.flip()                       # show screen

    return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    main()
    pygame.quit()
