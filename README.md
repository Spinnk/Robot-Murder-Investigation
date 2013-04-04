Robot-Murder-Investigation

Save File Format (*.rmis)

A save file will consist of concatenations of save data in the following order:

    len(Character) | Character | len(Inventory) | Inventory | len(Ship) | Ship | NPC_count | len(NPC) | NPC | ...  | len(NPC) | NPC | SHA12 hash of previous data

    len() will be a 2 byte big-endian representation of the length of the data packet following it:
        length = 1234 (decimal) -> 0x04d2 -> '\x04\xd2'

    NPC_count will be a 2 byte big-endian representation of how many NPCs are in the save

    Character Format (4 bytes):
        x | y | clip | frame
        x     - 1 byte
        y     - 1 byte
        clip  - 1 byte
        frame - 1 byte

    Inventory Format (INVENTORY_X * INVENTORY_Y * 2 bytes):
        item | count | item | count | ...
        item  - 1 byte
        count - 1 byte

    Ship Format (MAP_X * MAP_Y * 3 bytes):
        item_x | item_y | item_type | item_x | item_y | item_type | ...
        item_x       - 1 byte
        item_y       - 1 byte
        item_type    - 1 byte

    NPC Format (Variable size):
        type | name_len | name | x | y | clip | frame
        type      - 1 byte
        name_len  - 2 bytes
        name      - name_len bytes
        x         - 1 byte
        y         - 1 byte
        clip      - 1 byte
        frame     - 1 byte
