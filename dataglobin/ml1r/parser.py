import struct
from dataglobin.data import Item

def read_string(chunk: bytes, start: int, string_size: int) -> str:
    return chunk[start:start + string_size].split(b"\x00", 1)[0].decode("utf-8", errors="ignore")

def write_string(chunk: bytearray, offset: int, value: str, string_size: int):
    encoded = value.encode("utf-8")[:string_size - 1]
    chunk[offset:offset + string_size] = (encoded + b"\x00" * (string_size - len(encoded)))

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
        item.sprite = struct.unpack_from("<I", chunk, BASE + 0x0)[0]
        item.price = struct.unpack_from("<H", chunk, BASE + 0x4)[0]
        item.effect_id = struct.unpack_from("<H", chunk, BASE + 0x6)[0]
        item.effect_param1 = struct.unpack_from("<H", chunk, BASE + 0x8)[0]
        item.unk1 = struct.unpack_from("<B", chunk, BASE + 0xA)[0]
        item.flags1 = [bool((chunk[BASE + 0xB] >> bit) & 1) for bit in range(8)]
        items.append(item)
    return items

def repack_db_items(items: list[Item]) -> bytes:
    RECORD_SIZE = 0x6C
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
        struct.pack_into("<H", chunk, BASE + 0x6, item.effect_id)
        struct.pack_into("<H", chunk, BASE + 0x8, item.effect_param1)
        struct.pack_into("<B", chunk, BASE + 0xA, item.unk1)
        chunk[BASE + 0xB] = sum((1 << bit) for bit, flag in enumerate(item.flags1) if flag)
        data.extend(chunk)
    return bytes(data)

def parse_db_effects(data: bytes) -> list[str]:
    STRING_SIZE = 0x18
    return [
        read_string(data, offset, STRING_SIZE)
        for offset in range(0, len(data), STRING_SIZE)
        if len(data[offset:offset + STRING_SIZE]) == STRING_SIZE
    ]

def repack_db_effects(strings: list[str]) -> bytes:
    STRING_SIZE = 0x18
    data = bytearray(len(strings) * STRING_SIZE)
    for index, value in enumerate(strings):
        write_string(data, index * STRING_SIZE, value, STRING_SIZE)
    return bytes(data)