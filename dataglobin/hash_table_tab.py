from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
)
from dataglobin import data as Data
from dataglobin import hash_presets as Presets
from dataglobin.data import GameID

class HashTableTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self.description_label = QLabel(
            "Paper Jam, Superstar Saga + Bowser's Minions, and Bowser's Inside Story + Bowser Jr.'s Journey use custom strings to identify items. These strings are stored as hashes in the game's database and are used for things like treasure, monster drops, and in Paper Jam, shops. Only edit these if you're adding new items."
        )
        self.description_label.setWordWrap(True)
        layout.addWidget(self.description_label)

        self.hash_table_combo = QComboBox()
        self.hash_table_combo.addItem("UITM - Consumable Items", "UITM")
        layout.addWidget(self.hash_table_combo)

        self.bucket_count_label = QLabel("Bucket count: 0")
        layout.addWidget(self.bucket_count_label)

        self.hash_table = QTableWidget(0, 6)
        self.hash_table.setHorizontalHeaderLabels(["ID", "NAME", "STRING", "LAST_CH", "LENGTH", "BUCKET"])
        self.hash_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.hash_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.hash_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.hash_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        header = self.hash_table.horizontalHeader()
        for column in (0, 1, 3, 4, 5):
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.hash_table, 1)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.import_button = QPushButton("Import")
        self.export_button = QPushButton("Export")
        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.export_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_table()

    def refresh_table(self):
        self.hash_table.setRowCount(0)

        table_key = self.hash_table_combo.currentData()
        hash_table = Data.HASH_TABLE.get(table_key)

        if hash_table is None:
            self.bucket_count_label.setText("Bucket count: 0")
            return

        self.bucket_count_label.setText(
            f"Bucket count: {hash_table.bucket_amount}"
        )

        presets = {}
        if Data.GAME_VERSION == GameID.ML3R:
            presets = Presets.ML3R_UITM_STR
        if Data.GAME_VERSION == GameID.ML5:
            presets = Presets.ML5_UITM_STR

        # Hash entries use the ID without the item's category prefix
        entries_by_id = {entry.id: entry for entry in hash_table.entries}

        self.hash_table.setRowCount(len(Data.ITEMS))
        for row, item in enumerate(Data.ITEMS):
            item_id = item.id
            item_id_text = f"{item_id:04X}"
            item_name = item.getDefaultName()

            self._set_cell(row, 0, item_id_text)
            self._set_cell(row, 1, item_name)

            entry_id = item_id & 0x0FFF
            entry = entries_by_id.get(entry_id)

            if entry is None:
                continue
            self._set_cell(row, 2, self._find_matching_preset(presets, entry, hash_table))
            self._set_cell(row, 3, str(entry.last_char))
            self._set_cell(row, 4, str(entry.length))
            self._set_cell(row, 5, str(entry.bucket_id))

    def _find_matching_preset(self, presets, entry, hash_table):
        for item_id, value in presets.items():
            if (item_id & 0x0FFF) != entry.id:
                continue
            if hash_table.compute_metadata(value) == (entry.bucket_id, entry.last_char, entry.length):
                return value
        return "Unknown"

    def _set_cell(self, row, column, value):
        cell = QTableWidgetItem(str(value))
        if column in (0, 3, 4, 5):
            cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hash_table.setItem(row, column, cell)