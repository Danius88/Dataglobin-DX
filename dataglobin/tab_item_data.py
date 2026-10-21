from PySide6 import QtCore, QtWidgets
from dataglobin import data as Data
from dataglobin import constants as Constants
from dataglobin import persistent as Persistent
from dataglobin.constants import GameID, Language

class ItemDataTab(QtWidgets.QWidget):
    def __init__(self, parent=None, item_key=None):
        super().__init__(parent)

        self._refreshing = False
        self.item_key = item_key
        self.version = Data.GAME_VERSION

        self.condition_presets = []
        if self.version == GameID.ML3R:
            self.condition_presets = Constants.ML3R_UITM_CONDITION
        elif self.version == GameID.ML1R:
            self.condition_presets = Constants.ML1R_UITM_CONDITION
        elif self.version == GameID.ML5:
            self.condition_presets = Constants.ML5_UITM_CONDITION
        
        self.effect_presets = []
        if self.version == GameID.ML3R:
            if self.item_key == "UITM":
                self.effect_presets = Constants.ML3R_EFFECTS_UITM
            elif self.item_key == "EITM":
                self.effect_presets = Constants.ML3R_EFFECTS_EITM
        elif self.version == GameID.ML1R:
            if self.item_key == "UITM":
                self.effect_presets = Constants.ML1R_EFFECTS_UITM
            elif self.item_key == "WITM":
                self.effect_presets = Constants.ML1R_EFFECTS_WITM
            elif self.item_key == "BITM":
                self.effect_presets = Constants.ML1R_EFFECTS_BITM
            elif self.item_key == "SITM":
                self.effect_presets = Constants.ML1R_EFFECTS_SITM
        elif self.version == GameID.ML5:
            if self.item_key == "UITM":
                self.effect_presets = Constants.ML5_EFFECTS_UITM
            if self.item_key == "CITM":
                self.effect_presets = Constants.ML5_EFFECTS_CITM

        self.category_presets = []
        if self.version == GameID.ML3R and self.item_key == "EITM":
            self.category_presets = Constants.ML3R_EITM_CATEGORY
        elif self.version == GameID.ML5 and self.item_key == "EITM":
            self.category_presets = Constants.ML5_EITM_CATEGORY

        main_layout = QtWidgets.QHBoxLayout(self)

        list_area = QtWidgets.QWidget()
        list_area.setFixedWidth(250)

        list_layout = QtWidgets.QVBoxLayout(list_area)
        list_layout.setContentsMargins(0, 0, 0, 0)

        label = QtWidgets.QLabel("Item List")

        row = QtWidgets.QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)

        self.item_list = QtWidgets.QListWidget()
        self.item_list.currentItemChanged.connect(self.on_item_selected)
        buttons = QtWidgets.QVBoxLayout()
        buttons.setContentsMargins(0, 0, 0, 0)
        buttons.setSpacing(2)

        for text in ("↑", "↓"):
            button = QtWidgets.QPushButton(text)
            button.setFixedSize(24, 24)

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
        buttons.addStretch()
        for button in (self.display_order_up, self.display_order_down):
            button.setFixedSize(24, 24)
            buttons.addWidget(button)
        buttons.addStretch()

        self.display_order_add = QtWidgets.QPushButton("Add entry")
        self.display_order_remove = QtWidgets.QPushButton("Delete entry")
        self.display_order_add.clicked.connect(self.add_display_order_item)
        self.display_order_remove.clicked.connect(self.remove_display_order_item)
        self.display_order_up.clicked.connect(lambda: self.move_display_order_item(-1))
        self.display_order_down.clicked.connect(lambda: self.move_display_order_item(1))

        row.addWidget(self.display_order)
        row.addLayout(buttons)
        list_layout.addWidget(label)
        list_layout.addLayout(row)

        order_actions = QtWidgets.QHBoxLayout()
        order_actions.setContentsMargins(0, 0, 0, 0)
        order_actions.setSpacing(4)
        order_actions.addWidget(self.display_order_add)
        order_actions.addWidget(self.display_order_remove)
        list_layout.addLayout(order_actions)

        main_layout.addWidget(list_area)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.VLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        main_layout.addWidget(separator)

        area = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(area)
        layout.setContentsMargins(0, 0, 0, 0)
        #layout.addStretch()
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
        if self.version != GameID.ML1R or self.item_key not in ("SITM", "EITM", "BEAN"):
            label = QtWidgets.QLabel("Price")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.price_box = QtWidgets.QSpinBox()
            self.price_box.setRange(0, 0xFFFF)
            if self.version in (GameID.ML5, GameID.ML4):
                self.price_box.setRange(0, 0xFFFF)
            self.price_box.setAlignment(QtCore.Qt.AlignRight)
            self.bind_widget(self.price_box.valueChanged, self.set_price)
            grid.addWidget(label, 0, 1)
            grid.addWidget(self.price_box, 1, 1)

        # Sprite
        label = QtWidgets.QLabel("Sprite")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.sprite_box = QtWidgets.QSpinBox()
        self.sprite_box.setRange(0, 0xFF)
        self.sprite_box.setAlignment(QtCore.Qt.AlignRight)
        self.bind_widget(self.sprite_box.valueChanged, self.set_sprite)
        grid.addWidget(label, 0, 2)
        grid.addWidget(self.sprite_box, 1, 2)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)
        #TODO: Display menu/field/battle sprites
        grid.setColumnStretch(3, 1)

        general_layout.addWidget(general_panel)
        layout.addWidget(general_section)

        properties = QtWidgets.QWidget()
        properties_layout = QtWidgets.QVBoxLayout(properties)
        properties_layout.setContentsMargins(0, 0, 0, 0)
        properties_layout.setSpacing(4)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        if self._hasEffect():
            layout.addWidget(separator)
        layout.addWidget(properties)
        layout.addStretch()

        # Effects
        if self._hasEffect():
            panel = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout(panel)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(0)

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
            self.effect_note.setFixedHeight(self.effect_note.fontMetrics().lineSpacing() * 2)
            self.effect_note.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.bind_widget(self.effect_box.currentIndexChanged, self.set_effect)
            grid.addWidget(label, 0, 0, 1, 2)
            grid.addWidget(self.effect_box, 1, 0, 1, 2)
            grid.addWidget(self.effect_note, 2, 0, 1, 2)

            # Effect Parameters
            params_layout = QtWidgets.QHBoxLayout()
            params_layout.setContentsMargins(0, 0, 0, 0)
            params_layout.setSpacing(8)
            params_layout.setAlignment(QtCore.Qt.AlignHCenter)

            # Effect Param 1
            param1_layout = QtWidgets.QVBoxLayout()
            param1_layout.setContentsMargins(0, 0, 0, 0)
            param1_layout.setSpacing(0)
            label = QtWidgets.QLabel("Effect Param")
            if self._effectParam2():
                label.setText("Effect Param 1")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.param1_box = QtWidgets.QSpinBox()
            if self.version in (GameID.ML3R, GameID.ML1R, GameID.ML5):
                self.param1_box.setRange(-0x8000, 0x7FFF)
                if self.version == GameID.ML3R and self.item_key == "EITM":
                    self.param1_box.setRange(0, 255)
                elif self.version == GameID.ML5 and self.item_key == "EITM":
                    self.param1_box.setRange(-0x80000000, 0x7FFFFFFF)
            self.param1_box.setMinimumWidth(100)
            self.param1_box.setAlignment(QtCore.Qt.AlignRight)
            self.bind_widget(self.param1_box.valueChanged, self.set_effect_param1)
            self.param1_note = QtWidgets.QLabel()
            self.param1_note.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
            self.param1_note.setWordWrap(True)
            self.param1_note.setFixedHeight(self.param1_note.fontMetrics().lineSpacing() * 2)
            self.param1_note.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
            param1_layout.addWidget(label)
            param1_layout.addWidget(self.param1_box, alignment=QtCore.Qt.AlignHCenter)
            param1_layout.addWidget(self.param1_note)
            params_layout.addLayout(param1_layout)

            # Effect Param 2
            if self._effectParam2():
                param2_layout = QtWidgets.QVBoxLayout()
                param2_layout.setContentsMargins(0, 0, 0, 0)
                param2_layout.setSpacing(0)
                label = QtWidgets.QLabel("Effect Param 2")
                label.setAlignment(QtCore.Qt.AlignCenter)
                self.param2_box = QtWidgets.QSpinBox()
                self.param2_box.setRange(0, 0xFFFF)
                if self.version in (GameID.ML3R, GameID.ML1R, GameID.ML5):
                    self.param2_box.setRange(-0x8000, 0x7FFF)
                    if self.version == GameID.ML3R and self.item_key == "EITM":
                        self.param2_box.setRange(0, 0xFF)
                    elif self.version == GameID.ML5 and self.item_key == "EITM":
                        self.param2_box.setRange(-0x80000000, 0x7FFFFFFF)
                self.param2_box.setMinimumWidth(100)
                self.param2_box.setAlignment(QtCore.Qt.AlignRight)
                self.bind_widget(self.param2_box.valueChanged, self.set_effect_param2)
                self.param2_note = QtWidgets.QLabel()
                self.param2_note.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
                self.param2_note.setWordWrap(True)
                self.param2_note.setFixedHeight(self.param2_note.fontMetrics().lineSpacing() * 2)
                self.param2_note.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                param2_layout.addWidget(label)
                param2_layout.addWidget(self.param2_box, alignment=QtCore.Qt.AlignHCenter)
                param2_layout.addWidget(self.param2_note)
                params_layout.addLayout(param2_layout)

            grid.addLayout(params_layout, 4, 0, 1, 2)
            grid.setRowMinimumHeight(3, 6)

            properties_layout.addWidget(panel)
        
        if self._hasStats():
            separator = QtWidgets.QFrame()
            separator.setFrameShape(QtWidgets.QFrame.HLine)
            separator.setFrameShadow(QtWidgets.QFrame.Sunken)     
            properties_layout.addWidget(separator)

            # Row 1
            panel = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout(panel)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(2)

            self.hp_box = QtWidgets.QSpinBox()
            self.bp_box = QtWidgets.QSpinBox()
            self.pow_box = QtWidgets.QSpinBox()
            self.def_box = QtWidgets.QSpinBox()
            self.spe_box = QtWidgets.QSpinBox()
            self.sta_box = QtWidgets.QSpinBox()
            stats = [
                ("HP", self.hp_box),
                ("BP", self.bp_box),
                ("POW", self.pow_box),
                ("DEF", self.def_box),
                ("SPE", self.spe_box),
                ("STA", self.sta_box),
            ]
            for column, (name, spinbox) in enumerate(stats):
                label = QtWidgets.QLabel(name)
                label.setAlignment(QtCore.Qt.AlignCenter)
                spinbox.setRange(-0x8000, 0x7FFF)
                spinbox.setAlignment(QtCore.Qt.AlignRight)
                spinbox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                grid.addWidget(label, 0, column)
                grid.addWidget(spinbox, 1, column)
                grid.setColumnStretch(column, 1)
            self.bind_widget(self.hp_box.valueChanged, self.set_hp)
            self.bind_widget(self.bp_box.valueChanged, self.set_bp)
            self.bind_widget(self.pow_box.valueChanged, self.set_pow)
            self.bind_widget(self.def_box.valueChanged, self.set_def)
            self.bind_widget(self.spe_box.valueChanged, self.set_spe)
            self.bind_widget(self.sta_box.valueChanged, self.set_sta)
            properties_layout.addWidget(panel)
            properties_layout.addSpacing(4)

            # Row 2
            panel = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout(panel)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(4)

            if self.version in (GameID.ML3R, GameID.ML5):
                label = QtWidgets.QLabel("Category")
                label.setAlignment(QtCore.Qt.AlignCenter)
                self.category_box = QtWidgets.QComboBox()
                for category in self.category_presets:
                    text = f"#{category['id']} - {category['name']}"
                    self.category_box.addItem(text, category["id"])
                self.category_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                self.bind_widget(self.category_box.currentIndexChanged, self.set_category)
                grid.addWidget(label, 0, 0)
                grid.addWidget(self.category_box, 1, 0)
                grid.setColumnStretch(0, 1)
                grid.setColumnStretch(1, 1)
            else:
                grid.setColumnStretch(0, 1)
                grid.setColumnStretch(1, 2)
                grid.setColumnStretch(2, 1)

            
            if self.version == GameID.ML3R:
                label = QtWidgets.QLabel("User")
                label.setAlignment(QtCore.Qt.AlignCenter)
                self.user_box = QtWidgets.QComboBox()
                self.user_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                self.user_box.addItem("Mario & Luigi", 0)
                self.user_box.addItem("Bowser", 1)
                self.bind_widget(self.user_box.currentIndexChanged, self.set_user)
                grid.addWidget(label, 0, 1)
                grid.addWidget(self.user_box, 1, 1)
            elif self.version == GameID.ML1R and self.item_key == "WITM":
                label = QtWidgets.QLabel("User")
                label.setAlignment(QtCore.Qt.AlignCenter)
                self.user_box = QtWidgets.QComboBox()
                self.user_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                self.user_box.addItem("Mario", 1)
                self.user_box.addItem("Luigi", 2)
                self.user_box.addItem("Both Bros.", 3)
                self.bind_widget(self.user_box.currentIndexChanged, self.set_user)
                grid.addWidget(label, 0, 1)
                grid.addWidget(self.user_box, 1, 1)

            properties_layout.addWidget(panel)
        
        if self.version == GameID.ML3R and self.item_key == "UITM":
            # Row 1
            panel = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout(panel)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(2)

            label = QtWidgets.QLabel("Inventory Category")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.pocket_box = QtWidgets.QComboBox()
            self.pocket_box.addItem("Mushroom Pocket (Battle)", 1)
            self.pocket_box.addItem("Bean Pocket (Menu Only)", 0)
            self.bind_widget(self.pocket_box.currentIndexChanged, self.set_pocket)
            grid.addWidget(label, 0, 0)
            grid.addWidget(self.pocket_box, 1, 0)

            label = QtWidgets.QLabel("Usability Condition")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.condition_box = QtWidgets.QComboBox()
            for condition in self.condition_presets:
                text = f"#{condition['id']} - {condition['name']}"
                self.condition_box.addItem(text, condition["id"])
            self.bind_widget(self.condition_box.currentIndexChanged, self.set_condition)
            grid.addWidget(label, 0, 1)
            grid.addWidget(self.condition_box, 1, 1)
            
            grid.setColumnStretch(0, 1)
            grid.setColumnStretch(1, 1)
            properties_layout.setSpacing(10)
            properties_layout.addWidget(panel)

            # Row 2
            panel = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout(panel)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(2)

            label = QtWidgets.QLabel("Used by")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.user_box = QtWidgets.QComboBox()
            self.user_box.addItem("Everyone", 0)
            self.user_box.addItem("Bros. only", 1)
            self.user_box.addItem("Bowser only", 2)
            self.user_box.addItem("No one", 3)
            self.bind_widget(self.user_box.currentIndexChanged, self.set_user)
            grid.addWidget(label, 0, 0)
            grid.addWidget(self.user_box, 1, 0)

            label = QtWidgets.QLabel("Target Count")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.multitarget_box = QtWidgets.QComboBox()
            self.multitarget_box.addItem("Single-target", 0)
            self.multitarget_box.addItem("Multi-target", 1)
            self.bind_widget(self.multitarget_box.currentIndexChanged, self.set_multitarget)
            grid.addWidget(label, 0, 1)
            grid.addWidget(self.multitarget_box, 1, 1)
           
            grid.setColumnStretch(0, 1)
            grid.setColumnStretch(1, 1)
            properties_layout.setSpacing(10)
            properties_layout.addWidget(panel)

            # Row 3
            panel = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout(panel)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(2)

            self.usemenu_box = QtWidgets.QCheckBox("Useable from the menu")
            self.mushroom_box = QtWidgets.QCheckBox("Mushroom?")
            self.bind_widget(self.mushroom_box.toggled, self.set_mushroom)
            self.bind_widget(self.usemenu_box.toggled, self.set_usemenu)
            grid.addWidget(self.usemenu_box, 0, 0)
            grid.addWidget(self.mushroom_box, 0, 1)
            
            grid.setColumnStretch(0, 1)
            grid.setColumnStretch(1, 1)
            properties_layout.setSpacing(10)
            properties_layout.addWidget(panel)

        if self.version == GameID.ML1R and self.item_key == "UITM":
            # Row 1
            panel = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout(panel)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(2)

            label = QtWidgets.QLabel("Inventory Category")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.pocket_box = QtWidgets.QComboBox()
            self.pocket_box.addItem("Mushroom Pocket (Battle)", 1)
            self.pocket_box.addItem("Blend Pocket (Menu Only)", 0)
            self.bind_widget(self.pocket_box.currentIndexChanged, self.set_pocket)
            grid.addWidget(label, 0, 0)
            grid.addWidget(self.pocket_box, 1, 0)

            label = QtWidgets.QLabel("Usability Condition")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.condition_box = QtWidgets.QComboBox()
            for condition in self.condition_presets:
                text = f"#{condition['id']} - {condition['name']}"
                self.condition_box.addItem(text, condition["id"])
            self.bind_widget(self.condition_box.currentIndexChanged, self.set_condition)
            grid.addWidget(label, 0, 1)
            grid.addWidget(self.condition_box, 1, 1)
            
            grid.setColumnStretch(0, 1)
            grid.setColumnStretch(1, 1)
            properties_layout.setSpacing(10)
            properties_layout.addWidget(panel)

            # Row 2
            panel = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout(panel)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(2)

            label = QtWidgets.QLabel("Target Count")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.multitarget_box = QtWidgets.QComboBox()
            self.multitarget_box.addItem("Single-target", 0)
            self.multitarget_box.addItem("Multi-target", 1)
            self.bind_widget(self.multitarget_box.currentIndexChanged, self.set_multitarget)
            grid.addWidget(label, 0, 0)
            grid.addWidget(self.multitarget_box, 1, 0)

            label = QtWidgets.QLabel("Unknown")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.mushstat_box = QtWidgets.QSpinBox()
            self.mushstat_box.setRange(0, 0xFF)
            self.mushstat_box.setAlignment(QtCore.Qt.AlignRight)
            self.bind_widget(self.mushstat_box.valueChanged, self.set_mushstat)
            grid.addWidget(label, 0, 1)
            grid.addWidget(self.mushstat_box, 1, 1)

            grid.setColumnStretch(0, 1)
            grid.setColumnStretch(1, 1)
            properties_layout.setSpacing(10)
            properties_layout.addWidget(panel)

            # Row 3
            panel = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout(panel)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(2)

            self.usemenu_box = QtWidgets.QCheckBox("Useable from the menu")
            self.bind_widget(self.usemenu_box.toggled, self.set_usemenu)
            grid.addWidget(self.usemenu_box, 0, 0)
            
            grid.setColumnStretch(0, 1)
            grid.setColumnStretch(1, 1)
            properties_layout.setSpacing(10)
            properties_layout.addWidget(panel)

        if self.version == GameID.ML5 and self.item_key == "UITM":
            # Row 1
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
            self.bind_widget(self.mushroom_box.toggled, self.set_mushroom)
            self.bind_widget(self.bean_box.toggled, self.set_bean)
            grid.addWidget(self.mushroom_box, 1, 1)
            grid.addWidget(self.bean_box, 1, 2)

            grid.setColumnStretch(0, 2)
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
            
            self.usemenu_box = QtWidgets.QCheckBox("Useable (Menu)")
            self.usebattle_box = QtWidgets.QCheckBox("Useable (Battle)")
            self.usering_box = QtWidgets.QCheckBox("Useable (Arcade)")
            self.bind_widget(self.usering_box.toggled, self.set_usegauntlet)
            self.bind_widget(self.usebattle_box.toggled, self.set_usebattle)
            self.bind_widget(self.usemenu_box.toggled, self.set_usemenu)
            grid.addWidget(self.usemenu_box, 1, 0)
            grid.addWidget(self.usebattle_box, 1, 1)
            grid.addWidget(self.usering_box, 1, 2)
            
            grid.setColumnStretch(0, 1)
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
            self.bind_widget(self.condition_box.currentIndexChanged, self.set_condition)
            grid.addWidget(label, 0, 0)
            grid.addWidget(self.condition_box, 1, 0)

            label = QtWidgets.QLabel("Consumable by")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.user_box = QtWidgets.QComboBox()
            self.user_box.addItem("Any Bros.", 0)
            self.user_box.addItem("Mario & Luigi only", 1)
            self.user_box.addItem("Paper Mario only", 2)
            self.user_box.addItem("No one", 3)
            self.bind_widget(self.user_box.currentIndexChanged, self.set_user)
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
            self.bind_widget(self.multitarget_box.toggled, self.set_multitarget)
            self.bind_widget(self.targetenemy_box.toggled, self.set_targetenemy)
            self.bind_widget(self.targetback_box.toggled, self.set_targetback)
            grid.addWidget(self.multitarget_box, 0, 0)
            grid.addWidget(self.targetenemy_box, 0, 1)
            grid.addWidget(self.targetback_box, 0, 2)

            properties_layout.setSpacing(10)
            properties_layout.addWidget(panel)

        # Strings Start
        if self.version in (GameID.ML3R, GameID.ML1R, GameID.ML5):
            separator = QtWidgets.QFrame()
            separator.setFrameShape(QtWidgets.QFrame.HLine)
            separator.setFrameShadow(QtWidgets.QFrame.Sunken)
            properties_layout.addWidget(separator)
            strings = QtWidgets.QWidget()
            strings_layout = QtWidgets.QVBoxLayout(strings)
            strings_layout.setContentsMargins(0, 0, 0, 0)
            strings_layout.setSpacing(0)

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
            grid.setContentsMargins(0, 5, 0, 0)
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
            self.name_string_label.setAlignment(QtCore.Qt.AlignLeft)
            self.name_string_label.setMaxLength(0x17)
            self.name_string_value = QtWidgets.QLineEdit()
            self.name_string_value.setAlignment(QtCore.Qt.AlignLeft)
            self.name_string_value.setEnabled(True)
            self.name_string_value.setReadOnly(True)
            grid.addWidget(label, 1, 0)
            grid.addWidget(self.name_string_label, 1, 1)
            grid.addWidget(self.name_string_value, 1, 2)

            label = QtWidgets.QLabel("Plural")
            self.plural_string_label = QtWidgets.QLineEdit()
            self.plural_string_label.setAlignment(QtCore.Qt.AlignLeft)
            self.plural_string_label.setMaxLength(0x17)
            self.plural_string_value = QtWidgets.QLineEdit()
            self.plural_string_value.setAlignment(QtCore.Qt.AlignLeft)
            self.plural_string_value.setEnabled(True)
            self.plural_string_value.setReadOnly(True)
            grid.addWidget(label, 2, 0)
            grid.addWidget(self.plural_string_label, 2, 1)
            grid.addWidget(self.plural_string_value, 2, 2)

            label = QtWidgets.QLabel("Desc.")
            self.description_string_label = QtWidgets.QLineEdit()
            self.description_string_label.setAlignment(QtCore.Qt.AlignLeft)
            self.description_string_label.setMaxLength(0x17)
            self.description_string_value = QtWidgets.QLineEdit()
            self.description_string_value.setAlignment(QtCore.Qt.AlignLeft)
            self.description_string_value.setEnabled(True)
            self.description_string_value.setReadOnly(True)
            grid.addWidget(label, 3, 0)
            grid.addWidget(self.description_string_label, 3, 1)
            grid.addWidget(self.description_string_value, 3, 2)

            label = QtWidgets.QLabel("Full")
            self.full_string_label = QtWidgets.QLineEdit()
            self.full_string_label.setAlignment(QtCore.Qt.AlignLeft)
            self.full_string_label.setMaxLength(0x17)
            self.full_string_value = QtWidgets.QLineEdit()
            self.full_string_value.setAlignment(QtCore.Qt.AlignLeft)
            self.full_string_value.setEnabled(True)
            self.full_string_value.setReadOnly(True)
            grid.addWidget(label, 4, 0)
            grid.addWidget(self.full_string_label, 4, 1)
            grid.addWidget(self.full_string_value, 4, 2)

            strings_layout.addLayout(grid)
            properties_layout.addWidget(strings)

        
        # String labels
        self.bind_widget(self.name_string_label.textChanged, self.set_name_label)
        self.bind_widget(self.plural_string_label.textChanged, self.set_nams_label)
        self.bind_widget(self.description_string_label.textChanged, self.set_desc_label)
        self.bind_widget(self.full_string_label.textChanged, self.set_full_label)
        

        self.populate_items()

    def populate_items(self):
        self.item_list.clear()
        self.display_order.clear()
        items = Data.ITEMDATA.get(self.item_key, [])
        items_by_id = {item.id: item for item in items}
        for item in items:
            entry = QtWidgets.QListWidgetItem(f"#{item.id:04X} - {item.getName(Persistent.UI_DB_LANGUAGE)}")
            entry.setData(QtCore.Qt.ItemDataRole.UserRole, item)
            self.item_list.addItem(entry)
        order_data = Data.INV_ORDER.get(
            self.item_key,
            {"list": [], "padding": None},
        )
        for item_id in order_data["list"]:
            item = items_by_id.get(item_id)
            if item is None:
                continue
            entry = QtWidgets.QListWidgetItem(f"#{item.id:04X} - {item.getDefaultName()}")
            entry.setData(QtCore.Qt.ItemDataRole.UserRole, item)
            self.display_order.addItem(entry)
        if self.item_list.count():
            self.item_list.setCurrentRow(0)
            self.refresh_form()
        self.update_display_order_buttons()

    def get_current_item(self):
        entry = self.item_list.currentItem()
        if entry is None:
            return None
        return entry.data(QtCore.Qt.UserRole)

    def on_item_selected(self, current, previous):
        self.refresh_form()
        self.update_display_order_buttons()

    def refresh_form(self):
        item = self.get_current_item()
        if item is None:
            return
        self._refreshing = True
        try:
            if self.version == GameID.ML3R:
                self.refresh_ML3R(item)
            elif self.version == GameID.ML1R:
                self.refresh_ML1R(item)
            elif self.version == GameID.ML5:
                self.refresh_ML5(item)
                
            self.refresh_strings()
        finally:
            self._refreshing = False

    def refresh_ML3R(self, item):
        self.refresh_effect_form(item)
        self.id_box.setText(f"{item.id:X}" if item.id is not None else "")
        self.sprite_box.setValue(item.sprite or 0)
        self.price_box.setValue(item.price or 0)
        if self.item_key == "UITM":
            self.usemenu_box.setChecked(item.use_menu)
            self.mushroom_box.setChecked(item.is_mushroom)
            self.pocket_box.setCurrentIndex(self.pocket_box.findData(1 if item.mushroom_pocket else 0))
            self.multitarget_box.setCurrentIndex(self.multitarget_box.findData(1 if item.target_multi else 0))
            self.condition_box.setCurrentIndex(max(self.condition_box.findData(item.use_condition), 0))
            self.user_box.setCurrentIndex(max(self.user_box.findData(item.user), 0))
        elif self.item_key == "EITM":
            self.hp_box.setValue(item.hp or 0)
            self.bp_box.setValue(item.bp or 0)
            self.pow_box.setValue(item.pwr or 0)
            self.def_box.setValue(item.dfn or 0)
            self.spe_box.setValue(item.spe or 0)
            self.sta_box.setValue(item.sta or 0)
            self.user_box.setCurrentIndex(max(self.user_box.findData(item.user), 0))
            self.category_box.setCurrentIndex(max(self.category_box.findData(item.type), 0))

    def refresh_ML1R(self, item):
        self.id_box.setText(f"{item.id:X}" if item.id is not None else "")
        self.sprite_box.setValue(item.sprite or 0)
        if self.item_key == "UITM":
            self.refresh_effect_form(item)
            self.price_box.setValue(item.price or 0)
            self.mushstat_box.setValue(item.unk1 or 0)
            self.usemenu_box.setChecked(item.use_menu)
            self.pocket_box.setCurrentIndex(self.pocket_box.findData(1 if item.mushroom_pocket else 0))
            self.multitarget_box.setCurrentIndex(self.multitarget_box.findData(1 if item.target_multi else 0))
            self.condition_box.setCurrentIndex(max(self.condition_box.findData(item.use_condition), 0))
        elif self.item_key in ("WITM", "BITM"):
            self.refresh_effect_form(item)
            self.price_box.setValue(item.price or 0)
            self.hp_box.setValue(item.hp or 0)
            self.bp_box.setValue(item.bp or 0)
            self.pow_box.setValue(item.pwr or 0)
            self.def_box.setValue(item.dfn or 0)
            self.spe_box.setValue(item.spe or 0)
            self.sta_box.setValue(item.sta or 0)
            if self.item_key == "WITM":
                self.user_box.setCurrentIndex(max(self.user_box.findData(item.user), 0))

    def refresh_ML5(self, item):
        self.refresh_effect_form(item)
        self.id_box.setText(f"{item.id:X}" if item.id is not None else "")
        self.sprite_box.setValue(item.sprite or 0)
        self.price_box.setValue(item.price or 0)
        if self.item_key == "UITM":
            self.pocket_box.setText(self.get_pocket(item))
            self.usemenu_box.setChecked(item.use_menu)
            self.usebattle_box.setChecked(item.use_battle)
            self.usering_box.setChecked(item.use_arcade)
            self.mushroom_box.setChecked(item.is_mushroom)
            self.bean_box.setChecked(item.is_bean)
            self.multitarget_box.setChecked(item.target_multi)
            self.targetenemy_box.setChecked(item.target_enemy)
            self.targetback_box.setChecked(item.target_back)
            self.condition_box.setCurrentIndex(max(self.condition_box.findData(item.use_condition), 0))
            self.user_box.setCurrentIndex(max(self.user_box.findData(item.user), 0))
        elif self.item_key == "EITM":
            self.hp_box.setValue(item.hp or 0)
            self.bp_box.setValue(item.bp or 0)
            self.pow_box.setValue(item.pwr or 0)
            self.def_box.setValue(item.dfn or 0)
            self.spe_box.setValue(item.spe or 0)
            self.sta_box.setValue(item.sta or 0)
            self.user_box.setCurrentIndex(max(self.user_box.findData(item.user), 0))
            self.category_box.setCurrentIndex(max(self.category_box.findData(item.type), 0))


    def refresh_effect_form(self, item):
        effect_id = item.effect_id
        index = max(self.effect_box.findData(effect_id), 0)
        self.effect_box.setCurrentIndex(index)

        effect = self.get_effect_definition(self.effect_box.currentData())
        self.effect_note.setText(str(effect.get("note", "")))
        self.param1_note.setText(str(effect.get("param1", "")))
        self.param1_box.setValue(item.effect_param1 or 0)

        if self._effectParam2():
            self.param2_note.setText(str(effect.get("param2", "")))
            self.param2_box.setValue(item.effect_param2 or 0)

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

    def set_mushstat(self, item, value):
        if self.version == GameID.ML1R:
            item.unk1 = value

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

    def set_effect_param1(self, item, value):
        item.effect_param1 = value

    def set_effect_param2(self, item, value):
        item.effect_param2 = value

    def set_pocket(self, item, index):
        value = self.pocket_box.itemData(index)
        if value is None:
            return
        item.mushroom_pocket = bool(value)

    def get_pocket(self, item):
        if item.is_mushroom:
            return "Mushroom"
        # TODO: For the sprites, the game looks for matching sprites from items UITM_nut/UITM_sirup/UITM_candy
        if item.sprite == 4:
            return "Nut"
        if item.sprite in (6, 8):
            return "Syrup"
        if item.is_bean:
            return "Bean"
        return "Other"

    def set_condition(self, item, index):
        condition_id = self.condition_box.itemData(index)
        if condition_id is None:
            return
        item.use_condition = condition_id

    def set_multitarget(self, item, index):
        # Combobox
        if self.version in (GameID.ML3R, GameID.ML1R):
            value = self.multitarget_box.itemData(index)
            if value is None:
                return
            item.target_multi = bool(value)
        # Checkbox
        elif self.version == GameID.ML5:
            item.target_multi = index

    def set_targetenemy(self, item, checked):
        item.target_enemy = checked

    def set_targetback(self, item, checked):
        item.target_back = checked

    def set_user(self, item, index):
        user_id = self.user_box.itemData(index)
        if user_id is None:
            return
        item.user = user_id

    def set_category(self, item, index):
        type_id = self.category_box.itemData(index)
        if type_id is None:
            return
        item.type = type_id

    def set_usemenu(self, item, checked):
        item.use_menu = checked

    def set_usebattle(self, item, checked):
        item.use_battle = checked

    def set_usegauntlet(self, item, checked):
        item.use_arcade = checked

    def set_mushroom(self, item, checked):
        item.is_mushroom = checked

    def set_bean(self, item, checked):
        item.is_bean = checked

    def set_hp(self, item, value):
        item.hp = value

    def set_bp(self, item, value):
        item.bp = value

    def set_pow(self, item, value):
        item.pwr = value

    def set_def(self, item, value):
        item.dfn = value

    def set_spe(self, item, value):
        item.spe = value

    def set_sta(self, item, value):
        item.sta = value



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
        language = self.current_language
        text = f"#{item.id:04X} - {item.getDefaultName()}"
        for widget in (self.item_list, self.display_order):
            for i in range(widget.count()):
                entry = widget.item(i)
                stored_item = entry.data(QtCore.Qt.UserRole)
                if stored_item is not None and stored_item.id == item.id:
                    entry.setText(text)
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

    def add_display_order_item(self):
        item = self.get_current_item()
        if item is None:
            return
        item_id = item.id
        existing_ids = {
            self.display_order.item(i).data(QtCore.Qt.ItemDataRole.UserRole).id
            for i in range(self.display_order.count())
        }
        if item_id in existing_ids:
            self.update_display_order_buttons()
            return
        entry = QtWidgets.QListWidgetItem(f"#{item.id:04X} - {item.getDefaultName()}")
        entry.setData(QtCore.Qt.ItemDataRole.UserRole, item)
        self.display_order.addItem(entry)
        new_row = self.display_order.count() - 1
        self.display_order.setCurrentRow(new_row)
        self.display_order.setFocus()
        self.sync_display_order()
        self.update_display_order_buttons()

    def remove_display_order_item(self):
        item = self.get_current_item()
        if item is None or self.display_order.count() <= 1:
            self.update_display_order_buttons()
            return
        item_id = item.id
        for row in range(self.display_order.count()):
            entry = self.display_order.item(row)
            stored_item = entry.data(QtCore.Qt.ItemDataRole.UserRole)
            if stored_item is not None and stored_item.id == item_id:
                self.display_order.takeItem(row)
                self.sync_display_order()
                if self.display_order.count():
                    selected_row = max(0, row - 1)
                    selected_row = min(selected_row, self.display_order.count() - 1)
                    self.display_order.setCurrentRow(selected_row)
                    self.display_order.setFocus()
                break
        self.update_display_order_buttons()

    def sync_display_order(self):
        order_data = Data.INV_ORDER.setdefault(
            self.item_key,
            {"list": [], "padding": None},
        )
        order_data["list"] = [
            self.display_order.item(i).data(QtCore.Qt.ItemDataRole.UserRole).id
            for i in range(self.display_order.count())
        ]

    def update_display_order_buttons(self):
        item = self.get_current_item()
        if item is None:
            self.display_order_add.setText("Add entry")
            self.display_order_remove.setText("Delete entry")
            self.display_order_add.setEnabled(False)
            self.display_order_remove.setEnabled(False)
            return

        item_id = item.id
        already_added = any(
            self.display_order.item(i).data(QtCore.Qt.ItemDataRole.UserRole).id == item_id
            for i in range(self.display_order.count())
            if self.display_order.item(i).data(QtCore.Qt.ItemDataRole.UserRole) is not None
        )
        self.display_order_add.setText(f"Add #{item_id:04X}")
        self.display_order_remove.setText(f"Delete #{item_id:04X}")
        self.display_order_add.setEnabled(not already_added)
        self.display_order_remove.setEnabled( already_added and self.display_order.count() > 1)

    def move_display_order_item(self, offset):
        row = self.display_order.currentRow()
        new_row = row + offset
        if row < 0 or not 0 <= new_row < self.display_order.count():
            return
        item = self.display_order.takeItem(row)
        self.display_order.insertItem(new_row, item)
        self.display_order.setCurrentRow(new_row)
        self.sync_display_order()
        self.update_display_order_buttons()

    def _isItem(self):
        return (self.item_key == "UITM")

    def _hasEffect(self):
        if self.version == GameID.ML1R:
            return (self.item_key in ("UITM", "WITM", "BITM", "SITM"))
        elif self.version in (GameID.ML5, GameID.ML3R):
            return (self.item_key in ("UITM", "EITM", "BITM", "CITM"))

    def _hasStats(self):
        if self.version == GameID.ML1R:
            return (self.item_key in ("WITM", "BITM"))
        elif self.version in (GameID.ML5, GameID.ML3R):
            return (self.item_key == "EITM")

    def _effectParam2(self):
        if self.version == GameID.ML1R:
            return False
        elif self.version in (GameID.ML5, GameID.ML3R):
            return (self.item_key == "EITM")