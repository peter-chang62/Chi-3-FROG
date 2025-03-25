import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from qt_designer.form import Ui_MainWindow

from PyQt5 import QtWidgets, QtCore, QtGui
from scipy.constants import c
import numpy as np
from spectrometer import StellarnetBlueWave
from motor_stage import ZaberStage

fs = 1e-15
um = 1e-6


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.tab_spectrometer = SpectrometerTab(self.ui)


class SpectrometerTab:
    def __init__(self, ui):
        ui: Ui_MainWindow
        self.ui = ui

        self.set_validators()
        self.connect_line_edits_signals_slots()
        self.connect_push_buttons_signals_slots()

    def initialize_hardware(self):
        try:
            self.spectrometer = StellarnetBlueWave()
        except Exception as e:
            self.ui.le_error.setText(str(e))
            self.spectrometer.reset()
        try:
            self.stage = ZaberStage(self.ui.le_stage_com_port.text())
        except Exception as e:
            self.ui.le_error.setText(str(e))
            self.stage.ser.close()

        self.ui.le_error.setText("success")

    def set_validators(self):
        ui = self.ui
        line_edits = [
            ui.le_step_fs,
            ui.le_step_um,
            ui.le_target_pos_fs,
            ui.le_target_pos_um,
            ui.le_ymax,
            ui.le_ymin,
            ui.le_xmax,
            ui.le_xmin,
        ]
        [i.setValidator(QtGui.QDoubleValidator()) for i in line_edits]

    def connect_line_edits_signals_slots(self):
        self.ui.le_step_fs.editingFinished.connect(self.slot_le_step_fs)
        self.ui.le_step_um.editingFinished.connect(self.slot_le_step_um)
        self.ui.le_target_pos_fs.editingFinished.connect(self.slot_le_target_pos_fs)
        self.ui.le_target_pos_um.editingFinished.connect(self.slot_le_target_pos_um)

    def connect_push_buttons_signals_slots(self):
        self.ui.pb_initialize_hardware.clicked.connect(self.initialize_hardware)

    # -------- relative move --------------------------------------------------
    @property
    def step_um(self):
        return float(self.ui.le_step_um.text())

    @property
    def step_fs(self):
        return (2 * self.step_um * um / c) / fs

    @step_um.setter
    def step_um(self, step_um):
        self.ui.le_step_um.setText(str(np.round(step_um, 3)))
        self.ui.le_step_fs.setText(str(np.round(self.step_fs, 3)))

    @step_fs.setter
    def step_fs(self, step_fs):
        self.step_um = (c * step_fs * fs / 2) / um

    # -------- absolute move --------------------------------------------------
    @property
    def T0_um(self):
        return np.genfromtxt("T0_um.txt")

    @T0_um.setter
    def T0_um(self, T0_um):
        np.savetxt("T0_um.txt", np.asarray(T0_um))

    @property
    def target_pos_um(self):
        return float(self.ui.le_target_pos_um.text())

    @property
    def target_pos_fs(self):
        return (2 * (self.target_pos_um - self.T0_um) * um / c) / fs

    @target_pos_um.setter
    def target_pos_um(self, target_pos_um):
        self.ui.le_target_pos_um.setText(str(np.round(target_pos_um, 3)))
        self.ui.le_target_pos_fs.setText(str(np.round(self.target_pos_fs, 3)))

    @target_pos_fs.setter
    def target_pos_fs(self, target_pos_fs):
        self.target_pos_um = (c * target_pos_fs * fs / 2) / um + self.T0_um

    def slot_le_step_fs(self):
        self.step_fs = float(self.ui.le_step_fs.text())

    def slot_le_step_um(self):
        self.step_um = float(self.ui.le_step_um.text())

    def slot_le_target_pos_fs(self):
        self.target_pos_fs = float(self.ui.le_target_pos_fs.text())

    def slot_le_target_pos_um(self):
        self.target_pos_um = float(self.ui.le_target_pos_um.text())

    # -------------------------------------------------------------------------


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
