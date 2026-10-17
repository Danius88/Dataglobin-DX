import sys
import json
from enum import Enum
from pathlib import Path

from PySide6 import QtCore

import dataglobin.constants as Constants
from dataglobin.constants import GameID, Language

LAST_VERSION = Constants.DEFAULT_VERSION

# Dataglobin-DX UI language
UI_LANGUAGE = Language.US_EN
# Language used for the item name lists
UI_DB_LANGUAGE = None

ML3R_ROMFS_INPUT = None
ML3R_ROMFS_OUTPUT = None

ML1R_ROMFS_INPUT = None
ML1R_ROMFS_OUTPUT = None

ML5_ROMFS_INPUT = None
ML5_ROMFS_OUTPUT = None

CONFIG_PATH = Path(
    QtCore.QStandardPaths.writableLocation(
        QtCore.QStandardPaths.StandardLocation.AppConfigLocation
    )
) / "config.json"

def _serialize(value):
    if isinstance(value, Enum):
        return {"__enum__": value.__class__.__name__, "name": value.name}
    if isinstance(value, Path):
        return str(value)
    return value

def _deserialize(value):
    if isinstance(value, dict) and "__enum__" in value:
        enum_classes = {
            cls.__name__: cls
            for cls in (GameID, Language)
        }
        enum_cls = enum_classes[value["__enum__"]]
        return enum_cls[value["name"]]
    return value

def get_config_path() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent / "config.json"
    return Path(
        QtCore.QStandardPaths.writableLocation(
            QtCore.QStandardPaths.StandardLocation.AppConfigLocation
        )
    ) / "config.json"

def export_config():
    config = {
        "LAST_VERSION": _serialize(LAST_VERSION),
        
        "ML5_ROMFS_INPUT": _serialize(ML5_ROMFS_INPUT),
        "ML5_ROMFS_OUTPUT": _serialize(ML5_ROMFS_OUTPUT),

        "ML1R_ROMFS_INPUT": _serialize(ML1R_ROMFS_INPUT),
        "ML1R_ROMFS_OUTPUT": _serialize(ML1R_ROMFS_OUTPUT),

        "ML3R_ROMFS_INPUT": _serialize(ML3R_ROMFS_INPUT),
        "ML3R_ROMFS_OUTPUT": _serialize(ML3R_ROMFS_OUTPUT),
    }
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(config, indent=4),
        encoding="utf-8",
    )

def import_config():
    config_path = get_config_path()
    if not config_path.exists():
        return
    config = json.loads(config_path.read_text(encoding="utf-8"))
    for name, value in config.items():
        if name.isupper() and name in globals():
            globals()[name] = _deserialize(value)