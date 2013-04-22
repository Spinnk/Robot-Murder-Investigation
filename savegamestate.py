#! /usr/bin/python

# The SaveGameState and LoadGameState classes are subclasses of the GameState
# class which handle saving and loading the game
#
# savegamestate.py is part of Sentience in Space.
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
#---[ SaveGameState Class ]-----------------------------------------------------
#-------------------------------------------------------------------------------
## This class handles saving a game
#
class SaveGameState (GameState):

    def __init__(self, screen, state_id):
        self.state_id = state_id
        if not os.path.isdir(SAVE_DIR):
            os.mkdir(SAVE_DIR)

        # Default the save_location to SAVE_DIR/"Save 1"
        self.save_location = os.path.join(SAVE_DIR, "Save 1")
        self.num_saves = 0              # The current number of saves
        save_state = 100                # state associated with a given save
                                        # 100 represents "New Save" option

        # self.menu is a menu allowing a user to resume the game, write a new
        #  save, or overwrite an existing save (if one exists)
        self.menu = cMenu( 50, 50, 20, 5, 'vertical', 15, screen,
                           [('Back', OPTIONS_MENU_STATE, None, True),
                            ('', IN_GAME_STATE, None, False),
                            ('New Save', save_state, None, True)])
        self.menu.set_center(True, True)
        self.menu.set_alignment('center', 'center')

        # Add a button to the menu for each save file
        d = os.listdir( SAVE_DIR )
        save_state += 1
        for f in d:
            self.menu.add_buttons( [(f[:-5], save_state, None, True)])
            save_state += 1
            self.num_saves += 1
            
        if self.num_saves >= 8:
            self.menu.set_selectable('New Save', False)

    ## ---[ update ]------------------------------------------------------------
    def update(self, event):
        state = self.state_id
        if event.type == pygame.KEYDOWN or event.type == EVENT_CHANGE_STATE:
            rectList, state = self.menu.update(event, self.state_id)

        # If the new state is at least 100 then a save was requested
        if state >= 100:
            if self.num_saves >= 8:
                self.menu.set_selectable('New Save', False)
            if state == 100:
                save_name = "Save " + str(self.num_saves + 1)
                self.menu.add_buttons([( save_name, 100 + self.num_saves + 1, None, True)])
                self.num_saves += 1
                self.save_location = os.path.join(SAVE_DIR, save_name + ".rmis")
            else:
                self.save_location = os.path.join( SAVE_DIR, "Save " + str(state - 100) + ".rmis" )
        return state

    ## ---[ display ]----------------------------------------------------------
    def display(self):
        self.menu.draw_buttons()

    ## ---[ save ]----------------------------------------------------------
    #  @param   self            The class itself, Python standard
    #  @param   character       The current character status
    #  @param   inventory       The current inventory status
    #  @param   ship            The current character status
    #  @param   npc             The current npc sheet status
    #
    # saves the game status to self.save_location
    def save(self, character, inventory, journal, ship, npcs):
        try:
            c = character.save()
            i = inventory.save()
            j = journal.save()
            s = ship.save()
            ns = [npc.save() for npc in npcs]
            out = binascii.unhexlify(makehex(len(c), 4)) + c + binascii.unhexlify(makehex(len(i), 4)) + i + binascii.unhexlify(makehex(len(j), 4)) + j + binascii.unhexlify(makehex(len(s), 4)) + s + binascii.unhexlify(makehex(len(ns), 4)) + ''.join([binascii.unhexlify(makehex(len(n), 4)) + n for n in ns])
            out += hashlib.sha512(out).digest()
            f = open(self.save_location, 'wb')
            f.write(out)
            f.close()
            print "Saved game in", self.save_location
        except AttributeError as e:
            print "Error Saving Game:", e
            return None

        return self.num_saves

