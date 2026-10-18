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
        item.raw_data = chunk
        item.id = item_id + 0x1000
        
        item.label_name = read_string(chunk, 0x00, STRING_SIZE)
        item.label_nams = read_string(chunk, 0x18, STRING_SIZE)
        item.label_desc = read_string(chunk, 0x30, STRING_SIZE)
        item.label_full = read_string(chunk, 0x48, STRING_SIZE)

        item.sprite = struct.unpack_from("<I", chunk, BASE + 0x0)[0]
        item.price = struct.unpack_from("<H", chunk, BASE + 0x4)[0]

        item.effect_id = struct.unpack_from("<H", chunk, BASE + 0x6)[0]
        item.effect_param1 = struct.unpack_from("<h", chunk, BASE + 0x8)[0]
        
        item.unk1 = struct.unpack_from("<B", chunk, BASE + 0xA)[0]

        item.use_condition = chunk[BASE + 0xB] & 0x0F
        item.use_menu = bool((chunk[BASE + 0xB] >> 5) & 1)
        item.mushroom_pocket = bool((chunk[BASE + 0xB] >> 6) & 1)
        item.target_multi = bool((chunk[BASE + 0xB] >> 7) & 1)
        
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
        struct.pack_into("<h", chunk, BASE + 0x8, item.effect_param1)

        struct.pack_into("<B", chunk, BASE + 0xA, item.unk1)

        chunk[BASE + 0xB] = (chunk[BASE + 0xB] & 0xF0) | (item.use_condition & 0x0F)
        chunk[BASE + 0xB] = (chunk[BASE + 0xB] & ~(1 << 5)) | (int(item.use_menu) << 5)
        chunk[BASE + 0xB] = (chunk[BASE + 0xB] & ~(1 << 6)) | (int(item.mushroom_pocket) << 6)
        chunk[BASE + 0xB] = (chunk[BASE + 0xB] & ~(1 << 7)) | (int(item.target_multi) << 7)

        data.extend(chunk)
    return bytes(data)

def parse_db_wear(data: bytes) -> list[Item]:
    RECORD_SIZE = 0x74
    STRING_SIZE = 0x18
    BASE = STRING_SIZE * 4
    gears = []
    for gear_id, offset in enumerate(range(0, len(data), RECORD_SIZE)):
        chunk = data[offset:offset + RECORD_SIZE]
        if len(chunk) < RECORD_SIZE:
            break
        gear = Item()
        gear.raw_data = chunk
        gear.id = gear_id + 0x2000

        gear.label_name = read_string(chunk, 0x00, STRING_SIZE)
        gear.label_nams = read_string(chunk, 0x18, STRING_SIZE)
        gear.label_desc = read_string(chunk, 0x30, STRING_SIZE)
        gear.label_full = read_string(chunk, 0x48, STRING_SIZE)

        gear.sprite = struct.unpack_from("<I", chunk, BASE + 0x00)[0]
        gear.price = struct.unpack_from("<H", chunk, BASE + 0x04)[0]

        gear.effect_id = struct.unpack_from("<H", chunk, BASE + 0x06)[0]
        gear.effect_param1 = struct.unpack_from("<h", chunk, BASE + 0x08)[0]

        gear.hp = struct.unpack_from("<B", chunk, BASE + 0xA)[0]
        gear.bp = struct.unpack_from("<B", chunk, BASE + 0xB)[0]
        gear.pwr = struct.unpack_from("<B", chunk, BASE + 0xC)[0]
        gear.dfn = struct.unpack_from("<B", chunk, BASE + 0xD)[0]
        gear.spe = struct.unpack_from("<B", chunk, BASE + 0xE)[0]
        gear.sta = struct.unpack_from("<B", chunk, BASE + 0xF)[0]

        gear.user = chunk[BASE + 0x10] & 0x03

        gears.append(gear)
    return gears

def repack_db_wear(gears: list[Item]) -> bytes:
    RECORD_SIZE = 0x74
    STRING_SIZE = 0x18
    BASE = STRING_SIZE * 4
    data = bytearray()
    for gear in gears:
        chunk = bytearray(gear.raw_data[:RECORD_SIZE])

        write_string(chunk, 0x00, gear.label_name, STRING_SIZE)
        write_string(chunk, 0x18, gear.label_nams, STRING_SIZE)
        write_string(chunk, 0x30, gear.label_desc, STRING_SIZE)
        write_string(chunk, 0x48, gear.label_full, STRING_SIZE)

        struct.pack_into("<I", chunk, BASE + 0x00, gear.sprite)
        struct.pack_into("<H", chunk, BASE + 0x04, gear.price)

        struct.pack_into("<H", chunk, BASE + 0x06, gear.effect_id)
        struct.pack_into("<h", chunk, BASE + 0x08, gear.effect_param1)

        struct.pack_into("<B", chunk, BASE + 0x0A, gear.hp)
        struct.pack_into("<B", chunk, BASE + 0x0B, gear.bp)
        struct.pack_into("<B", chunk, BASE + 0x0C, gear.pwr)
        struct.pack_into("<B", chunk, BASE + 0x0D, gear.dfn)
        struct.pack_into("<B", chunk, BASE + 0x0E, gear.spe)
        struct.pack_into("<B", chunk, BASE + 0x0F, gear.sta)

        chunk[BASE + 0x10] = (chunk[BASE + 0x10] & 0xFC) | (gear.user & 0x03)

        data.extend(chunk)
    return bytes(data)

