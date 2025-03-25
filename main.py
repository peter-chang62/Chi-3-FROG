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
mm = 1e-3


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.tab_spectrometer = SpectrometerTab(self.ui)

    def closeEvent(self, event):
        self.tab_spectrometer.closeEvent(event)
        super().closeEvent(event)


class SpectrometerTab:
    def __init__(self, ui):
        ui: Ui_MainWindow
        self.ui = ui

        self.set_validators()
        self.connect_line_edits_signals_slots()
        self.connect_push_buttons_signals_slots()

        self._initialized_hardware = False

    def initialize_hardware(self):
        if self._initialized_hardware:
            self.ui.le_error.setText("hardware already initialized")
            return

        # fetch spectrometer
        try:
            self.spectrometer = StellarnetBlueWave()
            self.ui.le_error.setText("success")
        except Exception as e:
            self.ui.le_error.setText(str(e))
            self.spectrometer.reset()  # release spectrometer
            return

        # successfuly fetched spectrometer
        # now fetch the stage
        try:
            self.stage = ZaberStage(self.ui.le_stage_com_port.text())
            self.ui.le_error.setText("success")
        except Exception as e:
            self.ui.le_error.setText(str(e))
            self.stage.ser.close()  # release stage
            self.spectrometer.reset()  # and release spectrometer
            return

        self._initialized_hardware = True

    def closeEvent(self, event):
        if self._initialized_hardware:
            self.spectrometer.reset()
            self.stage.ser.close()

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
        self.ui.pb_step_back.clicked.connect(self.slot_pb_step_back)
        self.ui.pb_step_forward.clicked.connect(self.slot_pb_step_forward)
        self.ui.pb_home.clicked.connect(self.slot_pb_home)
        self.ui.pb_absolute_move.clicked.connect(self.slot_pb_absolute_move)
        self.ui.pb_set_t0.clicked.connect(self.slot_pb_set_t0)

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
        np.savetxt("T0_um.txt", np.asarray([T0_um]))

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

    def slot_pb_home(self):
        if self._initialized_hardware:
            self.stage.home()
        else:
            self.ui.le_error.setText("no hardware initialized")

    def slot_pb_absolute_move(self):
        if not self._initialized_hardware:
            self.ui.le_error.setText("no hardware initialized")
            return

        x = self.ui.le_target_pos_um.text()
        if x == "":
            self.ui.le_error.setText("where to?")
            return

        x = float(x) * um / mm
        x_encoder = x / self.stage._max_range * self.stage._max_pos
        self.stage.move_absolute(int(np.round(x_encoder)))

    def slot_pb_step_back(self):
        if not self._initialized_hardware:
            self.ui.le_error.setText("no hardware initialized")
            return

        x = self.ui.le_step_um.text()
        if x == "":
            self.ui.le_error.setText("where to?")
            return

        x = float(x) * um / mm
        x_encoder = x / self.stage._max_range * self.stage._max_pos
        self.stage.move_relative(int(np.round(-x_encoder)))

    def slot_pb_step_forward(self):
        if not self._initialized_hardware:
            self.ui.le_error.setText("no hardware initialized")
            return

        x = self.ui.le_step_um.text()
        if x == "":
            self.ui.le_error.setText("where to?")
            return

        x = float(x) * um / mm
        x_encoder = x / self.stage._max_range * self.stage._max_pos
        self.stage.move_relative(int(np.round(x_encoder)))

    def slot_pb_set_t0(self):
        (x_encoder,) = self.stage.return_current_position()
        x = x_encoder / self.stage._max_pos * self.stage._max_range * mm / um
        self.T0_um = x

        self.slot_lcd_current_pos_um()
        self.slot_le_target_pos_fs()

    def slot_lcd_current_pos_um(self):
        (x_encoder,) = self.stage.return_current_position()
        x = x_encoder / self.stage._max_pos * self.stage._max_range * mm / um
        self.ui.lcd_current_pos_um.display(np.round(x, 3))
        self.ui.lcd_current_pos_fs.display(
            np.round((2 * (x - self.T0_um) * um / c) / fs, 3)
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
