#! /usr/bin/python

# InGameState (an inherited class of GameState)
#
# The InGameState class provides an instance of GameState which handles
# in-game input and display
#
#
# ingamestate.py is part of Sentience in Space.
#
# Sentience in Space is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sentience in Space is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sentience in Space.  If not, see <http://www.gnu.org/licenses/>.

from gamestate import *

#-------------------------------------------------------------------------------
#---[ InGameState Class ]-------------------------------------------------------
#-------------------------------------------------------------------------------
## This class handles the functionality for in-game actions and display
#
class InGameState (GameState):
    # initialize with only map
    def __init__(self, screen, keybindings, state_id):
        self.state_id = state_id
        self.in_dialogue = None   # npc the user is currently talking to

        # load images, check if they exist, and apply colorkey
        self.character_sprite_sheet = pygame.image.load(CHARACTER_SPRITE_SHEET_DIR)
        if self.character_sprite_sheet == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        # don't do set_colorkey and convert on character image due to background already being transparent

        self.tile_sheet = pygame.image.load(TILE_SHEET_DIR)
        if self.tile_sheet == None:
            sys.exit(IMAGE_DOES_NOT_EXIST)
        self.tile_sheet.set_colorkey(COLOR_KEY)
        self.tile_sheet = self.tile_sheet.convert()

        # flags
        self.flags = None

        # set system stuff
        self.screen = screen
        self.keybindings = keybindings

        # create default objects
        self.user = Character()
        self.user.setx(2)
        self.user.sety(2)
        self.inventory = Inventory()
        self.journal = Journal()
        self.journal.addentry(3)
        self.ship = ShipLayout()
        self.ship.loadmap(MAP_DEFAULT_DIR)

        # temporary test NPC
        self.npcs = [NPC(0, 3, 6)]

        # temporary test items
        self.ship.additem([6,7], 1)
        self.ship.additem([1,5], 2)
        self.ship.additem([3,3], 3)

        self.camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) # tile index, not pixel

        # The possible states that this state may change to
        self.state_changes = [INVENTORY_STATE,
                              MAP_STATE,
                              JOURNAL_STATE,
                              OPTIONS_MENU_STATE,
                              PUZZLE_STATE]

    ## ---[ update ]------------------------------------------------------------
    def update(self, event):        
        if self.checkstatechange(event) in self.state_changes:
            return self.checkstatechange(event)
        if self.in_dialogue:
            if event.type == pygame.KEYDOWN and event.key == self.keybindings[KB_ENTER]:
                self.in_dialogue.rundialogue(0)
                self.in_dialogue = None
            return self.state_id
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.removeitem()
            # Attempt to talk to a nearby NPC if "enter" key is pressed
            elif event.key == self.keybindings[KB_ENTER]:
                self.in_dialogue = self.attempt_dialogue()
            else:
                grid = self.ship.getsurrounding(self.user.getx(), self.user.gety() + 1)
                self.user.update(event, grid)
        return IN_GAME_STATE

    ## ---[ display ]----------------------------------------------------------
    def display(self):
        # reposition camera to center around character
        # limit camera to edge of map so character will be
        # not center for those cases
        self.camera.x = self.user.getx() - TILE_SHOW_W / 2
        if self.camera.x < 0:
            self.camera.x = 0
        if (self.camera.x + TILE_SHOW_W) > MAP_WIDTH:
            self.camera.x = MAP_WIDTH - TILE_SHOW_W
        self.camera.y = self.user.gety() - TILE_SHOW_H / 2 + 1
        if self.camera.y < 0:
            self.camera.y = 0
        if (self.camera.y + TILE_SHOW_H + 1) > MAP_HEIGHT:
            self.camera.y = MAP_HEIGHT - TILE_SHOW_H - 1
        self.ship.display(self.screen, self.camera)
        for npc in self.npcs:
            npc.display(self.screen, self.camera)
        self.user.display(self.screen, self.camera)

    ## ---[ load ]------------------------------------------------------------
    # Sets the user, inventory, ship, and npcs according to the input
    def load(self, character, inventory, ship_layout, npcs):
        self.user = character
        self.inventory = inventory
        self.ship.setitems(ship_layout.getitems())
        self.npcs = npcs

    ## ---[ save ]------------------------------------------------------------
    # Returns a copy of the current user, inventory, ship, and npcs status
    def save(self):
        return self.user, self.inventory, self.journal, self.ship, self.npcs

    # modify items on floor
    # add items to character location
    def additems(self, items):
        for item in items:
            self.ship.additem([self.user.getx(), self.user.gety() + 1], item)

    # remove single item from character location and add to inventory
    def removeitem(self):
        item = self.ship.removeitem([self.user.getx(), self.user.gety() + 1])
        if item != None:
            if item == 1:
                self.inventory.additem(1, 1)
            else:
                self.inventory.additem(item)


    # set all floor items
    def setitemsonfloor(self, itemsonfloor):
        self.items = itemsonfloor

    # remove all floor items
    def removeitemsonfloor(self):
        self.items = []

    # get copy of items on floor
    def getitemsonfloor(self):
        return self.items

    # get a copy of the inventory
    def getinventory(self):
        return self.inventory

    def getjournal(self):
        return self.journal

    def getcharacterposition(self):
        return self.user.getx(), self.user.gety()

    # Find if there is a nearby NPC,
    # if there is, attempt to talk to it
    def attempt_dialogue(self):
        x, y = self.user.getx(), self.user.gety() + 1
        for npc in self.npcs:
            if (abs(npc.getx() - x) == 1 and npc.gety() == y) or (abs(npc.gety() - y) == 1 and npc.getx() == x ):
                npc.rundialogue(1)
                return npc




























