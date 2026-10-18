import struct
from dataglobin.data import Item

def read_string(chunk: bytes, start: int, string_size: int) -> str:
    return chunk[start:start + string_size].split(b"\x00", 1)[0].decode("utf-8", errors="ignore")

def write_string(chunk: bytearray, offset: int, value: str, string_size: int):
    encoded = value.encode("utf-8")[:string_size - 1]
    chunk[offset:offset + string_size] = (encoded + b"\x00" * (string_size - len(encoded)))

def parse_db_items(data: bytes) -> list[Item]:
    RECORD_SIZE = 0x70
    STRING_SIZE = 0x18
    BASE = STRING_SIZE * 4
    items = []
    for item_id, offset in enumerate(range(0, len(data), RECORD_SIZE)):
        chunk = data[offset:offset + RECORD_SIZE]
        if len(chunk) < RECORD_SIZE:
            break
        item = Item()
        item.raw_data = chunk
        item.id = item_id + 0x1000
        item.label_name = read_string(chunk, 0x00, STRING_SIZE)
        item.label_nams = read_string(chunk, 0x18, STRING_SIZE)
        item.label_desc = read_string(chunk, 0x30, STRING_SIZE)
        item.label_full = read_string(chunk, 0x48, STRING_SIZE)

        item.sprite = struct.unpack_from("<I", chunk, BASE + 0x0)[0]
        item.price = struct.unpack_from("<I", chunk, BASE + 0x4)[0]

        item.effect_id = struct.unpack_from("<H", chunk, BASE + 0x8)[0]
        item.effect_param1 = struct.unpack_from("<h", chunk, BASE + 0xA)[0]

        item.use_menu = bool((chunk[BASE + 0xC] >> 0) & 1)
        item.use_battle = bool((chunk[BASE + 0xC] >> 1) & 1)
        item.use_arcade = bool((chunk[BASE + 0xC] >> 2) & 1)
        item.user = ((chunk[BASE + 0xC] >> 3) & 1) | (((chunk[BASE + 0xC] >> 4) & 1) << 1)
        item.target_enemy = bool((chunk[BASE + 0xC] >> 5) & 1)
        item.target_multi = bool((chunk[BASE + 0xC] >> 6) & 1)
        item.target_back = bool((chunk[BASE + 0xC] >> 7) & 1)

        item.is_mushroom = bool((chunk[BASE + 0xD] >> 0) & 1)
        item.is_bean = bool((chunk[BASE + 0xD] >> 1) & 1)
        item.use_condition = (chunk[BASE + 0xD] >> 2) & 0x0F

        items.append(item)
    return items

def repack_db_items(items: list[Item]) -> bytes:
    RECORD_SIZE = 0x70
    STRING_SIZE = 0x18
    BASE = STRING_SIZE * 4
    data = bytearray()
    for item in items:
        chunk = bytearray(item.raw_data[:RECORD_SIZE])

        write_string(chunk, 0x00, item.label_name, STRING_SIZE)
        write_string(chunk, 0x18, item.label_nams, STRING_SIZE)
        write_string(chunk, 0x30, item.label_desc, STRING_SIZE)
        write_string(chunk, 0x48, item.label_full, STRING_SIZE)

        struct.pack_into("<I", chunk, BASE + 0x0, item.sprite)
        struct.pack_into("<I", chunk, BASE + 0x4, item.price)

        struct.pack_into("<H", chunk, BASE + 0x8, item.effect_id)
        struct.pack_into("<h", chunk, BASE + 0xA, item.effect_param1)

        chunk[BASE + 0xC] = (chunk[BASE + 0xC] & ~0x01) | int(item.use_menu)
        chunk[BASE + 0xC] = (chunk[BASE + 0xC] & ~0x02) | (int(item.use_battle) << 1)
        chunk[BASE + 0xC] = (chunk[BASE + 0xC] & ~0x04) | (int(item.use_arcade) << 2)
        chunk[BASE + 0xC] = (chunk[BASE + 0xC] & ~0x18) | ((item.user & 0x03) << 3)
        chunk[BASE + 0xC] = (chunk[BASE + 0xC] & ~0x20) | (int(item.target_enemy) << 5)
        chunk[BASE + 0xC] = (chunk[BASE + 0xC] & ~0x40) | (int(item.target_multi) << 6)
        chunk[BASE + 0xC] = (chunk[BASE + 0xC] & ~0x80) | (int(item.target_back) << 7)

        chunk[BASE + 0xD] = (chunk[BASE + 0xD] & ~0x01) | int(item.is_mushroom)
        chunk[BASE + 0xD] = (chunk[BASE + 0xD] & ~0x02) | (int(item.is_bean) << 1)
        chunk[BASE + 0xD] = (chunk[BASE + 0xD] & ~0x3C) | ((item.use_condition & 0x0F) << 2)

        data.extend(chunk)
    return bytes(data)

def parse_db_cards(data: bytes) -> list[Item]:
    RECORD_SIZE = 0x78
    STRING_SIZE = 0x18
    BASE = STRING_SIZE * 4
    items = []
    for item_id, offset in enumerate(range(0, len(data), RECORD_SIZE)):
        chunk = data[offset:offset + RECORD_SIZE]
        if len(chunk) < RECORD_SIZE:
            break
        item = Item()
        item.raw_data = chunk
        item.id = item_id + 0x2000
        item.label_name = read_string(chunk, 0x00, STRING_SIZE)
        item.label_nams = read_string(chunk, 0x18, STRING_SIZE)
        item.label_desc = read_string(chunk, 0x30, STRING_SIZE)
        item.label_full = read_string(chunk, 0x48, STRING_SIZE)
        item.sprite = struct.unpack_from("<I", chunk, BASE + 0x0)[0]
        item.price = struct.unpack_from("<H", chunk, BASE + 0x4)[0]
        items.append(item)
    return items