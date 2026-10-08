from dataclasses import dataclass
import os
from pathlib import Path
import struct

import dataglobin.constants as Constants
from dataglobin.constants import GameID, Language
import dataglobin.persistent as Persistent
import dataglobin.msbt as MSBT

GAME_VERSION = Constants.DEFAULT_VERSION

TEXT_DICT = []
ITEMS = []
WEARS = []
BADGES = []
MONSTERS = []

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
    price: int = None
    effect_id: int = None
    effect_param: int = None
    flags1: list[bool] = None
    flags2: list[bool] = None

    def getDefaultName(self):
        return get_msbt_string(Persistent.UI_DB_LANGUAGE, "Item", self.label_name)

    def getNameValue(self):
        return get_msbt_string(Persistent.DB_LANGUAGE, "Item", self.label_name)

    def getNamsValue(self):
        return get_msbt_string(Persistent.DB_LANGUAGE, "Item", self.label_nams)

    def getDescValue(self):
        return get_msbt_string(Persistent.DB_LANGUAGE, "Item", self.label_desc)

    def getFullValue(self):
        return get_msbt_string(Persistent.DB_LANGUAGE, "Item", self.label_full)


def parse_db(path):
    data = open(path, "rb").read()
    header_size = struct.unpack_from("<I", data, 0)[0]
    count = header_size // 4
    offsets = list(struct.unpack_from(f"<{count}I", data, 0))
    return [
        data[start:(offsets[i + 1] if i + 1 < count else len(data))]
        for i, start in enumerate(offsets)
    ]

# Validates that the input data contains language data
def validate_db_language():
    if GAME_VERSION in (GameID.ML3R, GameID.ML1R, GameID.ML5):
        available_languages = {text["language"] for text in TEXT_DICT}
        if Persistent.DB_LANGUAGE in available_languages:
            return
        for language in LANGUAGES_PRIORITY:
            if language in available_languages:
                Persistent.UI_DB_LANGUAGE = language
                Persistent.DB_LANGUAGE = language
                return
        raise RuntimeError("No available languages found in TEXT_DICT")

def get_msbt_string(language: Language, filename: str, label: str ) -> str | None:
    for language_data in TEXT_DICT:
        if language_data.get("language") != language:
            continue
        for msbt in language_data.get("msbt", []):
            if msbt.get("filename") != filename:
                continue
            for message in msbt.get("data", []):
                if message.get("key") == label:
                    return message.get("value")
    return None

def load_data(rom_path: Path):
    global GAME_VERSION
    if GAME_VERSION == GameID.ML3R:
        from dataglobin.parsers.ml3r import parse_db_items_ml3r

        global TEXT_DICT
        global ITEMS

        TEXT_DICT = MSBT.load_msbt(rom_path)
        validate_db_language()
        print("DB Language", Persistent.DB_LANGUAGE)

        db_dat = parse_db(os.path.join(rom_path, 'DB', 'DB.dat'))
        kj_dat = parse_db(os.path.join(rom_path, 'KJ', 'KJ.dat'))

        items = parse_db_items_ml3r(db_dat[0])
        ITEMS = items
