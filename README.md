Sentience in Space

Copyright (C) 2013  T.J. Callahan
Copyright (C) 2013  Jonathan Cann
Copyright (C) 2013  Geo Kersey
Copyright (C) 2013  Jason Lee
Copyright (C) 2013  Kate Spinney

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Requirements:
    System that is supported by Python 2.7.x and pygame 1.9.1
    Python 2.7.x (http://www.python.org/)
    pygame 1.9.1 (http://www.pygame.org/)

Usage:
    Run main.py

Additional Information (Change Logs, Bugs, etc):
    https://github.com/Spinnk/Robot-Murder-Investigation.git
    http://bestvideogame.wikidot.com/

======================================================================

Sentience in Space Specialized File/Data Formats:

    Saves (*.rmis)

        A save file will consist of concatenations of save data (extended ASCII character strings) in the following order:

            len(Character) | Character | len(Inventory) | Inventory | len(Journal) | Journal | len(Ship) | Ship | NPC_count | len(NPC) | NPC | ...  | len(NPC) | NPC | SHA12 hash of previous data

            len() will be a 2 byte big-endian representation of the length of the data packet following it:
                length = 1234 (decimal) -> 0x04d2 -> '\x04\xd2'

            NPC_count will be a 2 byte big-endian representation of how many NPCs are in the save

            Character Format (3 bytes):
                x | y | clip
                x          - 1 byte
                y          - 1 byte
                clip       - 1 byte

            Inventory Format (3 bytes * INVENTORY_X * INVENTORY_Y):
                item | count | special | item | count | special | ...
                item       - 1 byte
                count      - 1 byte
                special    - 1 byte

            Journal Format (2 bytes * count)
                has_read | entry | has_read | entry | ...
                has_read   - 1 byte
                entry      - 1 byte

            Ship Format (3 bytes * MAP_X * MAP_Y):
                item_x | item_y
                item_x     - 1 byte
                item_y     - 1 byte
                item_type  - 1 byte

            NPC Format (Variable size * count):
                type | name_len | name | x | y | clip
                type       - 1 byte
                name_len   - 2 bytes
                name       - name_len bytes
                x          - 1 byte
                y          - 1 byte
                clip       - 1 byte

    Map (map.txt)

        A series of (extended) ASCII characters representing the tiles. The file will be MAP_WIDTH * MAP_HEIGHT bytes large.
        The map is written row by row.

    Journal (journal entries.txt)

        A Journal Entry is contained within 2 lines based on OpenPGP Armor. All other lines in the file are considered comments.
        The order of entries determines the index of the entries within the program.

        -----BEGIN ENTRY-----
        TITLE LINE
        TEXT LINE 1
        TEXT LINE 2
        -----END ENTRY-----

    Puzzle Map (puzzle map.txt)

        A series of integers in a grid representing the default configuration of a puzzle.

    Dialogue (dialogue_n_.txt, _n_ is an integer):

        Unknown
