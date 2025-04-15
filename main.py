import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from qt_designer.form import Ui_MainWindow
from tab_spectrometer import SpectrometerTab
from tab_frog import FrogTab
from tab_settings import SettingsTab
from PyQt5 import QtCore
import os

fs = 1e-15
um = 1e-6
mm = 1e-3


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.tab_spectrometer = SpectrometerTab(self.ui)
        self.tab_frog = FrogTab(self.ui, self.tab_spectrometer)
        self.tab_spectrometer.tab_frog = self.tab_frog
        self.tab_settings = SettingsTab(self.ui, self.tab_spectrometer, self.tab_frog)
        self.tab_spectrometer.tab_settings = self.tab_settings

    def closeEvent(self, event):
        self.tab_frog.closeEvent(event)
        self.tab_spectrometer.closeEvent(event)
        super().closeEvent(event)


if __name__ == "__main__":
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
