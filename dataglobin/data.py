from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import struct

import dataglobin.constants as Constants
from dataglobin.constants import GameID, Language
import dataglobin.persistent as Persistent
import dataglobin.msbt as MSBT

GAME_VERSION = Constants.DEFAULT_VERSION

ITEMDATA = {}
TEXT_DICT = {}
GEARWEARS = []
GEARBADGES = []
GEARACCESRORIES = []
KEYITEMS = []
BEANS = []
BADGES = []
CARDS = []
MONSTERS = []
INV_ORDER = {}
HASH_TABLE = {}
EFFECTS_NAMES = {}

DB_DAT = None
KJ_DAT = None

LANGUAGES_PRIORITY = [
    Language.US_EN, Language.US_FR, Language.US_SP, 
    Language.EU_EN, Language.EU_FR, Language.EU_SP, Language.EU_GE, Language.EU_IT, 
    Language.EU_DU, Language.EU_PT, Language.EU_RU,
    Language.JP_JA, Language.KR_KO
]

#LANGUAGES_ML5 = ["US_en", "US_fr", "US_sp", "EU_en", "EU_fr", "EU_sp", "EU_ge", "EU_it", "EU_du", "EU_pt"]
LANGUAGES_ML5 = ["US_en", "US_sp"]

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
    effect_param1: int = None
    effect_param2: int = None
    type: int = None
    user: int = None
    hp: int = None
    bp: int = None
    pwr: int = None
    dfn: int = None
    spe: int = None
    sta: int = None
    flags1: list[bool] = None
    flags2: list[bool] = None
    flags3: list[bool] = None
    flags4: list[bool] = None
    unk1 = None
    unk2 = None
    unk3 = None
    unk4 = None

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

def repack_db(entries: list[bytes]) -> bytes:
    count = len(entries)
    header_size = count * 4
    offsets = []
    current_offset = header_size
    for entry in entries:
        offsets.append(current_offset)
        current_offset += len(entry)
    header = struct.pack(f"<{count}I", *offsets)
    return header + b"".join(entries)

def parse_db_order(data):
    order = [
        int.from_bytes(data[i:i + 2], byteorder="little")
        for i in range(0, len(data), 2)
    ]
    padding = 0 if order and order[-1] == 0 else None
    if padding is not None:
        order.pop()
    return {
        "list": order,
        "padding": padding,
    }

def repack_db_order(order: dict) -> bytes:
    data = b"".join(
        value.to_bytes(2, byteorder="little")
        for value in order["list"]
    )
    if order["padding"] is not None:
        data += order["padding"].to_bytes(2, byteorder="little")
    return data

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

def validate_db_language(version: GameID, text_dict):
    if version in (GameID.ML3R, GameID.ML1R, GameID.ML5):
        available_languages = set(text_dict.keys())
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

def get_effect_name(language: Language, key: str, item_id: int) -> str:
    names = EFFECTS_NAMES.get(key, [])
    if not 0 <= item_id < len(names):
        return ""
    label = names[item_id]
    return get_msbt_string(language, "Item.msbt", label) or label

