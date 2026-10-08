from pathlib import Path
from enum import Enum

SCRIPT_DIR = Path(__file__).parent
FILES_DIR = SCRIPT_DIR / 'files'

APP_NAME = "dataglobin"
APP_DISPLAY_NAME = "Dataglobin DX"

LANGUAGE_NAMES = ["日本語", "English", "Français", "Deutsch", "Italiano", "Español"]

class Language(Enum):
    JP_JA = "JP_ja"
    US_EN = "US_en"
    US_FR = "US_fr"
    US_SP = "US_sp"
    EU_EN = "EU_en"
    EU_FR = "EU_fr"
    EU_GE = "EU_ge"
    EU_IT = "EU_it"
    EU_SP = "EU_sp"
    EU_DU = "EU_du"
    EU_PT = "EU_pt"
    EU_RU = "EU_ru"
    KR_KO = "KR_ko"

class GameID(Enum):
    UNK = "UNK"
    ML1 = "ML1"
    ML2 = "ML2"
    ML3 = "ML3"
    ML4 = "ML4"
    ML5 = "ML5"
    ML1R = "ML1R"
    ML3R = "ML3R"

DEFAULT_VERSION = GameID.ML3R

ML3R_EFFECTS_UITM = [
    {
        "id": 0x1000,
        "name": "HP Recovery",
        "note": "Recovers HP.",
        "param1": "Recovered HP.\n0 = 100% recovery."
    },
    {
        "id": 0x1001,
        "name": "BP Recovery",
        "note": "Recovers BP.",
        "param1": "Recovered BP.\n0 = 100% recovery."
    },
    {
        "id": 0x1002,
        "name": "Revive",
        "note": "Revives downed characters.",
        "param1": "Recovered HP %."
    },
    {
        "id": 0x1003,
        "name": "Status Cure",
        "note": "Cures negative status effects.",
        "param1": "N/A"
    },
    {
        "id": 0x1004,
        "name": "HP & BP Recovery %",
        "note": "Recovers a percentage of HP and BP.",
        "param1": "Recovered HP & BP %.\n0 = 100% recovery."
    },
    {
        "id": 0x1005,
        "name": "HP Up",
        "note": "Permanently increases the player's HP.",
        "param1": "HP Increase."
    },
    {
        "id": 0x1006,
        "name": "BP Up",
        "note": "Permanently increases the player's BP.",
        "param1": "BP Increase."
    },
    {
        "id": 0x1007,
        "name": "POW Up",
        "note": "Permanently increases the player's POW.",
        "param1": "POW Increase."
    },
    {
        "id": 0x1008,
        "name": "DEF Up",
        "note": "Permanently increases the player's DEF.",
        "param1": "DEF Increase."
    },
    {
        "id": 0x1009,
        "name": "SPEED Up",
        "note": "Permanently increases the player's SPEED.",
        "param1": "SPEED Increase."
    },
    {
        "id": 0x100A,
        "name": "STACHE/HORN Up",
        "note": "Permanently increases the player's STACHE/HORN.",
        "param1": "STACHE/HORN Increase."
    },
    {
        "id": 0x100B,
        "name": "Unused",
        "note": "N/A",
        "param1": "N/A"
    },
    {
        "id": 0x100C,
        "name": "Boo Biscuit",
        "note": "Makes the player invincible for a certain amount of turns.",
        "param1": "Turn duration."
    },
]

ML3R_UITM_CONDITION = [
    { "id":  0, "name": "No special condition" },
    { "id":  1, "name": "Missing HP (HP)" },
    { "id":  2, "name": "Missing BP (BP)" },
    { "id":  3, "name": "Is KO'd" },
    { "id":  4, "name": "Affected by negative status" },
    { "id":  5, "name": "Missing HP or BP (HP & BP)" },
    { "id":  6, "name": "No use (HP)" },
    { "id":  7, "name": "No use (BP)" },
    { "id":  8, "name": "No use (POW)" },
    { "id":  9, "name": "No use (DEF)" },
    { "id": 10, "name": "No use (SPEED)" },
    { "id": 11, "name": "No use (STACHE/HORN)" },
    { "id": 12, "name": "???" },
    { "id": 13, "name": "All party members can act" },
]