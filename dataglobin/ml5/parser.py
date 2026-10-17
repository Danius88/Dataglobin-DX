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
        #item.raw_data = chunk
        item.id = item_id + 0x1000
        item.label_name = read_string(chunk, 0x00, STRING_SIZE)
        item.label_nams = read_string(chunk, 0x18, STRING_SIZE)
        item.label_desc = read_string(chunk, 0x30, STRING_SIZE)
        item.label_full = read_string(chunk, 0x48, STRING_SIZE)
        item.sprite = struct.unpack_from("<I", chunk, BASE + 0x0)[0]
        item.price = struct.unpack_from("<H", chunk, BASE + 0x4)[0]
        item.effect_id = struct.unpack_from("<H", chunk, BASE + 0x8)[0]
        item.effect_param1 = struct.unpack_from("<H", chunk, BASE + 0xA)[0]
        item.flags1 = [bool((chunk[BASE + 0xC] >> bit) & 1) for bit in range(8)]
        item.flags2 = [bool((chunk[BASE + 0xD] >> bit) & 1) for bit in range(8)]
        item.unk1 = struct.unpack_from("<H", chunk, BASE + 0xE)[0]
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
        struct.pack_into("<H", chunk, BASE + 0x4, item.price)
        struct.pack_into("<H", chunk, BASE + 0x8, item.effect_id)
        struct.pack_into("<H", chunk, BASE + 0xA, item.effect_param1)
        chunk[BASE + 0xC] = sum((1 << bit) for bit, flag in enumerate(item.flags1) if flag)
        chunk[BASE + 0xD] = sum((1 << bit) for bit, flag in enumerate(item.flags2) if flag)
        struct.pack_into("<H", chunk, BASE + 0xE, item.unk1)
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
        #item.raw_data = chunk
        item.id = item_id + 0x2000
        item.label_name = read_string(chunk, 0x00, STRING_SIZE)
        item.label_nams = read_string(chunk, 0x18, STRING_SIZE)
        item.label_desc = read_string(chunk, 0x30, STRING_SIZE)
        item.label_full = read_string(chunk, 0x48, STRING_SIZE)
        item.sprite = struct.unpack_from("<I", chunk, BASE + 0x0)[0]
        item.price = struct.unpack_from("<H", chunk, BASE + 0x4)[0]
        items.append(item)
    return items