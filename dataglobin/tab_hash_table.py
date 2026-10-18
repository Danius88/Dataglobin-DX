import json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
)
from dataglobin import data as Data
from dataglobin import hash_presets as Presets
from dataglobin.data import GameID

class HashTableTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.version = Data.GAME_VERSION

        self.HASH_TABLE_PRESETS = {
            GameID.ML3R: {
                "UITM": {
                    "label": "UITM - Usable Items",
                    "presets": Presets.ML3R_UITM_STR,
                },
                "EITM": {
                    "label": "EITM - Equippable Items",
                    "presets": Presets.ML3R_EITM_STR,
                },
            },
            GameID.ML1R: {
                "UITM": {
                    "label": "UITM - Usable Items",
                    "presets": Presets.ML1R_UITM_STR,
                },
                "WITM": {
                    "label": "WITM - Wear Items",
                    "presets": Presets.ML1R_WITM_STR,
                },
                "BITM": {
                    "label": "BITM - Badge Items",
                    "presets": Presets.ML1R_BITM_STR,
                },
                "SITM": {
                    "label": "SITM - Special Items",
                    "presets": Presets.ML1R_SITM_STR,
                },
                "EITM": {
                    "label": "EITM - Event Items",
                    "presets": Presets.ML1R_EITM_STR,
                },
                "BEAN": {
                    "label": "BEAN - Bean Items",
                    "presets": Presets.ML1R_BEAN_STR,
                },
            },
            GameID.ML5: {
                "UITM": {
                    "label": "UITM - Consumable Items",
                    "presets": Presets.ML5_UITM_STR,
                },
                "EITM": {
                    "label": "EITM - Equippable Items",
                    "presets": Presets.ML5_EITM_STR,
                },
            },
        }

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self.description_label = QLabel(
            "Paper Jam, Superstar Saga + Bowser's Minions, and Bowser's Inside Story + Bowser Jr.'s Journey use custom strings to identify items. These strings are stored as hashes in the game's database and are used for things like treasure, monster drops, and in Paper Jam, shops. Only edit these if you're adding new items."
        )
        self.description_label.setWordWrap(True)
        layout.addWidget(self.description_label)

        self.hash_table_combo = QComboBox()
        self.refresh_hash_table_options()
        self.hash_table_combo.currentIndexChanged.connect(self.refresh_table)
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
        self.export_button = QPushButton("Export JSON")
        self.import_button = QPushButton("Import JSON")
        self.export_button.clicked.connect(self.export_json)
        self.import_button.clicked.connect(self.import_json)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.import_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_table()

    def refresh_table(self):
        self.hash_table.setRowCount(0)

        table_key = self.hash_table_combo.currentData()
        version_presets = self.HASH_TABLE_PRESETS.get(self.version, {})
        config = version_presets.get(table_key)

        if config is None:
            self.bucket_count_label.setText("Bucket count: 0")
            return

        hash_table = Data.HASH_TABLE.get(table_key)
        if hash_table is None:
            self.bucket_count_label.setText("Bucket count: 0")
            return

        self.bucket_count_label.setText(
            f"Bucket count: {hash_table.bucket_amount}"
        )

        presets = config["presets"]
        items = Data.ITEMDATA[table_key]

        entries_by_id = {
            entry.id: entry for entry in hash_table.entries
        }

        self.hash_table.setRowCount(len(items))

        for row, item in enumerate(items):
            item_id = item.id
            item_id_text = f"{item_id:04X}"
            item_name = item.getDefaultName()

            self._set_cell(row, 0, item_id_text)
            self._set_cell(row, 1, item_name)

            entry_id = item_id & 0x0FFF
            entry = entries_by_id.get(entry_id)

            if entry is None:
                continue

            self._set_cell(
                row, 2,
                self._find_matching_preset(presets, entry, hash_table),
            )
            self._set_cell(row, 3, str(entry.last_char))
            self._set_cell(row, 4, str(entry.length))
            self._set_cell(row, 5, str(entry.bucket_id))

    def refresh_hash_table_options(self):
        self.hash_table_combo.clear()
        version_presets = self.HASH_TABLE_PRESETS.get(self.version, {})
        for table_key, config in version_presets.items():
            self.hash_table_combo.addItem(config["label"], table_key)

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


    def export_json(self):
        table_key = self.hash_table_combo.currentData()
        config = self.HASH_TABLE_PRESETS.get(self.version, {}).get(table_key)
        hash_table = Data.HASH_TABLE.get(table_key)

        if config is None or hash_table is None:
            QMessageBox.warning(self, "Export JSON", "The current hash table is empty.")
            return

        presets = config["presets"]
        entries_by_id = {entry.id: entry for entry in hash_table.entries}
        strings, known_entry_ids = [], set()

        for item in Data.ITEMDATA[table_key]:
            entry_id = item.id & 0x0FFF
            entry = entries_by_id.get(entry_id)
            if entry is None:
                continue

            value = self._find_matching_preset(presets, entry, hash_table)
            if value == "Unknown":
                continue

            strings.append({"id": entry_id, "value": value})
            known_entry_ids.add(entry_id)

        unknown_entries = [
            {"id": entry.id, "bucket": entry.bucket_id,
            "last_char": entry.last_char, "length": entry.length}
            for entry in hash_table.entries if entry.id not in known_entry_ids
        ]

        export_data = {
            "bucket_count": hash_table.bucket_amount,
            "strings": strings,
            "unknown_entries": unknown_entries,
        }

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Hash Table", f"{table_key}.json", "JSON Files (*.json)"
        )
        if not file_path:
            return
        if not file_path.lower().endswith(".json"):
            file_path += ".json"

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(export_data, file, indent=4, ensure_ascii=False)
                file.write("\n")
        except OSError as error:
            QMessageBox.critical(self, "Export JSON", f"Failed to export hash table:\n{error}")


    def import_json(self):
        table_key = self.hash_table_combo.currentData()
        config = self.HASH_TABLE_PRESETS.get(self.version, {}).get(table_key)
        current_table = Data.HASH_TABLE.get(table_key)

        if config is None or current_table is None:
            QMessageBox.warning(self, "Import JSON", "The current hash table is empty.")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Hash Table", "", "JSON Files (*.json)"
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError) as error:
            QMessageBox.critical(self, "Import JSON", f"Failed to read JSON:\n{error}")
            return

        # Validate the JSON structure.
        if not isinstance(data, dict) or set(data) != {
            "bucket_count", "strings", "unknown_entries"
        }:
            QMessageBox.critical(self, "Import JSON", "Invalid JSON format.")
            return

        bucket_count = data["bucket_count"]
        strings = data["strings"]
        unknown_entries = data["unknown_entries"]

        if (type(bucket_count) is not int or bucket_count <= 0
                or not isinstance(strings, list)
                or not isinstance(unknown_entries, list)):
            QMessageBox.critical(self, "Import JSON", "Invalid JSON data types or bucket count.")
            return

        if bucket_count != current_table.bucket_amount and unknown_entries:
            QMessageBox.critical(
                self, "Import JSON",
                "The bucket count differs from the current table, but unresolved entries exist. "
                "Their original strings are unknown, so their hashes cannot be recalculated."
            )
            return

        new_entries = []
        seen_ids = set()

        try:
            # Recalculate strings using the new bucket count
            calculator = Data.HashTable(bucket_count, [])

            for item in strings:
                if (not isinstance(item, dict) or set(item) != {"id", "value"}
                        or type(item["id"]) is not int or not 0 <= item["id"] <= 0x0FFF
                        or not isinstance(item["value"], str) or not item["value"]):
                    raise ValueError("Invalid string entry.")

                entry_id, value = item["id"], item["value"]
                if entry_id in seen_ids:
                    raise ValueError(f"Duplicate entry ID: {entry_id}")

                seen_ids.add(entry_id)
                bucket, last_char, length = calculator.compute_metadata(value)
                new_entries.append(Data.HashEntry(entry_id, length, last_char, bucket))

            # Preserve unknown entries when the bucket count matches
            for item in unknown_entries:
                if (not isinstance(item, dict)
                        or set(item) != {"id", "bucket", "last_char", "length"}
                        or type(item["id"]) is not int or not 0 <= item["id"] <= 0x0FFF
                        or type(item["bucket"]) is not int
                        or not 0 <= item["bucket"] < bucket_count
                        or not isinstance(item["last_char"], str)
                        or len(item["last_char"]) != 1
                        or type(item["length"]) is not int or item["length"] <= 0):
                    raise ValueError("Invalid unknown entry.")

                entry_id = item["id"]
                if entry_id in seen_ids:
                    raise ValueError(f"Duplicate entry ID: {entry_id}")

                seen_ids.add(entry_id)
                new_entries.append(Data.HashEntry(
                    entry_id, item["length"], item["last_char"], item["bucket"]
                ))

            # Check duplicated entries in the same bucket
            seen_metadata = {}
            for entry in new_entries:
                metadata = (entry.bucket_id, entry.length, entry.last_char)
                if metadata in seen_metadata:
                    previous_id = seen_metadata[metadata]
                    raise ValueError(
                        f"Duplicate hash metadata in bucket {entry.bucket_id}: "
                        f"length {entry.length}, last character {entry.last_char!r}. "
                        f"Entry IDs: {previous_id} and {entry.id}."
                    )
                seen_metadata[metadata] = entry.id

            # Binary validations
            if not 0 < bucket_count <= 0xFFFF:
                raise ValueError(f"The bucket count {bucket_count} is too large.")

            header_size = 2 + (bucket_count + 1) * 2
            total_size = header_size + len(new_entries) * 4
            if total_size > 0xFFFF:
                raise ValueError(f"Hash table size {total_size} exceeds the maximum representable bucket offset (65535 bytes).")

            for entry in new_entries:
                if not 0 <= entry.id <= 0xFFFF:
                    raise ValueError(f"Invalid entry ID: {entry.id}")
                if not 0 <= entry.length <= 0xFF:
                    raise ValueError(f"Invalid entry length for ID {entry.id}: {entry.length}")
                try:
                    last_char = entry.last_char.encode("ascii")
                except UnicodeEncodeError as error:
                    raise ValueError(f"Invalid last character for ID {entry.id}: "f"{entry.last_char!r}") from error
                if len(last_char) != 1:
                    raise ValueError(f"Last character for ID {entry.id} must encode to exactly one byte.")
        
        except (ValueError, TypeError, KeyError) as error:
            QMessageBox.critical(self, "Import JSON", f"Validation failed:\n{error}")
            return

        Data.HASH_TABLE[table_key] = Data.HashTable(bucket_count, new_entries)
        self.refresh_table()

        QMessageBox.information(
            self, "Import JSON",
            f"Successfully imported {len(new_entries)} entries into {table_key}."
        )
