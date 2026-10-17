from functools import partial
from PySide6 import QtCore, QtGui, QtMultimedia, QtWidgets
import dataglobin.persistent as Persistent
import dataglobin.constants as Constants
import dataglobin.data as Data

from dataglobin.constants import *
from dataglobin.tab_effect_strings import EffectStringsTab
from dataglobin.tab_item_data import ItemDataTab
from dataglobin.tab_hash_table import HashTableTab

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle(APP_DISPLAY_NAME)
        self.setWindowIcon(QtGui.QIcon(str(FILES_DIR / "dataglobin.ico")))

        self.success_sfx = QtMultimedia.QSoundEffect(self)
        self.success_sfx.setSource(QtCore.QUrl.fromLocalFile(str(FILES_DIR / "dataglobin_success.wav")))
        self.success_sfx.setVolume(0.3)

        menu_bar = self.menuBar()
        menu_bar_file = menu_bar.addMenu("&File")

        menu_bar_file.addAction(
            "&Open ML5 romfs",
            partial(self.open_romfs_directory, GameID.ML5),
        )

        menu_bar_file.addAction(
            "&Open ML1R romfs",
            partial(self.open_romfs_directory, GameID.ML1R),
        )

        menu_bar_file.addAction(
            "&Open ML3R romfs",
            partial(self.open_romfs_directory, GameID.ML3R),
        )

        menu_bar_file.addSeparator()

        self.export_data_action = menu_bar_file.addAction(
            "&Export Data",
            QtGui.QKeySequence.StandardKey.Save,
            partial(self.export_data),
        )
        self.export_data_action.setEnabled(False)

        menu_bar_file.addSeparator()
        menu_bar_file.addAction("&Quit", QtGui.QKeySequence.StandardKey.Quit, QtWidgets.QApplication.quit)

        self.program_is_already_open = False
        Data.GAME_VERSION = Persistent.LAST_VERSION
        self.init_ui(Persistent.LAST_VERSION)
        self.test_ML3R()

    def open_romfs_directory(self, version: GameID):
        input_dirs = {
            GameID.ML3R: Persistent.ML3R_ROMFS_INPUT,
            GameID.ML1R: Persistent.ML1R_ROMFS_INPUT,
            GameID.ML5: Persistent.ML5_ROMFS_INPUT,
        }
        directory = input_dirs.get(version)
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,
            "Open romfs directory",
            str(directory) if directory else "",
        )
        if directory:
            self.init_ui(version, Path(directory))

    def export_data(self):
        output_dirs = {
            GameID.ML3R: Persistent.ML3R_ROMFS_OUTPUT,
            GameID.ML1R: Persistent.ML1R_ROMFS_OUTPUT,
            GameID.ML5: Persistent.ML5_ROMFS_OUTPUT,
        }
        if Data.GAME_VERSION in output_dirs:
            directory = output_dirs[Data.GAME_VERSION]
            directory = QtWidgets.QFileDialog.getExistingDirectory(
                self,
                "Select output directory",
                str(directory) if directory else "",
            )
            if not directory:
                return
            
            Data.export_data(directory)
            Persistent.export_config()
            QtWidgets.QMessageBox.information(
                self,
                "Export Complete",
                f"Data exported successfully.\n\nLocation:\n{directory}",
            )

    def init_ui(self, version: GameID = GameID.UNK, rom_path: Path | None = None):
        if rom_path is not None:
            Data.load_data(version, rom_path)
            Data.GAME_VERSION = version
            self.export_data_action.setEnabled(True)
            Persistent.LAST_VERSION = version
            Persistent.export_config()
        main = QtWidgets.QTabWidget()
        if version in (GameID.ML3R, GameID.ML1R, GameID.ML5):
            # Consumable Items
            self.item_data_tab = ItemDataTab(self, item_key="UITM")
            main.addTab(self.item_data_tab, "&Item Data")
            # Gear
            if version in (GameID.ML3R, GameID.ML5):
                self.gear_data_tab = ItemDataTab(self, item_key="EITM")
                main.addTab(self.gear_data_tab, "&Gear Data")
            elif version == GameID.ML1R:
                self.wear_data_tab = ItemDataTab(self, item_key="WITM")
                main.addTab(self.wear_data_tab, "&Wear Data")
            
            if version == GameID.ML5:
                self.card_data_tab = ItemDataTab(self, item_key="CITM")
                #main.addTab(self.card_data_tab, "&Card Data")

            # Effect Strings
            if version in (GameID.ML1R, GameID.ML3R):
                self.effect_strings_tab = EffectStringsTab(self)
                main.addTab(self.effect_strings_tab, "&Effect Strings")
            # Hash Tables
            self.hash_table_tab = HashTableTab(self)
            main.addTab(self.hash_table_tab, "&Hash Tables")
        self.setCentralWidget(main)

    def test_ML3R(self):
        self.init_ui(GameID.ML3R, Path(r"C:/mnl/ML3R/romfs"))

    def test_ML1R(self):
        self.init_ui(GameID.ML1R, Path(r"C:/mnl/ML1R/romfs"))

    def test_ML5(self):
        self.init_ui(GameID.ML5, Path(r"C:/mnl/ML5/romfs"))