def load_data(version: GameID, rom_path: Path):
    global GAME_VERSION
    global ITEMDATA
    global TEXT_DICT
    global INV_ORDER
    global HASH_TABLE
    global EFFECTS_NAMES
    if version == GameID.ML3R:
        from dataglobin.ml3r.parser import parse_db_items, parse_db_gear, parse_db_effects

        _TEXT_DICT = MSBT.load_msbt(version, rom_path)
        validate_db_language(version, _TEXT_DICT)
        print("DB Language", Persistent.UI_DB_LANGUAGE)

        db_dat = parse_db(Path(rom_path) / 'DB' / 'DB.dat')

        _ITEMDATA = {}
        _ITEMDATA["UITM"] = parse_db_items(db_dat[0])
        _ITEMDATA["EITM"] = parse_db_gear(db_dat[3])

        _INV_ORDER = {}
        _INV_ORDER["UITM"] = parse_db_order(db_dat[1])
        _INV_ORDER["EITM"] = parse_db_order(db_dat[4])
        _INV_ORDER["BITM"] = parse_db_order(db_dat[7])
        _HASH_TABLE = {}
        _HASH_TABLE["UITM"] = parse_db_hash(db_dat[2])
        _HASH_TABLE["EITM"] = parse_db_hash(db_dat[5])
        _HASH_TABLE["BITM"] = parse_db_hash(db_dat[8])
        _HASH_TABLE["BMON"] = parse_db_hash(db_dat[15])
        _EFFECTS_NAMES = {}
        _EFFECTS_NAMES["EITM"] = parse_db_effects(db_dat[9])

        TEXT_DICT = _TEXT_DICT
        ITEMDATA = _ITEMDATA
        INV_ORDER = _INV_ORDER
        HASH_TABLE = _HASH_TABLE
        EFFECTS_NAMES = _EFFECTS_NAMES

        Persistent.ML3R_ROMFS_INPUT = rom_path

    elif version == GameID.ML1R:
        from dataglobin.ml1r.parser import parse_db_items, parse_db_effects

        _TEXT_DICT = MSBT.load_msbt(version, rom_path)
        validate_db_language(version, _TEXT_DICT)
        print("DB Language", Persistent.UI_DB_LANGUAGE)

        db_dat = parse_db(Path(rom_path) / 'DB' / 'DB.dat')

        _ITEMDATA = {}
        _ITEMDATA["UITM"] = parse_db_items(db_dat[0])

        _INV_ORDER = {}
        _INV_ORDER["UITM"] = parse_db_order(db_dat[1])
        _INV_ORDER["WITM"] = parse_db_order(db_dat[4])
        _INV_ORDER["BITM"] = parse_db_order(db_dat[7])
        _INV_ORDER["SITM"] = parse_db_order(db_dat[10])
        _INV_ORDER["EITM"] = parse_db_order(db_dat[13])
        _INV_ORDER["BEAN"] = parse_db_order(db_dat[16])
        _HASH_TABLE = {}
        _HASH_TABLE["UITM"] = parse_db_hash(db_dat[2])
        _HASH_TABLE["WITM"] = parse_db_hash(db_dat[5])
        _HASH_TABLE["BITM"] = parse_db_hash(db_dat[8])
        _HASH_TABLE["SITM"] = parse_db_hash(db_dat[11])
        _HASH_TABLE["EITM"] = parse_db_hash(db_dat[14])
        _HASH_TABLE["BEAN"] = parse_db_hash(db_dat[17])
        _HASH_TABLE["BMON"] = parse_db_hash(db_dat[24])
        _EFFECTS_NAMES = {}
        _EFFECTS_NAMES["WITM"] = parse_db_effects(db_dat[18])
        _EFFECTS_NAMES["BITM"] = parse_db_effects(db_dat[19])
        _EFFECTS_NAMES["SITM"] = parse_db_effects(db_dat[20])

        TEXT_DICT = _TEXT_DICT
        ITEMDATA = _ITEMDATA
        INV_ORDER = _INV_ORDER
        HASH_TABLE = _HASH_TABLE
        EFFECTS_NAMES = _EFFECTS_NAMES

        Persistent.ML1R_ROMFS_INPUT = rom_path
    
    elif version == GameID.ML5:
        from dataglobin.ml5.parser import parse_db_items, parse_db_cards

        _TEXT_DICT = MSBT.load_msbt(version, rom_path)
        validate_db_language(version, _TEXT_DICT)
        print("DB Language", Persistent.UI_DB_LANGUAGE)

        db_dat = parse_db(Path(rom_path) / 'DB' / 'DB.dat')
        
        _ITEMDATA = {}
        _ITEMDATA["UITM"] = parse_db_items(db_dat[0])
        _ITEMDATA["CITM"] = parse_db_cards(db_dat[6])

        _INV_ORDER = {}
        _INV_ORDER["UITM"] = parse_db_order(db_dat[1])
        _INV_ORDER["WITM"] = parse_db_order(db_dat[4])
        _INV_ORDER["CITM"] = parse_db_order(db_dat[7])
        _HASH_TABLE = {}
        _HASH_TABLE["UITM"] = parse_db_hash(db_dat[2])
        _HASH_TABLE["WITM"] = parse_db_hash(db_dat[5])
        _HASH_TABLE["CITM"] = parse_db_hash(db_dat[8])
        _HASH_TABLE["BMON"] = parse_db_hash(db_dat[10])

        TEXT_DICT = _TEXT_DICT
        ITEMDATA = _ITEMDATA
        INV_ORDER = _INV_ORDER
        HASH_TABLE = _HASH_TABLE

        Persistent.ML5_ROMFS_INPUT = rom_path
    
    GAME_VERSION = version

