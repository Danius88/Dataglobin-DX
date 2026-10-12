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





ML5_EFFECTS_UITM = [
    {
        "id": 0,
        "name": "HP Recovery",
        "note": "Recovers HP.",
        "param1": "Recovered HP.\n0 = 100% recovery."
    },
    {
        "id": 1,
        "name": "BP Recovery",
        "note": "Recovers BP.",
        "param1": "Recovered BP.\n0 = 100% recovery."
    },
    {
        "id": 2,
        "name": "Revive",
        "note": "Revives downed characters.",
        "param1": "Recovered HP %."
    },
    {
        "id": 3,
        "name": "Status Cure",
        "note": "Cures negative status effects.",
        "param1": "N/A"
    },
    {
        "id": 4,
        "name": "HP & BP Recovery %",
        "note": "Recovers a percentage of HP and BP.",
        "param1": "Recovered HP & BP %.\n0 = 100% recovery."
    },
    {
        "id": 5,
        "name": "Raw HP Up",
        "note": "Permanently increases the player's HP.",
        "param1": "HP Increase."
    },
    {
        "id": 6,
        "name": "Raw BP Up",
        "note": "Permanently increases the player's BP.",
        "param1": "BP Increase."
    },
    {
        "id": 7,
        "name": "Raw POW Up",
        "note": "Permanently increases the player's POW.",
        "param1": "POW Increase."
    },
    {
        "id": 8,
        "name": "Raw DEF Up",
        "note": "Permanently increases the player's DEF.",
        "param1": "DEF Increase."
    },
    {
        "id": 9,
        "name": "Raw SPEED Up",
        "note": "Permanently increases the player's SPEED.",
        "param1": "SPEED Increase."
    },
    {
        "id": 10,
        "name": "Raw STACHE Up",
        "note": "Permanently increases the player's STACHE.",
        "param1": "STACHE Increase."
    },
    {
        "id": 11,
        "name": "Unused",
        "note": "N/A",
        "param1": "N/A"
    },
    {
        "id": 12,
        "name": "Unused",
        "note": "N/A",
        "param1": "N/A"
    },
    {
        "id": 13,
        "name": "Boo Biscuit",
        "note": "Makes the player invincible for a certain amount of turns.",
        "param1": "Turn duration."
    },
]

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
        "name": "Raw HP Up",
        "note": "Permanently increases the player's HP.",
        "param1": "HP Increase."
    },
    {
        "id": 0x1006,
        "name": "Raw BP Up",
        "note": "Permanently increases the player's BP.",
        "param1": "BP Increase."
    },
    {
        "id": 0x1007,
        "name": "Raw POW Up",
        "note": "Permanently increases the player's POW.",
        "param1": "POW Increase."
    },
    {
        "id": 0x1008,
        "name": "Raw DEF Up",
        "note": "Permanently increases the player's DEF.",
        "param1": "DEF Increase."
    },
    {
        "id": 0x1009,
        "name": "Raw SPEED Up",
        "note": "Permanently increases the player's SPEED.",
        "param1": "SPEED Increase."
    },
    {
        "id": 0x100A,
        "name": "Raw STACHE Up",
        "note": "Permanently increases the player's STACHE.",
        "param1": "STACHE Increase."
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

ML5_UITM_CONDITION = [
    { "id":  0, "name": "No condition" },
    { "id":  1, "name": "Missing HP" },
    { "id":  2, "name": "Missing BP" },
    { "id":  3, "name": "Is KO'd" },
    { "id":  4, "name": "Negative status" },
    { "id":  5, "name": "Missing HP or BP" },
    { "id":  6, "name": "Everyone can act" },
    { "id":  7, "name": "HP can be increased" },
    { "id":  8, "name": "BP can be increased" },
    { "id":  9, "name": "POW can be increased" },
    { "id": 10, "name": "DEF can be increased" },
    { "id": 11, "name": "SPEED can be increased" },
    { "id": 12, "name": "STACHE can be increased" },
    { "id": 13, "name": "Background Enemy" },
]

ML3R_UITM_CONDITION = [
    { "id":  0, "name": "No condition" },
    { "id":  1, "name": "Missing HP" },
    { "id":  2, "name": "Missing BP" },
    { "id":  3, "name": "Is KO'd" },
    { "id":  4, "name": "Negative status" },
    { "id":  5, "name": "Missing HP or BP" },
    { "id":  6, "name": "HP can be increased" },
    { "id":  7, "name": "BP can be increased" },
    { "id":  8, "name": "POW can be increased" },
    { "id":  9, "name": "DEF can be increased" },
    { "id": 10, "name": "SPEED can be increased" },
    { "id": 11, "name": "STACHE can be increased" },
    { "id": 12, "name": "Unused" },
    { "id": 13, "name": "Everyone can act" },
]