#-------------------------------------------------------------------------------
#---[ LoadGameState Class ]-----------------------------------------------------
#-------------------------------------------------------------------------------
## This class handles loading a game from a save file
#
class LoadGameState (GameState):

    def __init__(self, screen, state_id):
        self.state_id = state_id
        self.num_saves = 0
        load_state = 201                        # The first load_state
        self.screen = screen                    # A copy of the screen

        # self.menu provides the interface for loading a game
        self.menu = cMenu( 50, 50, 20, 5, 'vertical', 15, self.screen,
                           [('Back', MAIN_MENU_STATE, None, True),
                            ('', IN_GAME_STATE, None, False)])
        self.menu.set_center(True, True)
        self.menu.set_alignment('center', 'center')

        # Iterate through the save directory and add a menu button for each
        #  saved game
        d = os.listdir( SAVE_DIR )
        for f in d:
            self.menu.add_buttons( [(f[:-5], load_state, None, True)])
            load_state += 1
            self.num_saves += 1
            
    ## ---[ update ]-----------------------------------------------------------
    # Inputs the state where "Load Game" was called and sets "Back" to go to
    # that state
    def calledfrom(self, state):
        # only allow "Back" to return to a menu state
        if state in [MAIN_MENU_STATE, OPTIONS_MENU_STATE]:
            self.menu.set_state( 'Back', state )


    ## ---[ update ]------------------------------------------------------------
    def update(self, event):
        state = self.state_id
        if event.type == pygame.KEYDOWN or event.type == EVENT_CHANGE_STATE:
            rectList, state = self.menu.update(event, self.state_id)
        return state

    ## ---[ display ]----------------------------------------------------------
    def display(self):
        #self.setmenu()
        self.menu.draw_buttons()

    ## ---[ updatemenu ]-------------------------------------------------------
    #
    # This updates the load menu to reflect any changes in the save directory
    def updatemenu(self, new_num_saves):
        # Return if the number of saves has not changed
        if self.num_saves == new_num_saves:
            return

        # remove all "saved game" buttons
        self.menu.remove_end( self.num_saves )

        load_state = 201                # The first save_state

        # Iterate through the save directory and add a menu button for each
        #  saved game
        d = os.listdir( SAVE_DIR )
        for f in d:
            self.menu.add_buttons( [(f[:-5], load_state, None, True)])
            load_state += 1

        self.num_saves = new_num_saves


    ## ---[ load ]------------------------------------------------------------
    #  @param   self            The class itself, Python standard
    #  @param   save_location   A string representing the save location
    #
    # loads the game from a given save location
    def load(self, save_name):
        save_location = os.path.join(SAVE_DIR, save_name)
        try:
            f = open(save_location, 'rb')
            data = f.read()
            f.close()
        except IOError:
            print "Error opening file: " + save_name
            return
        checksum = data[-64:]
        data = data[:-64]
        if hashlib.sha512(data).digest() != checksum:
            return CHECKSUMS_DO_NOT_MATCH, None, None, None
        c_len = int(binascii.hexlify(data[:2]), 16); data = data[2:]
        c = Character(); c.load(data[:c_len]); data = data[c_len:]
        i_len = int(binascii.hexlify(data[:2]), 16); data = data[2:]
        i = Inventory(); i.load(data[:i_len]); data = data[i_len:]
        j_len = int(binascii.hexlify(data[:2]), 16); data = data[2:]
        j = Journal(); j.load(data[:j_len]); data = data[j_len:]
        s_len = int(binascii.hexlify(data[:2]), 16); data = data[2:]
        s = ShipLayout(); s.load(data[:s_len]); data = data[s_len:]
        npc_count = int(binascii.hexlify(data[:2]), 16); data = data[2:]
        ns = []
        for x in xrange(npc_count):
            n_len = int(binascii.hexlify(data[:2]), 16); data = data[2:]
            n = NPC(0, 0, 0); n.load(data[:n_len]); ns += [n]; data = data[n_len:]
        if len(data):
            return INCORRECT_DATA_LENGTH, None, None, None

        print "Loaded from " + save_name
        j = Journal()
        return c, i, j, s, ns
