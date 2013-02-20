import pygame

# default window dimensions
WIDTH = 640
HEIGHT = 480

def resize_screen(screen):
    # get allowed resolutions
    modes = pygame.display.list_modes()
    modes.sort()
    '''
    display modes
    let user chose
    change mode
    '''
    return screen


def main():
    # Set up screen #######
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)    # create the screen
    pygame.display.set_caption('Game')                    # give the screen a titple
    screen.fill((0xff, 0xff, 0xff))                     # fill screen with white
    pygame.display.flip()                            # show screen
    # #####################

    while True:
        # single key presses
        for event in pygame.event.get():
            if (event.type == pygame.QUIT): # exit when close window "X" is pressed
                return

        # multikey presses
        pressed = pygame.key.get_pressed()
        if key[pygame.K_A] & key[pygame.K_B]:
            pass


if __name__=="__main__":
    pygame.init()
    main()
