import sys, pygame

from consts import *
from menu import *
from character import *
from npc import *
from shiplayout import *




class GameState:
    def __init__(self, screen):
        pass
        

    def update(self, event):
        pass

    def display(self):
        pass


class LoadGameState (GameState):
    def __init__(self, screen):
         #self.loadable = loadable
        pass

    def load(self):
        saved_file = open(SAVE_FILE, 'rb')
        data = saved_file.read()
        saved_file.close()

    def update(self, event):
        pass

    def display(self):
        pass



class MainMenuState (GameState):

    def __init__(self, screen):
        self.menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                            [('New Game', IN_GAME_STATE, None),
                             ('Load Game', LOAD_STATE, None),
                             ('Quit', EXIT_STATE, None)])

        self.menu.set_center(True, True)
        self.menu.set_alignment('center', 'center')
        
    def update(self, event):
        state = MAIN_MENU_STATE
        if event.type == pygame.KEYDOWN or event.type == EVENT_CHANGE_STATE:
            rectList, state = self.menu.update(event, MAIN_MENU_STATE)
        return state

    def display(self):
        self.menu.draw_buttons()


class InGameState (GameState):
    def __init__(self, screen, keybindings):
        self.user = character(CHARACTER_SPRITE_SHEET_DIR)
        self.ship = ShipLayout(TILE_SHEET_DIR, ITEM_SHEET_SMALL_DIR)
        self.ship.load(MAP_DEFAULT_DIR)
	self.keybindings = keybindings

        self.screen = screen
              
        self.character_sprite_sheet = pygame.image.load(CHARACTER_SPRITE_SHEET_DIR)
        self.tile_sheet = pygame.image.load(TILE_SHEET_DIR)
        self.npc_sheets = [pygame.image.load(file) for file in NPC_SHEETS_DIR]
        
        if self.character_sprite_sheet == None:
            return IMAGE_DOES_NOT_EXIST
        if self.tile_sheet == None:
            return IMAGE_DOES_NOT_EXIST
        for sheet in self.npc_sheets:
            if sheet == None:
                return IMAGE_DOES_NOT_EXIST

        self.tile_sheet.set_colorkey(COLOR_KEY)
        for sheet in self.npc_sheets:
            sheet.set_colorkey(COLOR_KEY)

        self.tile_sheet = self.tile_sheet.convert()

        for i in xrange(len(self.npc_sheets)):
            self.npc_sheets[i] = self.npc_sheets[i].convert()

        self.camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) # tile index, not pixel

    def update(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            return OPTIONS_MENU_STATE
        self.user.update(pygame.key.get_pressed(), self.keybindings)
        return IN_GAME_STATE

    def display(self):
        # reposition camera
        self.camera.x = self.user.getx() - SHOW_TILES_W / 2
        if self.camera.x < 0:
            self.camera.x = 0
        if (self.camera.x + 1) > MAP_WIDTH:
            self.camera.x = MAP_WIDTH - 1
        self.camera.y = self.user.gety() - SHOW_TILES_H / 2 + 1
        if self.camera.y < 0:
            self.camera.y = 0
        if (self.camera.y + 1) > MAP_HEIGHT:
            self.camera.y = MAP_HEIGHT - 1
            
        self.ship.display(self.screen, self.camera)
        self.user.display(self.screen, self.camera)


class OptionsMenuState (GameState):
    def __init__(self, screen):
        self.menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                            [('Save Game', SAVE_STATE, None),
                             ('Load Game', LOAD_STATE, None),
                             ('Modify Settings', SETTINGS_STATE, None),
                             ('Resume Game', IN_GAME_STATE, None),
                             ('Quit', EXIT_STATE, None)])
        self.menu.set_center(True, True)
        self.menu.set_alignment('center', 'center')

    def update(self, event):
        state = OPTIONS_MENU_STATE
        #if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
         #   rectList, state = self.menu.update(pygame.event.Event(EVENT_CHANGE_STATE, key = 0), OPTIONS_MENU_STATE)
        if event.type == pygame.KEYDOWN or event.type == EVENT_CHANGE_STATE:
            rectList, state = self.menu.update(event, OPTIONS_MENU_STATE)
        return state

    def display(self):
        self.menu.draw_buttons()
    
