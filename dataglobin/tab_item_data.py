from PySide6 import QtCore, QtWidgets
from dataglobin import data as Data
from dataglobin import constants as Constants
from dataglobin import persistent as Persistent
from dataglobin.constants import GameID, Language

class ItemDataTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._refreshing = False

        self.condition_presets = []
        if Data.GAME_VERSION == GameID.ML3R:
            self.condition_presets = Constants.ML3R_UITM_CONDITION
        elif Data.GAME_VERSION == GameID.ML5:
            self.condition_presets = Constants.ML5_UITM_CONDITION
        
        self.effect_presets = []
        if Data.GAME_VERSION == GameID.ML3R:
            self.effect_presets = Constants.ML3R_EFFECTS_UITM
        elif Data.GAME_VERSION == GameID.ML5:
            self.effect_presets = Constants.ML5_EFFECTS_UITM

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

        for text in ("↑", "↓", "+", "-"):
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

        self.display_order_up = QtWidgets.QPushButton("↑")
        self.display_order_down = QtWidgets.QPushButton("↓")

        for button in (self.display_order_up, self.display_order_down):
            button.setFixedSize(24, 24)
            buttons.addWidget(button)

        buttons.addStretch()

        self.display_order_up.clicked.connect(lambda: self.move_display_order_item(-1))
        self.display_order_down.clicked.connect(lambda: self.move_display_order_item(1))

        row.addWidget(self.display_order)
        row.addLayout(buttons)

        list_layout.addWidget(label)
        list_layout.addLayout(row)

        main_layout.addWidget(list_area)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.VLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        main_layout.addWidget(separator)

        area = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(area)
        layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(area, 1)

        general_section = QtWidgets.QWidget()
        general_layout = QtWidgets.QVBoxLayout(general_section)
        general_layout.setContentsMargins(0, 0, 0, 0)

        general_panel = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(general_panel)

        # ID
        label = QtWidgets.QLabel("ID")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.id_box = QtWidgets.QLineEdit()
        self.id_box.setDisabled(True)
        self.id_box.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(label, 0, 0)
        grid.addWidget(self.id_box, 1, 0)

        # Price
        label = QtWidgets.QLabel("Price")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.price_box = QtWidgets.QSpinBox()
        self.price_box.setRange(0, 65535)
        self.price_box.setAlignment(QtCore.Qt.AlignRight)
        grid.addWidget(label, 0, 1)
        grid.addWidget(self.price_box, 1, 1)

        # Sprite
        label = QtWidgets.QLabel("Sprite")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.sprite_box = QtWidgets.QSpinBox()
        self.sprite_box.setRange(0, 255)
        self.sprite_box.setAlignment(QtCore.Qt.AlignRight)
        grid.addWidget(label, 0, 2)
        grid.addWidget(self.sprite_box, 1, 2)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)
        #TODO: Display menu/field/battle sprites
        grid.setColumnStretch(3, 1)

        general_layout.addWidget(general_panel)
        layout.addWidget(general_section)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(separator)

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
        for effect in self.effect_presets:
            text = f"#{effect['id']:04X} - {effect['name']}"
            self.effect_box.addItem(text, effect["id"])
        self.effect_note = QtWidgets.QLabel()
        self.effect_note.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.effect_note.setWordWrap(True)
        self.effect_note.setMinimumHeight(35)
        self.effect_note.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        grid.addWidget(label, 0, 0, 1, 2)
        grid.addWidget(self.effect_box, 1, 0, 1, 2)
        grid.addWidget(self.effect_note, 2, 0, 1, 2)

        # Effect Parameter
        label = QtWidgets.QLabel("Effect Param")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.param_box = QtWidgets.QSpinBox()
        self.param_box.setRange(0, 65535)
        self.param_box.setMinimumWidth(120)
        self.param_box.setAlignment(QtCore.Qt.AlignRight)
        self.param_note = QtWidgets.QLabel()
        self.param_note.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.param_note.setWordWrap(True)
        self.param_note.setMinimumHeight(35)
        self.param_note.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        grid.addWidget(label, 0, 2)
        grid.addWidget(self.param_box, 1, 2)
        grid.addWidget(self.param_note, 2, 2)

        properties_layout.addWidget(panel)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        properties_layout.addWidget(separator)

        if Data.GAME_VERSION == GameID.ML3R:
            panel = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout(panel)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(2)
             
            # Inventory Pocket
            label = QtWidgets.QLabel("Inventory Category")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.pocket_box = QtWidgets.QComboBox()
            self.pocket_box.addItem("Mushroom Pocket (Battle)", 1)
            self.pocket_box.addItem("Bean Pocket (Menu Only)", 0)
            grid.addWidget(label, 0, 0)
            grid.addWidget(self.pocket_box, 1, 0)

            # Condition
            label = QtWidgets.QLabel("Usability Condition")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.condition_box = QtWidgets.QComboBox()
            for condition in self.condition_presets:
                text = f"#{condition['id']} - {condition['name']}"
                self.condition_box.addItem(text, condition["id"])
            grid.addWidget(label, 0, 1)
            grid.addWidget(self.condition_box, 1, 1)

            # User
            label = QtWidgets.QLabel("Used by")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.user_box = QtWidgets.QComboBox()
            self.user_box.addItem("Everyone", 0)
            self.user_box.addItem("Bros. only", 1)
            self.user_box.addItem("Bowser only", 2)
            self.user_box.addItem("No one", 3)
            grid.addWidget(label, 3, 0)
            grid.addWidget(self.user_box, 4, 0)

            # Target
            label = QtWidgets.QLabel("Target Count")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.multitarget_box = QtWidgets.QComboBox()
            self.multitarget_box.addItem("Single-target", 0)
            self.multitarget_box.addItem("Multi-target", 1)
            grid.addWidget(label, 3, 1)
            grid.addWidget(self.multitarget_box, 4, 1)

            # Additional Flags
            self.usemenu_box = QtWidgets.QCheckBox("Useable from the menu")
            self.mushroom_box = QtWidgets.QCheckBox("Mushroom (Unused?)")
            grid.addWidget(self.usemenu_box, 6, 0)
            grid.addWidget(self.mushroom_box, 6, 1)

            grid.addItem(QtWidgets.QSpacerItem(0, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed), 5, 0, 1, 2)

            grid.setRowMinimumHeight(2, 5)
            grid.setRowMinimumHeight(5, 5)

            properties_layout.addWidget(panel)

        if Data.GAME_VERSION == GameID.ML5:
            # Row 1
            panel = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout(panel)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(2)
            
            self.usemenu_box = QtWidgets.QCheckBox("Useable (Menu)")
            self.usebattle_box = QtWidgets.QCheckBox("Useable (Battle)")
            self.usering_box = QtWidgets.QCheckBox("Useable (Arcade)")
            grid.addWidget(self.usemenu_box, 1, 0)
            grid.addWidget(self.usebattle_box, 1, 1)
            grid.addWidget(self.usering_box, 1, 2)
            
            grid.setColumnStretch(0, 1)
            grid.setColumnStretch(1, 1)
            grid.setColumnStretch(2, 1)
            properties_layout.setSpacing(10)
            properties_layout.addWidget(panel)

            # Row 2
            panel = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout(panel)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(2)

            label = QtWidgets.QLabel("Inventory Category")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.pocket_box = QtWidgets.QLineEdit()
            self.pocket_box.setDisabled(True)
            self.pocket_box.setAlignment(QtCore.Qt.AlignCenter)
            grid.addWidget(label, 0, 0)
            grid.addWidget(self.pocket_box, 1, 0)

            self.mushroom_box = QtWidgets.QCheckBox("Mushroom")
            self.bean_box = QtWidgets.QCheckBox("Bean")
            grid.addWidget(self.mushroom_box, 1, 1)
            grid.addWidget(self.bean_box, 1, 2)

            grid.setColumnStretch(0, 2)
            grid.setColumnStretch(1, 1)
            grid.setColumnStretch(2, 1)
            properties_layout.setSpacing(10)
            properties_layout.addWidget(panel)

            # Row 3
            panel = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout(panel)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(2)

            label = QtWidgets.QLabel("Usability Condition")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.condition_box = QtWidgets.QComboBox()
            for condition in self.condition_presets:
                text = f"#{condition['id']} - {condition['name']}"
                self.condition_box.addItem(text, condition["id"])
            grid.addWidget(label, 0, 0)
            grid.addWidget(self.condition_box, 1, 0)

            label = QtWidgets.QLabel("Playable Target")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.user_box = QtWidgets.QComboBox()
            self.user_box.addItem("Any Bros.", 0)
            self.user_box.addItem("Mario & Luigi only", 1)
            self.user_box.addItem("Paper Mario only", 2)
            self.user_box.addItem("No one", 3)
            grid.addWidget(label, 0, 1)
            grid.addWidget(self.user_box, 1, 1)

            properties_layout.setSpacing(10)
            properties_layout.addWidget(panel)

            # Row 4
            panel = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout(panel)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(2)
            
            self.multitarget_box = QtWidgets.QCheckBox("Multi-Target")
            self.targetenemy_box = QtWidgets.QCheckBox("Targets Enemies")
            self.targetback_box = QtWidgets.QCheckBox("Targets BG Enemies")
            grid.addWidget(self.multitarget_box, 0, 0)
            grid.addWidget(self.targetenemy_box, 0, 1)
            grid.addWidget(self.targetback_box, 0, 2)

            properties_layout.setSpacing(10)
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

            self.current_language = Persistent.UI_DB_LANGUAGE
            language_groups = [
                [ Language.JP_JA, Language.US_EN, Language.US_FR, Language.US_SP ],
                [ Language.EU_EN, Language.EU_FR, Language.EU_GE, Language.EU_IT, Language.EU_SP ],
                [ Language.EU_DU, Language.EU_PT, Language.EU_RU, Language.KR_KO ],
            ]

            available_languages = set(Data.TEXT_DICT)
            self.language_buttons = []
            language_button_group = QtWidgets.QButtonGroup(self)

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
                row.addStretch()

                for language in available:
                    button = QtWidgets.QRadioButton(language.value)
                    button.setFixedHeight(22)

                    language_button_group.addButton(button)
                    row.addWidget(button)
                    self.language_buttons.append(button)

                    button.toggled.connect(
                        lambda checked, lang=language:
                            self.on_language_changed(lang) if checked else None
                    )

                    if language == self.current_language:
                        button.setChecked(True)

                row.addStretch()
                strings_layout.addLayout(row)

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
            self.name_string_value.setEnabled(True)
            self.name_string_value.setReadOnly(True)
            self.name_string_label.setAlignment(QtCore.Qt.AlignLeft)

            grid.addWidget(label, 1, 0)
            grid.addWidget(self.name_string_label, 1, 1)
            grid.addWidget(self.name_string_value, 1, 2)

            label = QtWidgets.QLabel("Plural")
            self.plural_string_label = QtWidgets.QLineEdit()
            self.plural_string_value = QtWidgets.QLineEdit()
            self.plural_string_value.setEnabled(True)
            self.plural_string_value.setReadOnly(True)
            self.plural_string_label.setAlignment(QtCore.Qt.AlignLeft)

            grid.addWidget(label, 2, 0)
            grid.addWidget(self.plural_string_label, 2, 1)
            grid.addWidget(self.plural_string_value, 2, 2)

            label = QtWidgets.QLabel("Desc.")
            self.description_string_label = QtWidgets.QLineEdit()
            self.description_string_value = QtWidgets.QLineEdit()
            self.description_string_value.setEnabled(True)
            self.description_string_value.setReadOnly(True)

            grid.addWidget(label, 3, 0)
            grid.addWidget(self.description_string_label, 3, 1)
            grid.addWidget(self.description_string_value, 3, 2)

            label = QtWidgets.QLabel("Full")
            self.full_string_label = QtWidgets.QLineEdit()
            self.full_string_value = QtWidgets.QLineEdit()
            self.full_string_value.setEnabled(True)
            self.full_string_value.setReadOnly(True)

            grid.addWidget(label, 4, 0)
            grid.addWidget(self.full_string_label, 4, 1)
            grid.addWidget(self.full_string_value, 4, 2)

            strings_layout.addLayout(grid)
            properties_layout.addWidget(strings)

        
        # Functions

        # Item List
        self.item_list.currentItemChanged.connect(self.on_item_selected)
        # General
        self.bind_widget(self.price_box.valueChanged, self.set_price)
        self.bind_widget(self.sprite_box.valueChanged, self.set_sprite)
        # Effect
        self.bind_widget(self.effect_box.currentIndexChanged, self.set_effect)
        self.bind_widget(self.param_box.valueChanged, self.set_effect_param)
        # Flags
        if Data.GAME_VERSION == GameID.ML3R:
            self.bind_widget(self.pocket_box.currentIndexChanged, self.set_pocket)
            self.bind_widget(self.condition_box.currentIndexChanged, self.set_condition)
            self.bind_widget(self.user_box.currentIndexChanged, self.set_user)
            self.bind_widget(self.multitarget_box.currentIndexChanged, self.set_multitarget)
            self.bind_widget(self.usemenu_box.toggled, self.set_usemenu)
            self.bind_widget(self.mushroom_box.toggled, self.set_mushroom)
        elif Data.GAME_VERSION == GameID.ML5:
            self.bind_widget(self.usemenu_box.toggled, self.set_usemenu)
            self.bind_widget(self.usebattle_box.toggled, self.set_usebattle)
            self.bind_widget(self.usering_box.toggled, self.set_usegauntlet)
            self.bind_widget(self.mushroom_box.toggled, self.set_mushroom)
            self.bind_widget(self.bean_box.toggled, self.set_bean)
            self.bind_widget(self.multitarget_box.toggled, self.set_multitarget)
            self.bind_widget(self.targetenemy_box.toggled, self.set_targetenemy)
            self.bind_widget(self.targetback_box.toggled, self.set_targetback)
            self.bind_widget(self.condition_box.currentIndexChanged, self.set_condition)
            self.bind_widget(self.user_box.currentIndexChanged, self.set_user)
        # String labels
        self.bind_widget(self.name_string_label.textChanged, self.set_name_label)
        self.bind_widget(self.plural_string_label.textChanged, self.set_nams_label)
        self.bind_widget(self.description_string_label.textChanged, self.set_desc_label)
        self.bind_widget(self.full_string_label.textChanged, self.set_full_label)
        

        self.populate_items()

    def populate_items(self):
        self.item_list.clear()
        items_by_id = {item.id: item for item in Data.ITEMS}
        for item in Data.ITEMS:
            entry = QtWidgets.QListWidgetItem(f"#{item.id:04X} - {item.getName(Persistent.UI_DB_LANGUAGE)}")
            entry.setData(QtCore.Qt.UserRole, item)
            self.item_list.addItem(entry)
        self.display_order.clear()
        for item_id in Data.INV_ORDER.get("UITM", []):
            item = items_by_id.get(item_id)
            if item is None:
                continue
            entry = QtWidgets.QListWidgetItem(f"#{item.id:04X} - {item.getDefaultName()}")
            entry.setData(QtCore.Qt.UserRole, item)
            self.display_order.addItem(entry)
        if self.item_list.count():
            self.item_list.setCurrentRow(0)
            self.refresh_form()

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
            # Effects
            effect_id = item.effect_id
            index = max(self.effect_box.findData(effect_id), 0)
            self.effect_box.setCurrentIndex(index)
            effect = self.get_effect_definition(self.effect_box.currentData())
            self.effect_note.setText(str(effect.get("note", "")))
            self.param_note.setText(str(effect.get("param1", "")))
            self.param_box.setValue(item.effect_param or 0)
            # Properties
            self.id_box.setText(f"{item.id:X}" if item.id is not None else "")
            self.sprite_box.setValue(item.sprite or 0)
            self.price_box.setValue(item.price or 0)
            # Flags
            if Data.GAME_VERSION == GameID.ML3R:
                self.usemenu_box.setChecked(item.flags1[5])
                self.mushroom_box.setChecked(item.flags1[7])
                self.pocket_box.setCurrentIndex(self.pocket_box.findData(1 if item.flags1[6] else 0))
                self.multitarget_box.setCurrentIndex(self.multitarget_box.findData(1 if item.flags2[0] else 0))
                condition_id = sum(int(flag) << bit for bit, flag in enumerate(item.flags1[:4]))
                self.condition_box.setCurrentIndex(max(self.condition_box.findData(condition_id), 0))
                user_id = int(item.flags2[1]) | (int(item.flags2[2]) << 1)
                self.user_box.setCurrentIndex(max(self.user_box.findData(user_id), 0))
            elif Data.GAME_VERSION == GameID.ML5:
                self.usemenu_box.setChecked(item.flags1[0])
                self.usebattle_box.setChecked(item.flags1[1])
                self.usering_box.setChecked(item.flags1[2])
                self.mushroom_box.setChecked(item.flags2[0])
                self.bean_box.setChecked(item.flags2[1])
                self.multitarget_box.setChecked(item.flags1[6])
                self.targetenemy_box.setChecked(item.flags1[5])
                self.targetback_box.setChecked(item.flags1[7])
                condition_id = sum(int(flag) << bit for bit, flag in enumerate(item.flags2[2:6]))
                self.condition_box.setCurrentIndex(max(self.condition_box.findData(condition_id), 0))
                user_id = int(item.flags1[3]) | (int(item.flags1[4]) << 1)
                self.user_box.setCurrentIndex(max(self.user_box.findData(user_id), 0))
            self.refresh_strings()
        finally:
            self._refreshing = False

    def bind_widget(self, signal, setter):
        def changed(*args):
            if self._refreshing:
                return
            item = self.get_current_item()
            if item is None:
                return
            value = args[0] if args else None
            setter(item, value)
            self.refresh_form()
        signal.connect(changed)

    def set_price(self, item, value):
        item.price = value

    def set_sprite(self, item, value):
        item.sprite = value

    def set_effect(self, item, index):
        effect_id = self.effect_box.itemData(index)
        if effect_id is None:
            return
        item.effect_id = effect_id

    def get_effect_definition(self, effect_id):
        for effect in self.effect_presets:
            if effect["id"] == effect_id:
                return effect
        return None

    def set_effect_param(self, item, value):
        item.effect_param = value

    def set_pocket(self, item, index):
        value = self.pocket_box.itemData(index)
        if value is None:
            return
        item.flags1[6] = bool(value)

    def set_condition(self, item, index):
        condition_id = self.condition_box.itemData(index)
        if condition_id is None:
            return
        if Data.GAME_VERSION == GameID.ML3R:
            for bit in range(4):
                item.flags1[bit] = bool(condition_id & (1 << bit))
        elif Data.GAME_VERSION == GameID.ML5:
            for bit in range(4):
                item.flags2[bit + 2] = bool(condition_id & (1 << bit))

    def set_multitarget(self, item, index):
        # Combobox in ML3R
        if Data.GAME_VERSION == GameID.ML3R:
            value = self.multitarget_box.itemData(index)
            if value is None:
                return
            item.flags2[0] = bool(value)
        # Checkbox in ML5
        elif Data.GAME_VERSION == GameID.ML5:
            item.flags1[6] = index

    def set_targetenemy(self, item, index):
        if Data.GAME_VERSION == GameID.ML5:
            item.flags1[5] = index

    def set_targetback(self, item, index):
        if Data.GAME_VERSION == GameID.ML5:
            item.flags1[7] = index

    def set_user(self, item, index):
        user_id = self.user_box.itemData(index)
        if user_id is None:
            return
        if Data.GAME_VERSION == GameID.ML3R:
            item.flags2[1] = bool(user_id & 1)
            item.flags2[2] = bool(user_id & 2)
        elif Data.GAME_VERSION == GameID.ML5:
            item.flags1[3] = bool(user_id & 1)
            item.flags1[4] = bool(user_id & 2)

    def set_usemenu(self, item, checked):
        if Data.GAME_VERSION == GameID.ML3R:
            item.flags1[5] = checked
        elif Data.GAME_VERSION == GameID.ML5:
            item.flags1[0] = checked

    def set_usebattle(self, item, checked):
        if Data.GAME_VERSION == GameID.ML5:
            item.flags1[1] = checked

    def set_usegauntlet(self, item, checked):
        if Data.GAME_VERSION == GameID.ML5:
            item.flags1[2] = checked

    def set_mushroom(self, item, checked):
        if Data.GAME_VERSION == GameID.ML3R:
            item.flags1[7] = checked
        elif Data.GAME_VERSION == GameID.ML5:
            item.flags2[0] = checked

    def set_bean(self, item, checked):
        if Data.GAME_VERSION == GameID.ML5:
            item.flags2[1] = checked


    def set_value_text(self, widget, text):
        widget.setText(text or "")
        widget.setCursorPosition(0)

    def set_label_text(self, widget, text):
        cursor_position = widget.cursorPosition()
        widget.setText(text or "")
        widget.setCursorPosition(cursor_position)

    def on_language_changed(self, language):
        self.current_language = language
        self.refresh_strings()
        
    def refresh_strings(self):
        item = self.get_current_item()
        if item is None:
            return
        text = f"#{item.id:04X} - {item.getDefaultName()}"
        for widget in (self.item_list, self.display_order):
            for i in range(widget.count()):
                entry = widget.item(i)
                stored_item = entry.data(QtCore.Qt.UserRole)
                if stored_item is not None and stored_item.id == item.id:
                    entry.setText(text)
        language = self.current_language
        self.set_label_text(self.name_string_label, item.label_name)
        self.set_label_text(self.plural_string_label, item.label_nams)
        self.set_label_text(self.description_string_label, item.label_desc)
        self.set_label_text(self.full_string_label, item.label_full)
        self.set_value_text(self.name_string_value, item.getName(language))
        self.set_value_text(self.plural_string_value, item.getNams(language))
        self.set_value_text(self.description_string_value, item.getDesc(language))
        self.set_value_text(self.full_string_value, item.getFull(language))

    def set_name_label(self, item, _):
        item.label_name = self.name_string_label.text()
        self.refresh_strings()

    def set_nams_label(self, item, _):
        item.label_nams = self.plural_string_label.text()
        self.refresh_strings()

    def set_desc_label(self, item, _):
        item.label_desc = self.description_string_label.text()
        self.refresh_strings()

    def set_full_label(self, item, _):
        item.label_full = self.full_string_label.text()
        self.refresh_strings()

    def move_display_order_item(self, offset):
        row = self.display_order.currentRow()
        new_row = row + offset
        if row < 0 or not 0 <= new_row < self.display_order.count():
            return
        item = self.display_order.takeItem(row)
        self.display_order.insertItem(new_row, item)
        self.display_order.setCurrentRow(new_row)
        Data.INV_ORDER["UITM"] = [
            self.display_order.item(i).data(QtCore.Qt.ItemDataRole.UserRole).id
            for i in range(self.display_order.count())
        ]