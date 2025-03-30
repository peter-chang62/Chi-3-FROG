from qt_designer.form import Ui_MainWindow
from PyQt5 import QtGui
from spectrometer import StellarnetBlueWave


# from tab_spectrometer import SpectrometerTab
# from tab_frog import FrogTab


class SettingsTab:
    def __init__(self, ui, tab_spectrometer, tab_frog):
        ui: Ui_MainWindow
        spectrometer: StellarnetBlueWave
        # tab_spectrometer: SpectrometerTab
        # tab_frog: FrogTab
        self.ui = ui
        self.tab_spectrometer = tab_spectrometer
        self.tab_frog = tab_frog

        self.set_validators()
        self.connect_line_edits_signals_slots()

    def set_validators(self):
        self.ui.le_integration_time.setValidator(QtGui.QIntValidator(5, 1000))
        self.ui.le_n_avg.setValidator(QtGui.QIntValidator(1, 1000))
        self.ui.le_x_smooth.setValidator(QtGui.QIntValidator(0, 4))
        self.ui.le_x_timing.setValidator(QtGui.QIntValidator(1, 3))

    def connect_line_edits_signals_slots(self):
        self.ui.le_integration_time.editingFinished.connect(
            self.slot_le_integration_time
        )
        self.ui.le_n_avg.editingFinished.connect(self.slot_le_n_avg)
        self.ui.le_x_smooth.editingFinished.connect(self.slot_le_x_smooth)
        self.ui.le_x_timing.editingFinished.connect(self.slot_le_x_timing)

    @property
    def _initialized_hardware(self):
        return self.tab_spectrometer._initialized_hardware

    @property
    def spectrometer(self):
        return self.tab_spectrometer.spectrometer

    @property
    def integration_time(self):
        return self.spectrometer.integration_time

    @integration_time.setter
    def integration_time(self, val):
        self.spectrometer.integration_time = val

    @property
    def n_avg(self):
        return self.spectrometer.n_avg

    @n_avg.setter
    def n_avg(self, val):
        self.spectrometer.n_avg = val

    @property
    def x_smooth(self):
        return self.spectrometer.x_smooth

    @x_smooth.setter
    def x_smooth(self, val):
        self.spectrometer.x_smooth = val

    @property
    def x_timing(self):
        return self.spectrometer.x_timing

    @x_timing.setter
    def x_timing(self, val):
        self.spectrometer.x_timing = val

    # --------- slots ---------------------------------------------------------
    def slot_le_integration_time(self):
        if not self._initialized_hardware:
            self.ui.tb_settings_error.setPlainText("no hardware initialized")
            return

        if self.tab_frog.thread_frog.isRunning():
            self.ui.tb_settings_error.setPlainText("FROG is running")
            return

        if self.tab_spectrometer.thread_spec.isRunning():
            self.ui.tb_settings_error.setPlainText("spectrometer is running")
            return

        self.integration_time = int(self.ui.le_integration_time.text())

    def slot_le_n_avg(self):
        if not self._initialized_hardware:
            self.ui.tb_settings_error.setPlainText("no hardware initialized")
            return

        if self.tab_frog.thread_frog.isRunning():
            self.ui.tb_settings_error.setPlainText("FROG is running")
            return

        if self.tab_spectrometer.thread_spec.isRunning():
            self.ui.tb_settings_error.setPlainText("spectrometer is running")
            return

        self.n_avg = int(self.ui.le_n_avg.text())

    def slot_le_x_smooth(self):
        if not self._initialized_hardware:
            self.ui.tb_settings_error.setPlainText("no hardware initialized")
            return

        if self.tab_frog.thread_frog.isRunning():
            self.ui.tb_settings_error.setPlainText("FROG is running")
            return

        if self.tab_spectrometer.thread_spec.isRunning():
            self.ui.tb_settings_error.setPlainText("spectrometer is running")
            return

        self.x_smooth = int(self.ui.le_x_smooth.text())

    def slot_le_x_timing(self):
        if not self._initialized_hardware:
            self.ui.tb_settings_error.setPlainText("no hardware initialized")
            return

        if self.tab_frog.thread_frog.isRunning():
            self.ui.tb_settings_error.setPlainText("FROG is running")
            return

        if self.tab_spectrometer.thread_spec.isRunning():
            self.ui.tb_settings_error.setPlainText("spectrometer is running")
            return

        self.x_timing = int(self.ui.le_x_timing.text())
