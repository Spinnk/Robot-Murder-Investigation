#! /usr/bin/python

# The IMJState class is inherited from the GameState class. It is responsible
# for the inventory/map/journal states
#
# imjstate.py is part of Sentience in Space.
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
#---[ IMJState Class ]----------------------------------------------------------
#-------------------------------------------------------------------------------
## This class is used to handle the Inventory/Map/Journal State
#
class IMJState (GameState):
    def __init__(self, screen, keybindings, state_id):
        self.state_id = state_id
        self.inventory = None
        self.screen = screen
        self.keybindings = keybindings
        self.dropped_items = []

        # The possible states that this state may change to
        self.state_changes = [IMJ_STATE, OPTIONS_MENU_STATE, IN_GAME_STATE]

    ## ---[ update ]------------------------------------------------------------
    def update(self, event):
        self.inventory.update(self.keybindings)
        changed_state = self.checkstatechange(event)
        if changed_state in self.state_changes:
            return changed_state
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.removeitem()
        return IMJ_STATE


    ## ---[ display ]----------------------------------------------------------
    def display(self):
        try:
            self.inventory.display(self.screen)
        except AttributeError:
            print "Error: Inventory not set."
            exit(1)

    ## ---[ removeitem ]-------------------------------------------------------
    # remove the currently selected item from inventory
    def removeitem(self):
        item = self.inventory.removeitem()
        if item != None:
            self.dropped_items += [item]

    ## ---[ setinventory ]-----------------------------------------------------
    # return a list of the items that were dropped when the inventory was last
    # open
    def getdroppeditems(self):
        dropped_list = self.dropped_items
        self.dropped_items = []
        return dropped_list

    ## ---[ setinventory ]-----------------------------------------------------
    #  @param   self        The class itself, Python standard
    #  @param   inventory   The current game inventory
    #
    #  Sets the inventory to match the given inventory
    def setinventory(self, inventory):
        self.inventory = inventory