def parse_db_badge(data: bytes) -> list[Item]:
    RECORD_SIZE = 0x70
    STRING_SIZE = 0x18
    BASE = STRING_SIZE * 4
    gears = []
    for gear_id, offset in enumerate(range(0, len(data), RECORD_SIZE)):
        chunk = data[offset:offset + RECORD_SIZE]
        if len(chunk) < RECORD_SIZE:
            break
        gear = Item()
        gear.raw_data = chunk
        gear.id = gear_id + 0x3000

        gear.label_name = read_string(chunk, 0x00, STRING_SIZE)
        gear.label_nams = read_string(chunk, 0x18, STRING_SIZE)
        gear.label_desc = read_string(chunk, 0x30, STRING_SIZE)
        gear.label_full = read_string(chunk, 0x48, STRING_SIZE)

        gear.sprite = struct.unpack_from("<I", chunk, BASE + 0x00)[0]
        gear.price = struct.unpack_from("<H", chunk, BASE + 0x04)[0]
        
        gear.effect_id = struct.unpack_from("<H", chunk, BASE + 0x06)[0]
        gear.effect_param1 = struct.unpack_from("<h", chunk, BASE + 0x08)[0]

        gear.hp = struct.unpack_from("<B", chunk, BASE + 0xA)[0]
        gear.bp = struct.unpack_from("<B", chunk, BASE + 0xB)[0]
        gear.pwr = struct.unpack_from("<B", chunk, BASE + 0xC)[0]
        gear.dfn = struct.unpack_from("<B", chunk, BASE + 0xD)[0]
        gear.spe = struct.unpack_from("<B", chunk, BASE + 0xE)[0]
        gear.sta = struct.unpack_from("<B", chunk, BASE + 0xF)[0]

        gears.append(gear)
    return gears

def repack_db_badge(gears: list[Item]) -> bytes:
    RECORD_SIZE = 0x70
    STRING_SIZE = 0x18
    BASE = STRING_SIZE * 4
    data = bytearray()
    for gear in gears:
        chunk = bytearray(gear.raw_data[:RECORD_SIZE])

        write_string(chunk, 0x00, gear.label_name, STRING_SIZE)
        write_string(chunk, 0x18, gear.label_nams, STRING_SIZE)
        write_string(chunk, 0x30, gear.label_desc, STRING_SIZE)
        write_string(chunk, 0x48, gear.label_full, STRING_SIZE)

        struct.pack_into("<I", chunk, BASE + 0x00, gear.sprite)
        struct.pack_into("<H", chunk, BASE + 0x04, gear.price)

        struct.pack_into("<H", chunk, BASE + 0x06, gear.effect_id)
        struct.pack_into("<h", chunk, BASE + 0x08, gear.effect_param1)

        struct.pack_into("<B", chunk, BASE + 0x0A, gear.hp)
        struct.pack_into("<B", chunk, BASE + 0x0B, gear.bp)
        struct.pack_into("<B", chunk, BASE + 0x0C, gear.pwr)
        struct.pack_into("<B", chunk, BASE + 0x0D, gear.dfn)
        struct.pack_into("<B", chunk, BASE + 0x0E, gear.spe)
        struct.pack_into("<B", chunk, BASE + 0x0F, gear.sta)
        data.extend(chunk)
    return bytes(data)

def parse_db_accessory(data: bytes) -> list[Item]:
    RECORD_SIZE = 0x68
    STRING_SIZE = 0x18
    BASE = STRING_SIZE * 4
    gears = []
    for gear_id, offset in enumerate(range(0, len(data), RECORD_SIZE)):
        chunk = data[offset:offset + RECORD_SIZE]
        if len(chunk) < RECORD_SIZE:
            break
        gear = Item()
        gear.raw_data = chunk
        gear.id = gear_id + 0x4000

        gear.label_name = read_string(chunk, 0x00, STRING_SIZE)
        gear.label_nams = read_string(chunk, 0x18, STRING_SIZE)
        gear.label_desc = read_string(chunk, 0x30, STRING_SIZE)
        gear.label_full = read_string(chunk, 0x48, STRING_SIZE)

        gear.sprite = struct.unpack_from("<I", chunk, BASE + 0x00)[0]

        gear.effect_id = struct.unpack_from("<H", chunk, BASE + 0x04)[0]
        gear.effect_param1 = struct.unpack_from("<h", chunk, BASE + 0x06)[0]

        gears.append(gear)
    return gears

