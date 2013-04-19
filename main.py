#! /usr/bin/python

# Sentience in Space
# Copyright (C) 2013  T.J. Callahan
# Copyright (C) 2013  Jonathan Cann
# Copyright (C) 2013  Geo Kersey
# Copyright (C) 2013  Jason Lee
# Copyright (C) 2013  Kate Spinney
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame

from consts import *
from game import *

# Set up environment
def setenvi():
    # Center window
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Change working directory
    #os.chdir(CWD)           # unnecessary

    # Set key repeat to 100 ms
    pygame.key.set_repeat(100, 100)

    # Turn off mouse events to reduce overhead
    pygame.event.set_blocked(pygame.MOUSEMOTION)

    # Set screen brightness
    pygame.display.set_gamma(SCREEN_BRIGHTNESS)

    # Set sound volume
    pygame.mixer.music.set_volume(SOUND_VOLUME)

def main():
    # Set up screen #######
    # create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    # make sure screen was created
    if screen == None:
        return SCREEN_DOES_NOT_EXIST

    # give the screen a title
    pygame.display.set_caption(GAME_NAME)

    # load and play background music
    pygame.mixer.music.load(SOUND_DIRS[0])
    pygame.mixer.music.set_volume(SOUND_VOLUME)
    pygame.mixer.music.play()

    # Set up variables ####
    quit = False

    background = pygame.image.load(BACKGROUND_IMAGE_DIR)
    gameInstance = Game(screen, KEYBINDINGS)
    gameInstance.update( pygame.event.Event(EVENT_CHANGE_STATE, key = 0) )
    # #####################

    # Set key repeat to 100 ms
    pygame.key.set_repeat(100, 100)

    # Turn off mouse events to reduce overhead
    pygame.event.set_blocked(pygame.MOUSEMOTION)


    while not(quit):
        # single key presses
        for event in pygame.event.get():
            if (event.type == pygame.QUIT): # exit when close window "X" is pressed
                quit = True

            # update game
            gameInstance.update( event )

        # keep background music playing
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(SOUND_DIR[0])
            pygame.mixer.music.set_volume(SOUND_VOLUME)
            pygame.mixer.music.play()

        # display background
        screen.blit(background, (0, 0))

        # display game
        gameInstance.display()

        # bring screen changes up
        pygame.display.flip()

        # cap framerate
        pygame.time.Clock().tick(FPS)

    # end music
    pygame.mixer.music.stop()

    return NO_PROBLEM

if __name__=='__main__':
    pygame.init()
    setenvi()
    main()
    pygame.quit()
