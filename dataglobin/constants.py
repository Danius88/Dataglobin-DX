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

ML1R_UITM_CONDITION = [
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
    { "id": 12, "name": "Any stat can be increased" },
    { "id": 13, "name": "Everyone can act" },
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

ML3R_EITM_CATEGORY = [
    { "id":  0, "name": "Wear" },
    { "id":  1, "name": "Socks" },
    { "id":  2, "name": "Gloves" },
    { "id":  3, "name": "Boots" },
    { "id":  4, "name": "Accessory" },
    { "id":  5, "name": "Shell" },
    { "id":  6, "name": "Bracelet" },
    { "id":  7, "name": "Fangs" },
    { "id":  8, "name": "Ring" },
]

ML5_EITM_CATEGORY = [
    { "id":  0, "name": "Boots" },
    { "id":  1, "name": "Hammer" },
    { "id":  2, "name": "Wear" },
    { "id":  3, "name": "Gloves" },
    { "id":  4, "name": "Accessory" },
]

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

ML1R_EFFECTS_UITM = [
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
        "name": "Raw Random Up",
        "note": "Permanently increases a random player's stat.",
        "param1": "Stat Increase."
    },
    {
        "id": 0x100C,
        "name": "POW-UP Status",
        "note": "Inflicts POW-UP and Heavy G status.",
        "param1": "POW-UP status modifier."
    },
    {
        "id": 0x100D,
        "name": "DEF-UP Status",
        "note": "Inflicts DEF-UP and Light G status.",
        "param1": "DEF-UP status modifier."
    },
    {
        "id": 0x100E,
        "name": "Boo Biscuit",
        "note": "Makes the player invincible for a certain amount of turns.",
        "param1": "Turn duration."
    }
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

ML1R_EFFECTS_WITM = [
    {
        "id": 0x2000,
        "name": "No Effect",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2001,
        "name": "HP-Auto Gain",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2002,
        "name": "After Mario",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2003,
        "name": "Before Mario",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2004,
        "name": "First Attack",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2005,
        "name": "Poison Dodge",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2006,
        "name": "LIGHT G",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2007,
        "name": "HEAVY G",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2008,
        "name": "RANDOM G",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2009,
        "name": "DEF-Up",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x200A,
        "name": "Win Mushroom",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x200B,
        "name": "Lucky Mushroom",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x200C,
        "name": "POW-Up Risky",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x200D,
        "name": "Speedy Guard",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x200E,
        "name": "Lucky Critical",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x200F,
        "name": "Guard Guardian",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2010,
        "name": "Emergency DEF",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2011,
        "name": "Barrier Guard",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2012,
        "name": "Barrier Guard",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2013,
        "name": "Mushroom Recover",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2014,
        "name": "One-Turn Recover",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2015,
        "name": "Emergency Guard",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2016,
        "name": "SPEED Up Badgeless",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x2017,
        "name": "Sweet Revenge",
        "note": "",
        "param1": "",
    }
]

ML1R_EFFECTS_BITM = [
    {
        "id": 0x3000,
        "name": "No Effect",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3001,
        "name": "Power-D",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3002,
        "name": "Spiny-Killer Jump",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3003,
        "name": "BP-Auto Gain",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3004,
        "name": "HP-Up Jump",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3005,
        "name": "HP-Up Hammer",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3006,
        "name": "HP-Up Hand",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3007,
        "name": "Lucky Attack",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3008,
        "name": "POW-Up",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3009,
        "name": "Shroom Force",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x300A,
        "name": "Item Grab",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x300B,
        "name": "First Striker",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x300C,
        "name": "Lucky Speedster",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x300D,
        "name": "POW-Up Squad",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x300E,
        "name": "Strong Start",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x300F,
        "name": "BURN Counter",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3010,
        "name": "Heavy Jump",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3011,
        "name": "LIGHT G SPEED Boost",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3012,
        "name": "Bean Collector",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3013,
        "name": "POW-Up Natural",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3014,
        "name": "BP-Recover Counter",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3015,
        "name": "BP-Recover Excellent",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x3016,
        "name": "Eb_",
        "note": "",
        "param1": "",
    },
]

ML1R_EFFECTS_SITM = [
    {
        "id": 0x4000,
        "name": "Extra Coins",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x4001,
        "name": "Flawless Victory EXP Bonus",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x4002,
        "name": "Floaty Jump",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x4003,
        "name": "Damage Up",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x4004,
        "name": "Block Hunter",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x4005,
        "name": "Double STACHE",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x4006,
        "name": "Item Fiend",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x4007,
        "name": "Jump Master",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x4008,
        "name": "Quick Win Bonus",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x4009,
        "name": "Critical Stat Change",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x400A,
        "name": "POW/SPEED Swap",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x400B,
        "name": "All Excellent",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x400C,
        "name": "Gravity Guard",
        "note": "",
        "param1": "",
    },
    {
        "id": 0x400D,
        "name": "Hand Master",
        "note": "",
        "param1": "",
    }
]

ML3R_EFFECTS_EITM = [
    {
        "id": 0x2000,
        "name": "No Effect",
        "note": "N/A",
        "param1": "N/A",
        "param2": "N/A"
    },
    {
        "id": 0x2001,
        "name": "Ew_HPUP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2002,
        "name": "Ew_SPUP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2003,
        "name": "Ew_POWUP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2004,
        "name": "Ew_DEFUP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2005,
        "name": "Ew_SPEEDUP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2006,
        "name": "Ew_HIGEUP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2007,
        "name": "Poison Dodge",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2008,
        "name": "Ew_RESI_YAKEDO",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2009,
        "name": "Ew_RESI_KAZE",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x200A,
        "name": "Ew_RESI_MEMAWASHI",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x200B,
        "name": "Ew_ABNORMAL_CANCELER",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x200C,
        "name": "Ew_POW_BROS",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x200D,
        "name": "Ew_POW_BROS",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x200E,
        "name": "Ew_POW_HAMMER",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x200F,
        "name": "Ew_POW_JUMP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2010,
        "name": "Ew_POW_JUMP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2011,
        "name": "Ew_POW_FIRE",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2012,
        "name": "Ew_POW_KOURA",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2013,
        "name": "Ew_POW_FLOW",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2014,
        "name": "Ew_FULLHP_POW",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2015,
        "name": "Ew_HARAHARA_POW",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2016,
        "name": "Ew_DAM_POW",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2017,
        "name": "Ew_KILL_POW",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2018,
        "name": "Ew_POW_OKORI",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2019,
        "name": "Ew_IRAIRA",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x201A,
        "name": "Emergency DEF",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x201B,
        "name": "Damage Up",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x201C,
        "name": "POW-Up Natural",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x201D,
        "name": "HP-Auto Gain",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x201E,
        "name": "BP-Auto Gain",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x201F,
        "name": "Ew_HPSP_RECOVER",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2020,
        "name": "Ew_HPSP_RECOVER",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2021,
        "name": "Ew_HPSP_RECOVER",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2022,
        "name": "Ew_EASY_HAMMER",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2023,
        "name": "Ew_EASY_JUMP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2024,
        "name": "Ew_EASY_PUNCH",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2025,
        "name": "Ew_EASY_FIRE",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2026,
        "name": "Ew_EASY_VACUUM",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2027,
        "name": "Ew_MEMAWASI_JUMP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2028,
        "name": "Ew_POWDOWN_JUMP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2029,
        "name": "Ew_COINGET_JUMP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x202A,
        "name": "Ew_DEFDOWN_HAMMER",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x202B,
        "name": "Ew_ITEMGET_HAMMER",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x202C,
        "name": "HP-Up Jump",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x202D,
        "name": "Ew_HP_JUMP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x202E,
        "name": "Ew_SP_HAMMER",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x202F,
        "name": "Ew_HP_PUNCH",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2030,
        "name": "Ew_EXCELLENT_CHARGE",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2031,
        "name": "Ew_EX_HP_HEAL",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2032,
        "name": "Ew_EX_SP_HEAL",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2033,
        "name": "Ew_HEAT_FIRE",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2034,
        "name": "Ew_REPEAT_ACT",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2035,
        "name": "Lucky Mushroom",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2036,
        "name": "Lucky Critical",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2037,
        "name": "Critical Stat Change",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2038,
        "name": "All Excellent",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2039,
        "name": "Shroom Force",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x203A,
        "name": "First Striker",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x203B,
        "name": "Ew_VACUUM_MAME",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x203C,
        "name": "Ew_VACUUM_POWUP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x203D,
        "name": "Ew_LUCKY_CHARGE",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x203E,
        "name": "Ew_DETH_HAMMER",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x203F,
        "name": "Ew_DETH_PUNCH",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2040,
        "name": "Ew_SETUYAKU_SP_RND",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2041,
        "name": "Ew_SETUYAKU_SP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2042,
        "name": "Ew_BOOTH_BROS",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2043,
        "name": "Ew_HALVE_SP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2044,
        "name": "Barrier Guard",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2045,
        "name": "Ew_AUTO_KINOKO",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2046,
        "name": "Guard Guardian",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2047,
        "name": "Auto Guard",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2048,
        "name": "Speedy Guard",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2049,
        "name": "Emergency Guard",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x204A,
        "name": "Ew_COUNTER_CHARGE",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x204B,
        "name": "Jump Master",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x204C,
        "name": "Power-D",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x204D,
        "name": "BURN Counter",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x204E,
        "name": "BP-Recover Counter",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x204F,
        "name": "Ew_POWUP_KINOKO",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2050,
        "name": "Ew_DEFUP_KINOKO",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2051,
        "name": "Ew_BOOTH_KINOKO",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2052,
        "name": "Ew_ITEMPOWUP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2053,
        "name": "Mushroom Cure",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2054,
        "name": "Ew_HUTTOBI_COINUP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2055,
        "name": "Ew_NODAM_COIN",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2056,
        "name": "Flawless Victory EXP Bonus",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2057,
        "name": "Ew_BARI_HISSATU",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2058,
        "name": "Ew_HETARE_DEF",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2059,
        "name": "Ew_ONBU_BARRIOR",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x205A,
        "name": "One-Turn Recover",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x205B,
        "name": "Sweet Revenge",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x205C,
        "name": "Quick Win Bonus",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x205D,
        "name": "Ew_FULLGAUGE_BP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x205E,
        "name": "Ew_FULLGAUGE_POWUP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x205F,
        "name": "Ew_FULLGAUGE_ALLUP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2060,
        "name": "Win Mushroom",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2061,
        "name": "Item Fiend",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2062,
        "name": "Ew_OTAKARAUP",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2063,
        "name": "Bean Collector",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2064,
        "name": "BP-Recover Excellent",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2065,
        "name": "POW-Up Risky",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2066,
        "name": "Strong Start",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2067,
        "name": "Ew_POW_NAGURI",
        "note": "",
        "param1": "",
        "param2": ""
    },
    {
        "id": 0x2068,
        "name": "Ew_POW_FUMI",
        "note": "",
        "param1": "",
        "param2": ""
    },
]

ML5_EFFECTS_CITM = [
    {
        "id": 0,
        "name": "No Effect",
        "note": "N/A",
        "param1": "N/A",
        "param2": "N/A"
    },
]