def export_data(directory: str):
    if GAME_VERSION in (GameID.ML3R, GameID.ML1R, GameID.ML5):
        # Input
        input_dirs = {
            GameID.ML3R: Persistent.ML3R_ROMFS_INPUT,
            GameID.ML1R: Persistent.ML1R_ROMFS_INPUT,
            GameID.ML5: Persistent.ML5_ROMFS_INPUT,
        }
        input_rom_dir = input_dirs[GAME_VERSION]
        if input_rom_dir is None:
            raise ValueError(f"No input ROMFS directory loaded for {GAME_VERSION}")
        
        input_rom_dir = Path(input_rom_dir)
        output_dir = Path(directory)

        # DB.dat
        db_source = input_rom_dir / "DB" / "DB.dat"
        db_destination = output_dir / "romfs" / "DB" / "DB.dat"
        db_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(db_source, db_destination)
        db_dat = parse_db(db_destination)
        if GAME_VERSION == GameID.ML3R:
            from dataglobin.ml3r.parser import repack_db_items, repack_db_gear, repack_db_effects
            db_dat[0] = repack_db_items(ITEMDATA["UITM"])
            db_dat[1] = repack_db_order(INV_ORDER["UITM"])
            db_dat[3] = repack_db_gear(ITEMDATA["EITM"])
            db_dat[4] = repack_db_order(INV_ORDER["EITM"])
            db_dat[7] = repack_db_order(INV_ORDER["BITM"])
            db_dat[9] = repack_db_effects(EFFECTS_NAMES["EITM"])

        elif GAME_VERSION == GameID.ML1R:
            from dataglobin.ml1r.parser import repack_db_items, repack_db_effects
            db_dat[0]  = repack_db_items(ITEMDATA["UITM"])
            db_dat[1]  = repack_db_order(INV_ORDER["UITM"])
            db_dat[4]  = repack_db_order(INV_ORDER["WITM"])
            db_dat[7]  = repack_db_order(INV_ORDER["BITM"])
            db_dat[10] = repack_db_order(INV_ORDER["SITM"])
            db_dat[13] = repack_db_order(INV_ORDER["EITM"])
            db_dat[16] = repack_db_order(INV_ORDER["BEAN"])
            db_dat[18] = repack_db_effects(EFFECTS_NAMES["WITM"])
            db_dat[19] = repack_db_effects(EFFECTS_NAMES["BITM"])
            db_dat[20] = repack_db_effects(EFFECTS_NAMES["SITM"])
        
        elif GAME_VERSION == GameID.ML5:
            from dataglobin.ml5.parser import repack_db_items
            db_dat[0] = repack_db_items(ITEMDATA["UITM"])
            db_dat[1] = repack_db_order(INV_ORDER["UITM"])
            db_dat[4] = repack_db_order(INV_ORDER["EITM"])
            db_dat[7] = repack_db_order(INV_ORDER["CITM"])

        db_destination.write_bytes(repack_db(db_dat))

        # Msg
        msg_source = input_rom_dir / "Msg"
        msg_destination = output_dir / "romfs" / "Msg"
        for language in LANGUAGES_ML5:
            source_dir = msg_source / language
            if not source_dir.is_dir():
                continue
            destination_dir = msg_destination / language
            destination_dir.mkdir(parents=True, exist_ok=True)
            for filename in ("Item.msbt", "BMsg.dat"):
                source_file = source_dir / filename
                if source_file.is_file():
                    shutil.copy2(source_file, destination_dir / filename)

        # Config
        output_dirs = {
            GameID.ML3R: "ML3R_ROMFS_OUTPUT",
            GameID.ML1R: "ML1R_ROMFS_OUTPUT",
            GameID.ML5: "ML5_ROMFS_OUTPUT",
        }
        setattr(Persistent, output_dirs[GAME_VERSION], output_dir)