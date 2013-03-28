# main.py
# Main program to combine everything together

import os
import random

import pygame

from consts import *
from character import *
from game import *
from inventory import *
from keybinding import *
from npc import *
from shiplayout import *

def init():
    # read keybindings
    # KB_UP, KB_LEFT, KB_DOWN, KB_RIGHT, KB_USE
    read_keybindings(KEYBINDINGS_DIR)                           # doesnt work

    # open images
    background = pygame.image.load(BACKGROUND_IMAGE_DIR)
    #character_sprite_sheet = pygame.image.load(CHARACTER_SPRITE_SHEET_DIR)
    #tile_sheet = pygame.image.load(TILE_SHEET_DIR)
    #npc_sheets = [pygame.image.load(file) for file in NPC_SHEETS_DIR]
    #inventory_sheet = pygame.image.load(INVENTORY_BACKGROUND_SHEET_DIR)
    #item_sheet_large = pygame.image.load(ITEM_SHEET_LARGE_DIR)
    #item_sheet_small = pygame.image.load(ITEM_SHEET_SMALL_DIR)

    if background == None:
        return IMAGE_DOES_NOT_EXIST

    #if inventory_sheet == None:
    #    return IMAGE_DOES_NOT_EXIST
    #if item_sheet_large == None:
    #    return IMAGE_DOES_NOT_EXIST
    #if item_sheet_small == None:
    #    return IMAGE_DOES_NOT_EXIST


#    background.set_colorkey(COLOR_KEY)
#    character_sprite_sheet.set_colorkey(COLOR_KEY)
    #tile_sheet.set_colorkey(COLOR_KEY)
    #inventory_sheet.set_colorkey(COLOR_KEY)
    #item_sheet_large.set_colorkey(COLOR_KEY)
    #item_sheet_small.set_colorkey(COLOR_KEY)


#    background = background.convert()
#    character_sprite_sheet = character_sprite_sheet.convert()
    #tile_sheet = tile_sheet.convert()
    #inventory_sheet = inventory_sprite_sheet.convert()
    #item_sheet_large = item_sheet_large.convert()
    #item_sheet_small = item_sheet_small.convert()
 

    return background #, inventory_sheet, item_sheet_large, item_sheet_small, npc_sheets

def main():
    # Set up screen #######
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)    # create the screen
    if screen == None:
        return SCREEN_DOES_NOT_EXIST

    pygame.display.set_caption(GAME_NAME)                   # give the screen a title

#    background, character_sprite_sheet, tile_sheet, inventory_sheet, item_sheet_large, item_sheet_small, npc_sheets = init_load()
    background = init()

    # Set up variables ####
    quit = False

    gameInstance = Game(screen)

    #camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) # tile index, not pixel
    #user = character()
    npcs = [NPC(random.randint(0, NPC_MAX_VALUE)) for x in xrange(NPC_COUNT)]
    npcs += [] # add special npcs
    #ship = ShipLayout()
    #ship.load(MAP_DEFAULT_DIR)

    # states are listed in consts.py
    state = MAIN_MENU_STATE

    gameInstance.update( pygame.event.Event(EVENT_CHANGE_STATE, key = 0) )

    pygame.key.set_repeat(100, 100)

    # #####################
    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if (event.type == pygame.QUIT): # exit when close window "X" is pressed
                quit = True

            gameInstance.update( event )

        # display background
        screen.blit(background, (0, 0))

        
        gameInstance.display(screen, 0)

        
            # update objects
            #user.update(pygame.key.get_pressed())
            # map.update
            # npcs.update
            # etc
        #gameInstance.update( pygame.event.Event(EVENT_CHANGE_STATE, key = 0) )
        gameInstance.display(screen, IN_GAME_STATE)
           

            # refresh screen
            # display map/world
            #ship.display(screen, tile_sheet, camera)
            # display player
            #user.display(screen, character_sprite_sheet, camera)
            # display NPCs
           # for npc in npcs:
                #npc.display(screen, camera)
            # etc

        if state == LOAD_STATE:
            pass

        elif state == EXIT_STATE:
            quit = True

        elif state == OPTIONS_MENU_STATE:
            gameInstance.display(screen, state)

        pygame.display.set_caption(GAME_NAME)
        pygame.display.flip()                       # show screen

    return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    main()
    pygame.quit()
