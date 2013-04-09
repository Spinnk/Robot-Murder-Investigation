#! /usr/bin/python

# PuzzleState (an inherited class of GameState)
#
# The PuzzleState handles puzzle actions and display
#
#
# puzzlestate.py is part of Sentience in Space.
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
from puzzle import *

#-------------------------------------------------------------------------------
#---[ Puzzle Class ]------------------------------------------------------------
#-------------------------------------------------------------------------------
## This class handles the functionality for puzzle actions and display
#
class PuzzleState (GameState):
    def __init__(self, screen, keybindings, state_id):
        self.state_id = state_id
        self.current_puzzle = None


    ## ---[ update ]------------------------------------------------------------
    def update(self, event):
        self.current_puzzle.update(event)


    ## ---[ display ]----------------------------------------------------------
    def display(self):
        pass

    def setpuzzle(self, puzzle_type):
        pass





