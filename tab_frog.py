from qt_designer.form import Ui_MainWindow
import threading
from PyQt5 import QtCore, QtGui
from scipy.constants import c
import numpy as np
from spectrometer import StellarnetBlueWave
from motor_stage import ZaberStage
import pyqtgraph as pg

fs = 1e-15
um = 1e-6
mm = 1e-3


def create_curve(color="b", width=2, x=None, y=None):
    curve = pg.PlotDataItem(pen=pg.mkPen(color=color, width=width))
    if (x is not None) and (y is not None):
        curve.setData(x, y)
    return curve


class FrogTab:
    def __init__(self, ui):
        ui: Ui_MainWindow
        self.ui = ui

        self.set_validators()

    def closeEvent(self, event):
        pass

    def set_validators(self):
        ui = self.ui
        line_edits = [
            ui.le_frog_start_fs,
            ui.le_frog_start_um,
            ui.le_frog_end_fs,
            ui.le_frog_end_um,
            ui.le_frog_step_fs,
            ui.le_frog_step_um,
        ]
        [i.setValidator(QtGui.QDoubleValidator()) for i in line_edits]

    @property
    def T0_um(self):
        return self.ui.tab_spectrometer.T0_um

    @property
    def _initialized_hardware(self):
        return self.ui.tab_spectrometer._initialized_hardware

    @property
    def spectrometer(self):
        return self.ui.tab_spectrometer.spectrometer

    @property
    def stage(self):
        return self.ui.tab_spectrometer.stage

    @property
    def frog_start_um(self):
        return float(self.ui.le_frog_start_um.text())

    @property
    def frog_start_fs(self):
        return (2 * (self.frog_start_um - self.T0_um) * um / c) / fs

    @frog_start_um.setter
    def frog_start_um(self, frog_start_um):
        self.ui.le_frog_start_um.setText(str(np.round(frog_start_um, 3)))
        self.ui.le_frog_start_fs.setText(str(np.round(self.frog_start_fs, 3)))

    @frog_start_fs.setter
    def frog_start_fs(self, frog_start_fs):
        self.frog_start_um = (c * frog_start_fs * fs / 2) / um + self.T0_um