def repack_db_accessory(gears: list[Item]) -> bytes:
    RECORD_SIZE = 0x68
    STRING_SIZE = 0x18
    BASE = STRING_SIZE * 4
    data = bytearray()
    for gear in gears:
        chunk = bytearray(gear.raw_data[:RECORD_SIZE])

        write_string(chunk, 0x00, gear.label_name, STRING_SIZE)
        write_string(chunk, 0x18, gear.label_nams, STRING_SIZE)
        write_string(chunk, 0x30, gear.label_desc, STRING_SIZE)
        write_string(chunk, 0x48, gear.label_full, STRING_SIZE)

        struct.pack_into("<I", chunk, BASE + 0x00, gear.sprite)

        struct.pack_into("<H", chunk, BASE + 0x04, gear.effect_id)
        struct.pack_into("<h", chunk, BASE + 0x06, gear.effect_param1)
        
        data.extend(chunk)
    return bytes(data)

def parse_db_keyitem(data: bytes) -> list[Item]:
    RECORD_SIZE = 0x64
    STRING_SIZE = 0x18
    BASE = STRING_SIZE * 4
    items = []
    for gear_id, offset in enumerate(range(0, len(data), RECORD_SIZE)):
        chunk = data[offset:offset + RECORD_SIZE]
        if len(chunk) < RECORD_SIZE:
            break
        item = Item()
        item.raw_data = chunk
        item.id = gear_id + 0x5000

        item.label_name = read_string(chunk, 0x00, STRING_SIZE)
        item.label_nams = read_string(chunk, 0x18, STRING_SIZE)
        item.label_desc = read_string(chunk, 0x30, STRING_SIZE)
        item.label_full = read_string(chunk, 0x48, STRING_SIZE)

        item.sprite = struct.unpack_from("<I", chunk, BASE + 0x00)[0]

        items.append(item)
    return items

def repack_db_keyitem(items: list[Item]) -> bytes:
    RECORD_SIZE = 0x68
    STRING_SIZE = 0x18
    BASE = STRING_SIZE * 4
    data = bytearray()
    for item in items:
        chunk = bytearray(item.raw_data[:RECORD_SIZE])

        write_string(chunk, 0x00, item.label_name, STRING_SIZE)
        write_string(chunk, 0x18, item.label_nams, STRING_SIZE)
        write_string(chunk, 0x30, item.label_desc, STRING_SIZE)
        write_string(chunk, 0x48, item.label_full, STRING_SIZE)

        struct.pack_into("<I", chunk, BASE + 0x00, item.sprite)
        
        data.extend(chunk)
    return bytes(data)

def parse_db_bean(data: bytes) -> list[Item]:
    RECORD_SIZE = 0x64
    STRING_SIZE = 0x18
    BASE = STRING_SIZE * 4
    items = []
    for gear_id, offset in enumerate(range(0, len(data), RECORD_SIZE)):
        chunk = data[offset:offset + RECORD_SIZE]
        if len(chunk) < RECORD_SIZE:
            break
        item = Item()
        item.raw_data = chunk
        item.id = gear_id + 0x6000

        item.label_name = read_string(chunk, 0x00, STRING_SIZE)
        item.label_nams = read_string(chunk, 0x18, STRING_SIZE)
        item.label_desc = read_string(chunk, 0x30, STRING_SIZE)
        item.label_full = read_string(chunk, 0x48, STRING_SIZE)

        item.sprite = struct.unpack_from("<I", chunk, BASE + 0x00)[0]

        items.append(item)
    return items

def repack_db_bean(items: list[Item]) -> bytes:
    RECORD_SIZE = 0x68
    STRING_SIZE = 0x18
    BASE = STRING_SIZE * 4
    data = bytearray()
    for item in items:
        chunk = bytearray(item.raw_data[:RECORD_SIZE])

        write_string(chunk, 0x00, item.label_name, STRING_SIZE)
        write_string(chunk, 0x18, item.label_nams, STRING_SIZE)
        write_string(chunk, 0x30, item.label_desc, STRING_SIZE)
        write_string(chunk, 0x48, item.label_full, STRING_SIZE)

        struct.pack_into("<I", chunk, BASE + 0x00, item.sprite)
        
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