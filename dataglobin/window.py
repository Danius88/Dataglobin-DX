import os
import io
import sys
import struct
from functools import partial
from random import choice
from PySide6 import QtCore, QtGui, QtMultimedia, QtWidgets
import ndspy.rom
import ndspy.code
from mnllib.bis import LanguageTable, TextTable, BIS_ENCODING
import dataglobin.persistent as Persistent
import dataglobin.constants as Constants
import dataglobin.data as Data

# BIS_ENCODING = "shift_jis"

from dataglobin.constants import *
from dataglobin.tab_enemy_data import EnemyDataTab
from dataglobin.tab_item_data import ItemDataTab

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle(APP_DISPLAY_NAME)
        self.setWindowIcon(QtGui.QIcon(str(FILES_DIR / "dataglobin.ico")))

        self.success_sfx = QtMultimedia.QSoundEffect(self)
        self.success_sfx.setSource(
            QtCore.QUrl.fromLocalFile(str(FILES_DIR / "dataglobin_success.wav"))
        )
        self.success_sfx.setVolume(0.3)

        menu_bar = self.menuBar()
        menu_bar_file = menu_bar.addMenu("&File")

        menu_bar_file.addAction(
            "&Open BISDX romfs directory",
            QtGui.QKeySequence.StandardKey.Open,
            partial(self.open_romfs_directory, GameID.ML3R),
        )

        menu_bar_file.addSeparator()
        menu_bar_file.addAction(
            "&Quit",
            QtGui.QKeySequence.StandardKey.Quit,
            QtWidgets.QApplication.quit,
        )

        self.program_is_already_open = False
        Data.GAME_VERSION = Persistent.LAST_VERSION
        self.init_ui()
        self.test_ML3R()

    def open_romfs_directory(self, version: GameID):
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Open BISDX romfs directory",
        )
        if directory:
            self.init_ui(version, Path(directory))

    def init_ui(self, version: GameID = GameID.UNK, rom_path: Path | None = None):
        if rom_path is not None:
            Data.GAME_VERSION = version
            Data.load_data(rom_path)
            

        main = QtWidgets.QTabWidget()
        self.item_data_tab = ItemDataTab(self)
        self.enemy_data_tab = EnemyDataTab(self)

        main.addTab(self.item_data_tab, "&Item Data")
        main.addTab(self.enemy_data_tab, "&Enemy Data")

        self.setCentralWidget(main)


    def test_ML3R(self):
        self.init_ui(GameID.ML3R, Path(r"C:/mnl/ML3R"))