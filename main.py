# main.py
# Main program to combine everything together

import os
import random

import pygame

from consts import *
from character import *

def main():
    # Set up screen #######
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)    # create the screen
    if screen == None:
        return SCREEN_DOES_NOT_EXIST

    pygame.display.set_caption('Game')               # give the screen a titple
    # #####################

    # Set up variables ####
    quit = False
    camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    user = character(CHARACTER_SPRITE_SHEET)

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

        # refresh screen
        screen.fill((0xff, 0xff, 0xff))             # fill screen with white
        user.display(screen, camera)                # display user sprite
        pygame.display.set_caption('(' + str(user.x()) + ',' + str(user.y()) + ')')
        pygame.display.flip()                       # show screen

    return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    main()
    pygame.quit()
