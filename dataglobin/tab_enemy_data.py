from PySide6 import QtWidgets

class EnemyDataTab(QtWidgets.QWidget):
    def __init__(self, monster_data=None, monster_names=None, overlay_BObjMon_offsets=None, overlay_BObj=None, BObjMon_file=None, parent=None):
        super().__init__(parent)

        main_layout = QtWidgets.QHBoxLayout(self)

        self.enemy_list = QtWidgets.QListWidget()
        self.enemy_list.setMinimumWidth(180)
        self.enemy_list.addItems(["Monster 1", "Monster 2", "Monster 3"])
        main_layout.addWidget(self.enemy_list)

        enemy_area = QtWidgets.QWidget()
        enemy_layout = QtWidgets.QVBoxLayout(enemy_area)
        main_layout.addWidget(enemy_area, 1)

        monster_properties = QtWidgets.QWidget()
        monster_properties_layout = QtWidgets.QGridLayout(monster_properties)
        enemy_layout.addWidget(monster_properties)

        appearance = QtWidgets.QWidget()
        appearance_layout = QtWidgets.QGridLayout(appearance)
        appearance_layout.setContentsMargins(0, 0, 0, 0)
        monster_properties_layout.addWidget(appearance, 0, 0, 5, 1)

        name_label = QtWidgets.QLabel("Name")
        self.name_box = QtWidgets.QComboBox()
        appearance_layout.addWidget(name_label, 1, 1)
        appearance_layout.addWidget(self.name_box, 2, 1)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        monster_properties_layout.addWidget(line, 0, 1, 5, 1)

        stats = QtWidgets.QWidget()
        stats_layout = QtWidgets.QGridLayout(stats)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        monster_properties_layout.addWidget(stats, 0, 2)

        hp_label = QtWidgets.QLabel("HP")
        self.hp_box = QtWidgets.QSpinBox()
        stats_layout.addWidget(hp_label, 0, 0)
        stats_layout.addWidget(self.hp_box, 1, 0)

        pow_label = QtWidgets.QLabel("POW")
        self.pow_box = QtWidgets.QSpinBox()
        stats_layout.addWidget(pow_label, 0, 1)
        stats_layout.addWidget(self.pow_box, 1, 1)

        def_label = QtWidgets.QLabel("DEF")
        self.def_box = QtWidgets.QSpinBox()
        stats_layout.addWidget(def_label, 0, 2)
        stats_layout.addWidget(self.def_box, 1, 2)

        speed_label = QtWidgets.QLabel("SPE")
        self.speed_box = QtWidgets.QSpinBox()
        stats_layout.addWidget(speed_label, 0, 3)
        stats_layout.addWidget(self.speed_box, 1, 3)

        lv_label = QtWidgets.QLabel("LV")
        self.lv_box = QtWidgets.QSpinBox()
        stats_layout.addWidget(lv_label, 2, 0)
        stats_layout.addWidget(self.lv_box, 3, 0)

        exp_label = QtWidgets.QLabel("EXP")
        self.exp_box = QtWidgets.QSpinBox()
        stats_layout.addWidget(exp_label, 2, 1)
        stats_layout.addWidget(self.exp_box, 3, 1)

        coins_label = QtWidgets.QLabel("Coins")
        self.coins_box = QtWidgets.QSpinBox()
        stats_layout.addWidget(coins_label, 2, 2)
        stats_layout.addWidget(self.coins_box, 3, 2)

        properties = QtWidgets.QWidget()
        properties_layout = QtWidgets.QGridLayout(properties)
        properties_layout.setContentsMargins(0, 0, 0, 0)
        monster_properties_layout.addWidget(properties, 2, 2)

        burn_label = QtWidgets.QLabel("Burn Chance")
        self.burn_box = QtWidgets.QComboBox()
        self.burn_box.addItems(["Normal", "Double", "Half", "Immune"])
        properties_layout.addWidget(burn_label, 0, 0)
        properties_layout.addWidget(self.burn_box, 1, 0)

        dizzy_label = QtWidgets.QLabel("Dizzy Chance")
        self.dizzy_box = QtWidgets.QComboBox()
        self.dizzy_box.addItems(["Normal", "Double", "Half", "Immune"])
        properties_layout.addWidget(dizzy_label, 0, 1)
        properties_layout.addWidget(self.dizzy_box, 1, 1)

        fire_label = QtWidgets.QLabel("Fire Damage")
        self.fire_box = QtWidgets.QComboBox()
        self.fire_box.addItems(["Normal", "Critical", "Half", "Immune"])
        properties_layout.addWidget(fire_label, 0, 2)
        properties_layout.addWidget(self.fire_box, 1, 2)

        stat_down_label = QtWidgets.QLabel("Stat Down Chance")
        self.stat_down_box = QtWidgets.QComboBox()
        self.stat_down_box.addItems(["Normal", "Double", "Half", "Immune"])
        properties_layout.addWidget(stat_down_label, 2, 0)
        properties_layout.addWidget(self.stat_down_box, 3, 0)

        instant_ko_label = QtWidgets.QLabel("Instant KO Chance")
        self.instant_ko_box = QtWidgets.QComboBox()
        self.instant_ko_box.addItems(["Normal", "Double", "Half", "Immune"])
        properties_layout.addWidget(instant_ko_label, 2, 1)
        properties_layout.addWidget(self.instant_ko_box, 3, 1)

        drops = QtWidgets.QWidget()
        drops_layout = QtWidgets.QGridLayout(drops)
        drops_layout.setContentsMargins(0, 0, 0, 0)
        monster_properties_layout.addWidget(drops, 4, 2)

        normal_item_label = QtWidgets.QLabel("Normal Item")
        self.normal_item_box = QtWidgets.QLineEdit()
        drops_layout.addWidget(normal_item_label, 0, 0)
        drops_layout.addWidget(self.normal_item_box, 1, 0)

        normal_rate_label = QtWidgets.QLabel("Normal Drop Rate")
        self.normal_rate_box = QtWidgets.QSpinBox()
        drops_layout.addWidget(normal_rate_label, 0, 1)
        drops_layout.addWidget(self.normal_rate_box, 1, 1)

        rare_item_label = QtWidgets.QLabel("Rare Item")
        self.rare_item_box = QtWidgets.QLineEdit()
        drops_layout.addWidget(rare_item_label, 2, 0)
        drops_layout.addWidget(self.rare_item_box, 3, 0)

        rare_rate_label = QtWidgets.QLabel("Rare Drop Rate")
        self.rare_rate_box = QtWidgets.QSpinBox()
        drops_layout.addWidget(rare_rate_label, 2, 1)
        drops_layout.addWidget(self.rare_rate_box, 3, 1)