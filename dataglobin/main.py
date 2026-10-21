import os
import sys
from PySide6 import QtWidgets

from dataglobin.window import MainWindow
import dataglobin.persistent as Persistent

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Dataglobin-DX")
    app.setOrganizationName("Dataglobin-DX")
    if os.name == 'nt':
        app.setStyle('Fusion')

    Persistent.import_config()

    window = MainWindow()

    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
