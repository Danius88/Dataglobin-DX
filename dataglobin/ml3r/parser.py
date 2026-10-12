import struct
from dataglobin.data import Item

def read_string(chunk: bytes, start: int, string_size: int) -> str:
    return chunk[start:start + string_size].split(b"\x00", 1)[0].decode("utf-8", errors="ignore")

def parse_db_items(data: bytes) -> list[Item]:
    RECORD_SIZE = 0x6C
    STRING_SIZE = 0x18
    BASE = STRING_SIZE * 4
    items = []
    for item_id, offset in enumerate(range(0, len(data), RECORD_SIZE)):
        chunk = data[offset:offset + RECORD_SIZE]
        if len(chunk) < RECORD_SIZE:
            break
        item = Item()
        #item.raw_data = chunk
        item.id = item_id + 0x1000
        item.label_name = read_string(chunk, 0x00, STRING_SIZE)
        item.label_nams = read_string(chunk, 0x18, STRING_SIZE)
        item.label_desc = read_string(chunk, 0x30, STRING_SIZE)
        item.label_full = read_string(chunk, 0x48, STRING_SIZE)
        item.sprite = struct.unpack_from("<H", chunk, BASE + 0x0)[0]
        item.price = struct.unpack_from("<H", chunk, BASE + 0x4)[0]
        item.effect_id = struct.unpack_from("<H", chunk, BASE + 0x6)[0]
        item.effect_param = struct.unpack_from("<H", chunk, BASE + 0x8)[0]
        item.flags1 = [bool((chunk[BASE + 0xA] >> bit) & 1) for bit in range(8)]
        item.flags2 = [bool((chunk[BASE + 0xB] >> bit) & 1) for bit in range(8)]
        items.append(item)
    return items