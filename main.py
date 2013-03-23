# main.py
# Main program to combine everything together

import os
import random

import pygame

from consts import *
from character import *
from game import *
from keybinding import *
from shiplayout import *

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
    gameInstance = Game(screen)

    ship = ShipLayout(TILE_SHEET, COLOR_KEY)
    ship.load(MAP_DEFAULT)

    state = 0   #0 = main menu
                #1 = in-game
                #2 = inventory/map/journal
                #3 = puzzle
                #4 = options menu

    # #####################
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and pygame.key.get_pressed()[pygame.K_ESCAPE]): # exit when close window "X" is pressed or escape key
                quit = True

            elif state == 0:
                state = gameInstance.update( event )
        # multi key presses
        pressed = pygame.key.get_pressed()

        # refresh screen
        # display background
        screen.blit(background, (0, 0))

        if state == 0:
            gameInstance.display(screen)

        elif state == 1:
            # reposition camera
            camera.x = user.x() - SHOW_TILES_W / 2
            if camera.x < 0:
                camera.x = 0
            if (camera.x + 1) > MAP_WIDTH:
                camera.x = MAP_WIDTH - 1
            camera.y = user.y() - SHOW_TILES_H / 2 + 1
            if camera.y < 0:
                camera.y = 0
            if (camera.y + 1) > MAP_HEIGHT:
                camera.y = MAP_HEIGHT - 1

            # update objects
            user.update(pressed)
            # map.update
            # npcs.update
            # etc

            # display map/world
            ship.display(screen, camera)
            # display player
            user.display(screen, camera)
            # display NPCs
            # etc

        pygame.display.set_caption(GAME_NAME + ' (' + str(user.x()) + ',' + str(user.y()) + ')')
        pygame.display.flip()                       # show screen

    return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    main()
    pygame.quit()
