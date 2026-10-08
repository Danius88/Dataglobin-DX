from PySide6 import QtCore, QtWidgets
from dataglobin import data as Data
from dataglobin import constants as Constants
from dataglobin import persistent as Persistent
from dataglobin.constants import GameID, Language

class ItemDataTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._refreshing = False

        main_layout = QtWidgets.QHBoxLayout(self)

        list_area = QtWidgets.QWidget()
        list_area.setFixedWidth(250)

        list_layout = QtWidgets.QVBoxLayout(list_area)
        list_layout.setContentsMargins(0, 0, 0, 0)

        label = QtWidgets.QLabel("Item List")

        row = QtWidgets.QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)

        self.item_list = QtWidgets.QListWidget()

        buttons = QtWidgets.QVBoxLayout()
        buttons.setContentsMargins(0, 0, 0, 0)
        buttons.setSpacing(2)

        for text in ("↑", "↓", "+"):
            button = QtWidgets.QPushButton(text)
            button.setFixedSize(24, 24)
            buttons.addWidget(button)

        buttons.addStretch()

        row.addWidget(self.item_list)
        row.addLayout(buttons)

        list_layout.addWidget(label)
        list_layout.addLayout(row)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)

        list_layout.addWidget(separator)

        label = QtWidgets.QLabel("Display Order")

        row = QtWidgets.QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)

        self.display_order = QtWidgets.QListWidget()

        buttons = QtWidgets.QVBoxLayout()
        buttons.setContentsMargins(0, 0, 0, 0)
        buttons.setSpacing(2)

        for text in ("↑", "↓", "+"):
            button = QtWidgets.QPushButton(text)
            button.setFixedSize(24, 24)
            buttons.addWidget(button)

        buttons.addStretch()

        row.addWidget(self.display_order)
        row.addLayout(buttons)

        list_layout.addWidget(label)
        list_layout.addLayout(row)

        main_layout.addWidget(list_area)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.VLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)

        # Properties Start
        main_layout.addWidget(separator)

        area = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(area)
        main_layout.addWidget(area, 1)

        properties = QtWidgets.QWidget()
        properties_layout = QtWidgets.QVBoxLayout(properties)
        properties_layout.setContentsMargins(0, 0, 0, 0)
        properties_layout.setSpacing(4)

        layout.addWidget(properties)
        layout.addStretch()

        panel = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(panel)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(2)

        # Effect ID
        label = QtWidgets.QLabel("Item Effect")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.effect_box = QtWidgets.QComboBox()
        for effect in Constants.ML3R_EFFECTS_UITM:
            text = f"#{effect['id']:04X} - {effect['name']}"
            self.effect_box.addItem(text, effect["id"])
        self.effect_note = QtWidgets.QLabel()
        self.effect_note.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop
        )
        self.effect_note.setWordWrap(True)
        self.effect_note.setMinimumHeight(35)
        self.effect_note.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        grid.addWidget(label, 0, 0)
        grid.addWidget(self.effect_box, 1, 0)
        grid.addWidget(self.effect_note, 2, 0)

        # Effect Parameter
        label = QtWidgets.QLabel("Effect Param")
        label.setAlignment(QtCore.Qt.AlignCenter)

        self.param_box = QtWidgets.QSpinBox()
        self.param_box.setRange(0, 65535)
        self.param_box.setMinimumWidth(120)

        self.param_note = QtWidgets.QLabel()
        self.param_note.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop
        )
        self.param_note.setWordWrap(True)
        self.param_note.setMinimumHeight(35)
        self.param_note.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Minimum
        )

        grid.addWidget(label, 0, 2)
        grid.addWidget(self.param_box, 1, 2)
        grid.addWidget(self.param_note, 2, 2)

        # Price
        label = QtWidgets.QLabel("Price")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.price_box = QtWidgets.QSpinBox()
        self.price_box.setRange(0, 65535)
        self.price_box.setFixedWidth(70)
        grid.addWidget(label, 0, 3)
        grid.addWidget(self.price_box, 1, 3)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 0)
        grid.setColumnStretch(3, 0)

        properties_layout.addWidget(panel)

        # Flags start
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        properties_layout.addWidget(separator)

        panel = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(panel)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(2)

        # Inventory Pocket
        label = QtWidgets.QLabel("Inventory Category")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.pocket_box = QtWidgets.QComboBox()
        grid.addWidget(label, 0, 0)
        grid.addWidget(self.pocket_box, 1, 0)

        label = QtWidgets.QLabel("Usability Condition")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.condition_box = QtWidgets.QComboBox()
        grid.addWidget(label, 0, 1)
        grid.addWidget(self.condition_box, 1, 1)

        properties_layout.addWidget(panel)

        # Strings Start
        if Data.GAME_VERSION in (GameID.ML3R, GameID.ML1R, GameID.ML5):
            separator = QtWidgets.QFrame()
            separator.setFrameShape(QtWidgets.QFrame.HLine)
            separator.setFrameShadow(QtWidgets.QFrame.Sunken)

            properties_layout.addWidget(separator)

            strings = QtWidgets.QWidget()
            strings_layout = QtWidgets.QVBoxLayout(strings)
            strings_layout.setContentsMargins(0, 0, 0, 0)
            strings_layout.setSpacing(2)

            language_groups = [
                [ Language.JP_JA, Language.US_EN, Language.US_FR, Language.US_SP ],
                [ Language.EU_EN, Language.EU_FR, Language.EU_GE, Language.EU_IT, Language.EU_SP ],
                [ Language.EU_DU, Language.EU_PT, Language.EU_RU, Language.KR_KO ],
            ]

            available_languages = {text["language"] for text in Data.TEXT_DICT}
            self.language_buttons = []
            for group in language_groups:
                available = [
                    language
                    for language in group
                    if language in available_languages
                ]

                if not available:
                    continue

                row = QtWidgets.QHBoxLayout()
                row.setContentsMargins(0, 0, 0, 0)
                row.setSpacing(4)

                group_box = QtWidgets.QButtonGroup(self)

                row.addStretch()

                for language in available:
                    button = QtWidgets.QRadioButton(language.value)
                    button.setFixedHeight(22)

                    group_box.addButton(button)
                    row.addWidget(button)
                    self.language_buttons.append(button)

                    if Persistent.DB_LANGUAGE == language:
                        button.setChecked(True)

                row.addStretch()
                strings_layout.addLayout(row)

            if Persistent.DB_LANGUAGE is None and self.language_buttons:
                button = self.language_buttons[0]
                button.setChecked(True)
                Persistent.DB_LANGUAGE = Language(button.text())

            grid = QtWidgets.QGridLayout()
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(2)

            label = QtWidgets.QLabel("Label")
            label.setAlignment(QtCore.Qt.AlignCenter)
            grid.addWidget(label, 0, 1)

            label = QtWidgets.QLabel("Value")
            label.setAlignment(QtCore.Qt.AlignCenter)
            grid.addWidget(label, 0, 2)

            label = QtWidgets.QLabel("Name")
            self.name_string_label = QtWidgets.QLineEdit()
            self.name_string_value = QtWidgets.QLineEdit()
            self.name_string_value.setEnabled(False)

            grid.addWidget(label, 1, 0)
            grid.addWidget(self.name_string_label, 1, 1)
            grid.addWidget(self.name_string_value, 1, 2)

            label = QtWidgets.QLabel("Plural Name")
            self.plural_string_label = QtWidgets.QLineEdit()
            self.plural_string_value = QtWidgets.QLineEdit()
            self.plural_string_value.setEnabled(False)

            grid.addWidget(label, 2, 0)
            grid.addWidget(self.plural_string_label, 2, 1)
            grid.addWidget(self.plural_string_value, 2, 2)

            label = QtWidgets.QLabel("Description")
            self.description_string_label = QtWidgets.QLineEdit()
            self.description_string_value = QtWidgets.QLineEdit()
            self.description_string_value.setEnabled(False)

            grid.addWidget(label, 3, 0)
            grid.addWidget(self.description_string_label, 3, 1)
            grid.addWidget(self.description_string_value, 3, 2)

            label = QtWidgets.QLabel("Full")
            self.full_string_label = QtWidgets.QLineEdit()
            self.full_string_value = QtWidgets.QLineEdit()
            self.full_string_value.setEnabled(False)

            grid.addWidget(label, 4, 0)
            grid.addWidget(self.full_string_label, 4, 1)
            grid.addWidget(self.full_string_value, 4, 2)

            strings_layout.addLayout(grid)
            properties_layout.addWidget(strings)

        
        # Functions

        # Item List
        self.item_list.currentItemChanged.connect(self.on_item_selected)
        # Effect ID
        self.bind_widget(self.effect_box.currentIndexChanged, self.set_effect)
        # Effect Parameter
        self.bind_widget(self.param_box.valueChanged, self.set_effect_param)
        # Price
        self.bind_widget(self.price_box.valueChanged, self.set_price)

        self.populate_items()

    def populate_items(self):
        self.item_list.clear()
        for item in Data.ITEMS:
            text = f"#{item.id:04X} - {item.getDefaultName()}"
            entry = QtWidgets.QListWidgetItem(text)
            entry.setData(QtCore.Qt.UserRole, item)
            self.item_list.addItem(entry)
        if self.item_list.count():
            self.item_list.setCurrentRow(0)

    def get_current_item(self):
        entry = self.item_list.currentItem()
        if entry is None:
            return None
        return entry.data(QtCore.Qt.UserRole)

    def on_item_selected(self, current, previous):
        self.refresh_form()

    def refresh_form(self):
        item = self.get_current_item()
        if item is None:
            return
        self._refreshing = True
        try:
            combo_id = item.effect_id
            index = self.effect_box.findData(combo_id)
            if index >= 0:
                self.effect_box.setCurrentIndex(index)
                effect = self.get_effect_definition(combo_id)
                if effect is not None:
                    self.effect_note.setText(str(effect.get("note", "")))
                    self.param_note.setText(str(effect.get("param1", "")))
                else:
                    self.effect_note.clear()
                    self.param_note.clear()
            else:
                self.effect_box.setCurrentIndex(-1)
                self.effect_note.clear()
                self.param_note.clear()
            self.param_box.setValue(item.effect_param or 0)
            self.price_box.setValue(item.price or 0)
        finally:
            self._refreshing = False

    def bind_widget(self, signal, setter):
        def changed(value):
            if self._refreshing:
                return
            item = self.get_current_item()
            if item is None:
                return
            setter(item, value)
            self.refresh_form()
        signal.connect(changed)

    def set_effect(self, item, index):
        effect_id = self.effect_box.itemData(index)
        if effect_id is None:
            return
        item.effect_id = effect_id

    def set_effect_param(self, item, value):
        item.effect_param = value

    def set_price(self, item, value):
        item.price = value

    def get_effect_definition(self, effect_id):
        for effect in Constants.ML3R_EFFECTS_UITM:
            if effect["id"] == effect_id:
                return effect
        return None