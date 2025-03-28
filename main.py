import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from qt_designer.form import Ui_MainWindow
from tab_spectrometer import SpectrometerTab
from tab_frog import FrogTab

fs = 1e-15
um = 1e-6
mm = 1e-3


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.tab_spectrometer = SpectrometerTab(self)
        self.tab_frog = FrogTab(self)

    def closeEvent(self, event):
        self.tab_spectrometer.closeEvent(event)
        self.tab_frog.closeEvent(event)
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
