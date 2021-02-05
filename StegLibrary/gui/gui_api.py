# Buildtin modules
import sys
from typing import NoReturn

# Internal modules
from StegLibrary.helper import err_imp
from StegLibrary.gui import MainWindow

# Non-builtin modules
try:
    from PyQt5 import QtWidgets
except ImportError:
    err_imp("PyQt5")
    exit(1)


def execute_gui() -> NoReturn:
    """Opens the GUI for StegLibrary."""
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())