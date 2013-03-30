# save.py
# This file should not be stand-alone
# The functions should be moved into some other class after they are completed

'''
Sentience in Space 
	Save File Format (*.rmis)

	A save file will consist of concatenations of save data in the following order:

		len(Character) | Character | len(Inventory) | Inventory | len(Ship) | Ship | NPC_count | len(NPC) | NPC | ...  | len(NPC) | NPC | SHA12 hash of previous data

		len() will be a 2 byte big-endian representation of the length of the data packet following it:
			length = 1234 (decimal) -> 0x04d2 -> '\x04\xd2'

		NPC_count will be a 2 byte big-endian representation of how many NPCs are in the save

        Character Format:
            x | y | clip | frame
            x     - 1 byte
            y     - 1 byte
            clip  - 1 byte
            frame - 1 byte

        Inventory Format: 
            item | count | item | count | ...
            item  - 1 byte
            count - 1 byte

        Ship Format:
            item_x | item_y | item_type | item_x | item_y | item_type | ...
            item_x       - 1 byte
            item_y       - 1 byte
            item_type    - 1 byte

        NPC Format:
            type | name_len | name | x | y | clip | frame
            type      - 1 byte
            name_len  - 2 bytes
            name      - name_len bytes
            x         - 1 byte
            y         - 1 byte
            clip      - 1 byte
            frame     - 1 byte
'''

import hashlib

from consts import *
from character import *
from inventory import *
from shiplayout import *
from npc import *

def load(save_location):
	f = open(save_location, 'rb')
	data = f.read()
	f.close()
	checksum = data[-64:]
	data = data[:-64]
	if hashlib.sha512(data).digest() != checksum:
		return CHECKSUMS_DO_NOT_MATCH, None, None, None
	c_len = int(binascii.hexlify(data[:2]), 16); data = data[2:]
	c = Character(CHARACTER_SPRITE_SHEET_DIR); c.load(data[:c_len]); data = data[c_len:]
	i_len = int(binascii.hexlify(data[:2]), 16); data = data[2:]
	i = Inventory(INVENTORY_BACKGROUND_SHEET_DIR, ITEM_SHEET_SMALL_DIR, ITEM_SHEET_LARGE_DIR, ITEM_BOX_DIR, INVENTORY_BUTTONS_DIR); i.load(data[:i_len]); data = data[i_len:]
	s_len = int(binascii.hexlify(data[:2]), 16); data = data[2:]
	s = ShipLayout(TILE_SHEET_DIR, ITEM_SHEET_SMALL_DIR); s.load(data[:s_len]); data = data[s_len:]
	npc_count = int(binascii.hexlify(data[:2]), 16); data = data[2:]

	ns = []
	for x in xrange(npc_count):
		n_len = int(binascii.hexlify(data[:2]), 16); data = data[2:]
		n = NPC(); n.load(data[:n_len]); data = data[n_len:]
	if len(data):
		return INCORRECT_DATA_LENGTH, None, None, None
	return c, i, s, ns

def save(save_location, character, inventory, ship, npcs):
	c = character.save()
	i = inventory.save()
	s = ship.save()
	ns = [npc.save() for npc in npcs]
	out = binascii.unhexlify(makehex(len(c), 4)) + c + binascii.unhexlify(makehex(len(i), 4)) + i + binascii.unhexlify(makehex(len(s), 4)) + s + binascii.unhexlify(makehex(len(ns), 4)) + ''.join([binascii.unhexlify(makehex(len(n), 4)) + n for n in ns])
	out += hashlib.sha512(out).digest()
	f = open(save_location, 'wb')
	f.write(out)
	f.close()
	return NO_PROBLEM

if __name__=='__main__':
	pygame.init()
	pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	c = Character(CHARACTER_SPRITE_SHEET_DIR)
	i = Inventory(INVENTORY_BACKGROUND_SHEET_DIR, ITEM_SHEET_SMALL_DIR, ITEM_SHEET_LARGE_DIR, ITEM_BOX_DIR, INVENTORY_BUTTONS_DIR)
	s = ShipLayout(TILE_SHEET_DIR, ITEM_SHEET_SMALL_DIR)
	ns = [NPC() for x in xrange(3)]
	save(os.path.join(SAVE_DIR, "empty save.rmis"), c, i, s, ns)
	load(os.path.join(SAVE_DIR, "empty save.rmis"))
	pygame.quit()