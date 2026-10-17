from PySide6 import QtCore, QtWidgets
from dataglobin import data as Data
from dataglobin import constants as Constants
from dataglobin import persistent as Persistent
from dataglobin.constants import GameID, Language

class EffectStringsTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._refreshing = False

        self.categories = []
        if Data.GAME_VERSION == GameID.ML1R:
            self.categories = [
                {"name": "Wear", "key": "WITM", "prefix": 2},
                {"name": "Badges", "key": "BITM", "prefix": 3},
                {"name": "Accessories", "key": "SITM", "prefix": 4},
            ]
        elif Data.GAME_VERSION == GameID.ML3R:
            self.categories = [
                {"name": "Gear", "key": "EITM", "prefix": 2},
            ]
        self.language_groups = [
            [Language.JP_JA, Language.US_EN, Language.US_FR, Language.US_SP],
            [Language.EU_EN, Language.EU_FR, Language.EU_GE, Language.EU_IT, Language.EU_SP],
            [Language.EU_DU, Language.EU_PT, Language.EU_RU, Language.KR_KO],
        ]
        self.available_languages = set(Data.TEXT_DICT)
        self.category_widgets = {}

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(4)

        if Data.GAME_VERSION == GameID.ML3R:
            title = QtWidgets.QLabel("Note: This whole section is an unused leftover from Superstar Saga + Bowser's Minions. \nIn Bowser's Inside Story + Bowser Jr.'s Journey, the effect's name isn't displayed.")
            title.setAlignment(QtCore.Qt.AlignCenter)
            main_layout.addWidget(title)

        for section_index, category in enumerate(self.categories):
            key = category["key"]
            section = QtWidgets.QWidget()
            section_layout = QtWidgets.QHBoxLayout(section)
            section_layout.setContentsMargins(0, 0, 0, 0)

            list_area = QtWidgets.QWidget()
            list_area.setFixedWidth(250)
            list_layout = QtWidgets.QVBoxLayout(list_area)
            list_layout.setContentsMargins(0, 0, 0, 0)
            list_layout.addWidget(QtWidgets.QLabel(category["name"]))
            item_list = QtWidgets.QListWidget()
            list_layout.addWidget(item_list)
            section_layout.addWidget(list_area)

            separator = QtWidgets.QFrame()
            separator.setFrameShape(QtWidgets.QFrame.VLine)
            separator.setFrameShadow(QtWidgets.QFrame.Sunken)
            section_layout.addWidget(separator)

            properties = QtWidgets.QWidget()
            properties_layout = QtWidgets.QVBoxLayout(properties)
            properties_layout.setContentsMargins(0, 0, 0, 0)
            properties_layout.addStretch()

            language_layout = QtWidgets.QVBoxLayout()
            language_layout.setContentsMargins(0, 0, 0, 0)
            language_layout.setSpacing(0)
            language_group = QtWidgets.QButtonGroup(self)
            language_buttons = []

            for group in self.language_groups:
                available = [lang for lang in group if lang in self.available_languages]
                if not available:
                    continue

                row = QtWidgets.QHBoxLayout()
                row.setContentsMargins(0, 0, 0, 0)
                row.setSpacing(4)
                row.addStretch()

                for language in available:
                    button = QtWidgets.QRadioButton(language.value)
                    button.setFixedHeight(22)
                    language_group.addButton(button)
                    language_buttons.append((button, language))
                    button.toggled.connect(
                        lambda checked, lang=language, cat=key:
                            self.on_language_changed(cat, lang) if checked else None
                    )
                    row.addWidget(button)

                row.addStretch()
                language_layout.addLayout(row)

            properties_layout.addLayout(language_layout)

            grid = QtWidgets.QGridLayout()
            grid.setContentsMargins(0, 5, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(2)

            label_header = QtWidgets.QLabel("Label")
            label_header.setAlignment(QtCore.Qt.AlignCenter)
            grid.addWidget(label_header, 0, 1)

            value_header = QtWidgets.QLabel("Value")
            value_header.setAlignment(QtCore.Qt.AlignCenter)
            grid.addWidget(value_header, 0, 2)
            grid.addWidget(QtWidgets.QLabel("Name"), 1, 0)

            label_input = QtWidgets.QLineEdit()
            label_input.setAlignment(QtCore.Qt.AlignLeft)
            label_input.setMaxLength(0x17)
            grid.addWidget(label_input, 1, 1)

            value_input = QtWidgets.QLineEdit()
            value_input.setAlignment(QtCore.Qt.AlignLeft)
            value_input.setReadOnly(True)
            grid.addWidget(value_input, 1, 2)

            grid.setColumnStretch(0, 0)
            grid.setColumnStretch(1, 1)
            grid.setColumnStretch(2, 1)
            properties_layout.addLayout(grid)
            properties_layout.addStretch()
            section_layout.addWidget(properties, 1)
            main_layout.addWidget(section, 1)

            self.category_widgets[key] = {
                "prefix": category["prefix"],
                "list": item_list,
                "language_group": language_group,
                "language_buttons": language_buttons,
                "current_language": Persistent.UI_DB_LANGUAGE,
                "label": label_input,
                "value": value_input,
            }

            item_list.currentItemChanged.connect(lambda current, previous, cat=key: self.refresh_category(cat))
            label_input.textChanged.connect(lambda text, cat=key: self.on_label_changed(cat, text))

            for button, language in language_buttons:
                if language == Persistent.UI_DB_LANGUAGE:
                    button.setChecked(True)
                    break

            if section_index < len(self.categories) - 1:
                separator = QtWidgets.QFrame()
                separator.setFrameShape(QtWidgets.QFrame.HLine)
                separator.setFrameShadow(QtWidgets.QFrame.Sunken)
                main_layout.addWidget(separator)

        for category in self.categories:
            key = category["key"]
            self.populate_category(key)
            item_list = self.category_widgets[key]["list"]
            if item_list.count():
                item_list.setCurrentRow(0)
            else:
                self.refresh_category(key)

    def populate_category(self, key: str) -> None:
        widgets = self.category_widgets[key]
        list_widget = widgets["list"]
        list_widget.clear()
        names = getattr(Data, "EFFECTS_NAMES", {}).get(key)
        if not names:
            return
        prefix = widgets["prefix"]
        for index, label in enumerate(names):
            item_id = (prefix << 12) | index
            name = Data.get_effect_name(Persistent.UI_DB_LANGUAGE, key, index)
            item = QtWidgets.QListWidgetItem(f"#{item_id:04X} - {name}")
            item.setData(QtCore.Qt.UserRole, index)
            list_widget.addItem(item)

    def set_value_text(self, widget, text):
        widget.setText(text or "")
        widget.setCursorPosition(0)

    def set_label_text(self, widget, text):
        cursor_position = widget.cursorPosition()
        widget.setText(text or "")
        widget.setCursorPosition(min(cursor_position, len(text or "")))

    def on_language_changed(self, key, language):
        self.category_widgets[key]["current_language"] = language
        self.refresh_category(key)

    def on_label_changed(self, key: str, text: str) -> None:
        if self._refreshing:
            return
        names = getattr(Data, "EFFECTS_NAMES", {}).get(key)
        if names is None:
            return
        widgets = self.category_widgets[key]
        current_item = widgets["list"].currentItem()
        if current_item is None:
            return
        index = current_item.data(QtCore.Qt.UserRole)
        if index is None or not 0 <= index < len(names):
            return
        names[index] = text
        item_id = (widgets["prefix"] << 12) | index
        name = Data.get_effect_name(Persistent.UI_DB_LANGUAGE, key, index)
        current_item.setText(f"#{item_id:04X} - {name}")
        self.refresh_category(key)

    def refresh_category(self, key):
        widgets = self.category_widgets[key]
        entry = widgets["list"].currentItem()
        self._refreshing = True
        try:
            names = getattr(Data, "EFFECTS_NAMES", {}).get(key, [])
            if entry is None:
                self.set_label_text(widgets["label"], "")
                self.set_value_text(widgets["value"], "")
                return
            index = entry.data(QtCore.Qt.UserRole)
            if index is None or not 0 <= index < len(names):
                self.set_label_text(widgets["label"], "")
                self.set_value_text(widgets["value"], "")
                return
            label = names[index]
            self.set_label_text(widgets["label"], label)
            value = Data.get_msbt_string(widgets["current_language"], "Item.msbt", label)
            self.set_value_text(widgets["value"], value)
        finally:
            self._refreshing = False