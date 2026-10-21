import sys
from enum import Enum
from pathlib import Path

from PySide6 import QtCore

import dataglobin.constants as Constants
from dataglobin.constants import GameID, Language

LAST_VERSION = Constants.DEFAULT_VERSION

UI_LANGUAGE = Language.US_EN
UI_DB_LANGUAGE = None

ML3R_ROMFS_INPUT = None
ML3R_ROMFS_OUTPUT = None

ML1R_ROMFS_INPUT = None
ML1R_ROMFS_OUTPUT = None

ML5_ROMFS_INPUT = None
ML5_ROMFS_OUTPUT = None


def get_config_path() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / "config.ini"
    return (
        Path(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.AppConfigLocation))
        / "config.ini"
    )

def export_config() -> None:
    settings = QtCore.QSettings(str(get_config_path()), QtCore.QSettings.Format.IniFormat)
    config = {
        "LAST_VERSION": LAST_VERSION,
        "ML5_ROMFS_INPUT": ML5_ROMFS_INPUT,
        "ML5_ROMFS_OUTPUT": ML5_ROMFS_OUTPUT,
        "ML1R_ROMFS_INPUT": ML1R_ROMFS_INPUT,
        "ML1R_ROMFS_OUTPUT": ML1R_ROMFS_OUTPUT,
        "ML3R_ROMFS_INPUT": ML3R_ROMFS_INPUT,
        "ML3R_ROMFS_OUTPUT": ML3R_ROMFS_OUTPUT,
    }
    for key, value in config.items():
        if value is None:
            value = ""
        elif isinstance(value, Enum):
            value = value.name
        elif isinstance(value, Path):
            value = str(value)
        settings.setValue(key, value)
    settings.sync()

def import_config() -> None:
    global LAST_VERSION
    global ML5_ROMFS_INPUT, ML5_ROMFS_OUTPUT
    global ML1R_ROMFS_INPUT, ML1R_ROMFS_OUTPUT
    global ML3R_ROMFS_INPUT, ML3R_ROMFS_OUTPUT

    settings = QtCore.QSettings(str(get_config_path()), QtCore.QSettings.Format.IniFormat)

    def read(key, default=None, converter=None):
        value = settings.value(key, default)
        if converter is Path:
            return Path(value) if value else None
        if isinstance(converter, type) and issubclass(converter, Enum):
            if isinstance(value, converter):
                return value
            if not value:
                return default
            return converter[value]
        return value

    LAST_VERSION = read("LAST_VERSION", Constants.DEFAULT_VERSION, GameID)

    ML5_ROMFS_INPUT = read("ML5_ROMFS_INPUT", converter=Path)
    ML5_ROMFS_OUTPUT = read("ML5_ROMFS_OUTPUT", converter=Path)

    ML1R_ROMFS_INPUT = read("ML1R_ROMFS_INPUT", converter=Path)
    ML1R_ROMFS_OUTPUT = read("ML1R_ROMFS_OUTPUT", converter=Path)

    ML3R_ROMFS_INPUT = read("ML3R_ROMFS_INPUT", converter=Path)
    ML3R_ROMFS_OUTPUT = read("ML3R_ROMFS_OUTPUT", converter=Path)