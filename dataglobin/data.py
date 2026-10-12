from dataclasses import dataclass
import os
from pathlib import Path
import struct

import dataglobin.constants as Constants
from dataglobin.constants import GameID, Language
import dataglobin.persistent as Persistent
import dataglobin.msbt as MSBT

GAME_VERSION = Constants.DEFAULT_VERSION

TEXT_DICT = {}
ITEMS = []
WEARS = []
BADGES = []
MONSTERS = []
INV_ORDER = {}
HASH_TABLE = {}

LANGUAGES_PRIORITY = [
    Language.US_EN, Language.US_FR, Language.US_SP, 
    Language.EU_EN, Language.EU_FR, Language.EU_SP, Language.EU_GE, Language.EU_IT, 
    Language.EU_DU, Language.EU_PT, Language.EU_RU,
    Language.JP_JA, Language.KR_KO
]

@dataclass
class Item:
    raw_data: bytes = None
    id: int = None
    order: int = None
    label_name: str = None
    label_nams: str = None
    label_desc: str = None
    label_full: str = None
    sprite: int = None
    price: int = None
    effect_id: int = None
    effect_param: int = None
    flags1: list[bool] = None
    flags2: list[bool] = None
    flags3: list[bool] = None
    flags4: list[bool] = None

    def getDefaultName(self):
        return get_msbt_string(Persistent.UI_DB_LANGUAGE, "Item.msbt", self.label_name)

    def getName(self, language: Language):
        return get_msbt_string(language, "Item.msbt", self.label_name)

    def getNams(self, language: Language):
        return get_msbt_string(language, "Item.msbt", self.label_nams)

    def getDesc(self, language: Language):
        return get_msbt_string(language, "Item.msbt", self.label_desc)

    def getFull(self, language: Language):
        return get_msbt_string(language, "Item.msbt", self.label_full)

@dataclass
class HashEntry:
    id: int
    length: int
    last_char: str
    bucket_id: int
@dataclass
class HashTable:
    bucket_amount: int
    entries: list[HashEntry]
    def compute_hash(self, value):
        hsh = 0
        for c in value.encode("utf-8"):
            hsh = (hsh * 0x492 + c) & 0xFFFFFFFF
        return (hsh & 0x7FFFFFFF) % self.bucket_amount
    def compute_metadata(self, value):
        return self.compute_hash(value), value[-1], len(value)
    
def parse_db(path):
    data = open(path, "rb").read()
    header_size = struct.unpack_from("<I", data, 0)[0]
    count = header_size // 4
    offsets = list(struct.unpack_from(f"<{count}I", data, 0))
    return [
        data[start:(offsets[i + 1] if i + 1 < count else len(data))]
        for i, start in enumerate(offsets)
    ]

def parse_db_order(data):
    chunk = data[:-2]
    return [
        int.from_bytes(chunk[i:i + 2], byteorder="little")
        for i in range(0, len(chunk), 2)
    ]


def parse_db_hash(data):
    amount = int.from_bytes(data[0:2], byteorder="little")
    header_size = 2 + (amount + 1) * 2
    offsets = [
        int.from_bytes(data[2 + i * 2: 4 + i * 2], byteorder="little")
        for i in range(amount + 1)
    ]
    entries = []
    for bucket_id in range(amount):
        start = offsets[bucket_id]
        end = offsets[bucket_id + 1]
        if start < header_size or end < start or end > len(data):
            raise ValueError(f"Invalid offsets for bucket {bucket_id}")
        if (end - start) % 4 != 0:
            raise ValueError(f"Invalid entry data size in bucket {bucket_id}")
        for offset in range(start, end, 4):
            entry_id = int.from_bytes(data[offset:offset + 2], "little")
            length = data[offset + 2]
            last_char = chr(data[offset + 3])
            entries.append(HashEntry(id=entry_id, length=length, last_char=last_char, bucket_id=bucket_id))
    return HashTable(bucket_amount=amount, entries=entries)

# Validates that the input data contains language data
def validate_db_language():
    if GAME_VERSION in (GameID.ML3R, GameID.ML1R, GameID.ML5):
        available_languages = set(TEXT_DICT.keys())
        if Persistent.UI_DB_LANGUAGE in available_languages:
            return
        for language in LANGUAGES_PRIORITY:
            if language in available_languages:
                Persistent.UI_DB_LANGUAGE = language
                return
        raise RuntimeError("No available languages found in TEXT_DICT")

def get_msbt_string(language: Language, filename: str, label: str) -> str | None:
    language_data = TEXT_DICT.get(language, {})
    msbt = language_data.get(filename)
    if msbt is None:
        return ""
    for message in msbt.get("data", []):
        if message.get("key") == label:
            return message.get("value")
    return ""

def load_data(rom_path: Path):
    global GAME_VERSION
    global TEXT_DICT
    global ITEMS
    global INV_ORDER
    if GAME_VERSION == GameID.ML3R:
        from dataglobin.ml3r.parser import parse_db_items

        TEXT_DICT = MSBT.load_msbt(rom_path)
        validate_db_language()
        print("DB Language", Persistent.UI_DB_LANGUAGE)

        db_dat = parse_db(os.path.join(rom_path, 'DB', 'DB.dat'))
        kj_dat = parse_db(os.path.join(rom_path, 'KJ', 'KJ.dat'))

        items = parse_db_items(db_dat[0])
        ITEMS = items

        INV_ORDER["UITM"] = parse_db_order(db_dat[1])
        INV_ORDER["WITM"] = parse_db_order(db_dat[4])
        INV_ORDER["BITM"] = parse_db_order(db_dat[7])
        HASH_TABLE["UITM"] = parse_db_hash(db_dat[2])
        HASH_TABLE["WITM"] = parse_db_hash(db_dat[5])
        HASH_TABLE["BITM"] = parse_db_hash(db_dat[8])
        HASH_TABLE["MON"]  = parse_db_hash(db_dat[15])
    
    elif GAME_VERSION == GameID.ML5:
        from dataglobin.ml5.parser import parse_db_items

        TEXT_DICT = MSBT.load_msbt(rom_path)
        validate_db_language()
        print("DB Language", Persistent.UI_DB_LANGUAGE)

        db_dat = parse_db(os.path.join(rom_path, 'DB', 'DB.dat'))

        items = parse_db_items(db_dat[0])
        ITEMS = items

        INV_ORDER["UITM"] = parse_db_order(db_dat[1])
        INV_ORDER["WITM"] = parse_db_order(db_dat[4])
        INV_ORDER["CITM"] = parse_db_order(db_dat[7])
        HASH_TABLE["UITM"] = parse_db_hash(db_dat[2])
        HASH_TABLE["WITM"] = parse_db_hash(db_dat[5])
        HASH_TABLE["CITM"] = parse_db_hash(db_dat[8])
        HASH_TABLE["MON"]  = parse_db_hash(db_dat[10])
