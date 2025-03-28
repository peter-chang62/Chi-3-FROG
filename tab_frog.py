from qt_designer.form import Ui_MainWindow

# from tab_spectrometer import SpectrometerTab
import threading
from PyQt5 import QtCore, QtGui
from scipy.constants import c
import numpy as np
from spectrometer import StellarnetBlueWave
from motor_stage import ZaberStage
import pyqtgraph as pg
import struct
from PyQt5.QtGui import QTransform


fs = 1e-15
um = 1e-6
mm = 1e-3


def create_curve(color="b", width=2, x=None, y=None):
    curve = pg.PlotDataItem(pen=pg.mkPen(color=color, width=width))
    if (x is not None) and (y is not None):
        curve.setData(x, y)
    return curve


class FrogTab:
    def __init__(self, ui, tab_spectrometer):
        ui: Ui_MainWindow
        # tab_spectrometer: SpectrometerTab
        self.ui = ui
        self.tab_spectrometer = tab_spectrometer
        self.set_validators()
        self.connect_line_edits_signals_slots()
        self.connect_push_buttons_signals_slots()

        self.ui.progbar_frog.setValue(0)

        self.ui.gv_frog.ui.menuBtn.hide()
        self.ui.gv_frog.ui.histogram.hide()

        self._view_box = self.ui.gv_frog.getView()

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

    def connect_line_edits_signals_slots(self):
        self.ui.le_frog_start_fs.editingFinished.connect(self.slot_le_frog_start_fs)
        self.ui.le_frog_end_fs.editingFinished.connect(self.slot_le_frog_end_fs)
        self.ui.le_frog_step_fs.editingFinished.connect(self.slot_le_frog_step_fs)
        self.ui.le_frog_start_um.editingFinished.connect(self.slot_le_frog_start_um)
        self.ui.le_frog_end_um.editingFinished.connect(self.slot_le_frog_end_um)
        self.ui.le_frog_step_um.editingFinished.connect(self.slot_le_frog_step_um)

        self.slot_le_frog_start_fs()
        self.slot_le_frog_end_fs()
        self.slot_le_frog_step_fs()

    def connect_push_buttons_signals_slots(self):
        self.ui.pb_frog.clicked.connect(self.slot_pb_frog)

    def create_threads_workers(self):
        self.event_stop_frog = threading.Event()
        self.start_frog_event = threading.Event()
        self.thread_frog = QtCore.QThread()
        self.worker_frog = WorkerFrogStepScan(
            self.spectrometer,
            self.stage,
            self.event_stop_frog,
            self._x_encoder_step,
            self._N_steps,
            self.T0_um,
        )
        self.worker_frog.moveToThread(self.thread_frog)
        self.thread_frog.started.connect(self.worker_frog.loop)
        self.worker_frog.progress.connect(self.slot_frog_update)
        self.worker_frog.finished.connect(self.thread_frog.quit)
        self.tab_spectrometer.worker_stage.finished.connect(self.start_frog)

    @property
    def T0_um(self):
        return self.tab_spectrometer.T0_um

    @property
    def _initialized_hardware(self):
        return self.tab_spectrometer._initialized_hardware

    @property
    def spectrometer(self):
        return self.tab_spectrometer.spectrometer

    @property
    def stage(self):
        return self.tab_spectrometer.stage

    # ---------- line edits ---------------------------------------------------

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

    @property
    def frog_end_um(self):
        return float(self.ui.le_frog_end_um.text())

    @property
    def frog_end_fs(self):
        return (2 * (self.frog_end_um - self.T0_um) * um / c) / fs

    @frog_end_um.setter
    def frog_end_um(self, frog_end_um):
        self.ui.le_frog_end_um.setText(str(np.round(frog_end_um, 3)))
        self.ui.le_frog_end_fs.setText(str(np.round(self.frog_end_fs, 3)))

    @frog_end_fs.setter
    def frog_end_fs(self, frog_end_fs):
        self.frog_end_um = (c * frog_end_fs * fs / 2) / um + self.T0_um

    @property
    def frog_step_um(self):
        return float(self.ui.le_frog_step_um.text())

    @property
    def _x_encoder_start(self):
        x = self.frog_start_um * um / mm  # convert to mm
        x_encoder = x / self.stage._max_range * self.stage._max_pos
        return int(np.round(x_encoder))

    @property
    def _x_encoder_end(self):
        x = self.frog_end_um * um / mm  # convert to mm
        x_encoder = x / self.stage._max_range * self.stage._max_pos
        return int(np.round(x_encoder))

    @property
    def _x_encoder_step(self):
        x = self.frog_step_um * um / mm  # convert to mm
        x_encoder = x / self.stage._max_range * self.stage._max_pos
        return int(np.round(x_encoder))

    @property
    def _N_steps(self):
        end = self._x_encoder_end
        start = self._x_encoder_start
        step = self._x_encoder_step
        return int(np.round((end - start) / step))

    @property
    def frog_step_fs(self):
        return (2 * self.frog_step_um * um / c) / fs

    @frog_step_um.setter
    def frog_step_um(self, frog_step_um):
        self.ui.le_frog_step_um.setText(str(np.round(frog_step_um, 3)))
        self.ui.le_frog_step_fs.setText(str(np.round(self.frog_step_fs, 3)))

    @frog_step_fs.setter
    def frog_step_fs(self, frog_step_fs):
        self.frog_step_um = (c * frog_step_fs * fs / 2) / um

    def slot_le_frog_start_fs(self):
        self.frog_start_fs = float(self.ui.le_frog_start_fs.text())

    def slot_le_frog_start_um(self):
        self.frog_start_um = float(self.ui.le_frog_start_um.text())

    def slot_le_frog_end_fs(self):
        self.frog_end_fs = float(self.ui.le_frog_end_fs.text())

    def slot_le_frog_end_um(self):
        self.frog_end_um = float(self.ui.le_frog_end_um.text())

    def slot_le_frog_step_fs(self):
        self.frog_step_fs = float(self.ui.le_frog_step_fs.text())

    def slot_le_frog_step_um(self):
        self.frog_step_um = float(self.ui.le_frog_step_um.text())

    # ---------- frog ---------------------------------------------------------
    def slot_pb_frog(self):
        if not self._initialized_hardware:
            self.ui.tb_frog_error.setPlainText("no hardware initialized")
            return

        if self.thread_frog.isRunning():
            if not self.event_stop_frog.is_set():
                self.event_stop_frog.set()
            else:
                self.ui.tb_frog_error.setPlainText("wait for FROG to stop")
            return

        if self.tab_spectrometer.thread_stage.isRunning():
            if not self.tab_spectrometer.event_stop_stage.is_set():
                self.tab_spectrometer.event_stop_stage.set()
            else:
                self.ui.tb_frog_error.setPlainText("wait for stage to stop")
            return

        if self.tab_spectrometer.thread_spec.isRunning():
            if not self.tab_spectrometer.event_stop_spec.is_set():
                self.tab_spectrometer.thread_spec.quit()
                self.tab_spectrometer.thread_spec.wait()

        self.worker_frog._x_encoder_step = self._x_encoder_step
        self.worker_frog.N_steps = self._N_steps
        self.worker_frog.T0_um = self.T0_um

        self._view_box.setRange(
            xRange=[self.frog_start_fs, self.frog_end_fs],
            yRange=[self.spectrometer.wl[0], self.spectrometer.wl[-1]],
        )

        self._t_array = np.zeros(self._N_steps)
        self._s_array = np.zeros([self._N_steps, self.spectrometer.wl.size])

        self.tab_spectrometer.slot_pb_absolute_move(
            target_pos_encoder=self._x_encoder_start
        )
        self.start_frog_event.set()

    def start_frog(self):
        if not self.start_frog_event.is_set():
            return

        self.start_frog_event.clear()
        self.thread_frog.start()

    def slot_frog_update(self, step, pos_um, t_array, s_array):
        self.ui.progbar_frog.setValue(
            int(np.round(step * 100 / self.worker_frog.N_steps))
        )
        self.tab_spectrometer.curve_spectrum.setData(self.spectrometer.wl, s_array[-1])

        t_fs = t_array[-1]
        self.ui.lcd_current_pos_um.display(np.round(pos_um, 3))
        self.ui.lcd_current_pos_fs.display(t_fs)

        x = t_array
        y = self.spectrometer.wl
        if t_array.size > 1:
            scale = [
                (x[-1] - x[0]) / (x.size - 1),
                (y[-1] - y[0]) / (y.size - 1),
            ]
        else:
            scale = None

        view_range = self._view_box.viewRange()

        self.ui.gv_frog.setImage(
            s_array, pos=[t_array[0], self.spectrometer.wl[0]], scale=scale
        )
        self.ui.gv_frog.roi.setPos([t_array[0], self.spectrometer.wl[0]])
        self.ui.gv_frog.roi.setSize(
            [
                t_array[-1] - t_array[0],
                self.spectrometer.wl[-1] - self.spectrometer.wl[0],
            ]
        )

        self._view_box.setRange(
            xRange=view_range[0],  # Preserve the x-range
            yRange=view_range[1],  # Preserve the y-range
            padding=0,  # Optional: Adjust padding if needed
        )

        self._s_array[: step + 1] = s_array
        self._t_array[: step + 1] = t_array


class WorkerFrogStepScan(QtCore.QObject):
    progress = QtCore.pyqtSignal(int, float, np.ndarray, np.ndarray)
    finished = QtCore.pyqtSignal()

    def __init__(self, spectrometer, stage, stop_event, x_encoder_step, N_steps, T0_um):
        super().__init__()
        spectrometer: StellarnetBlueWave
        stage: ZaberStage
        stop_event: threading.Event

        self.spec = spectrometer
        self.stage = stage
        self.stop_event = stop_event

        self._x_encoder_step = x_encoder_step
        self.N_steps = N_steps

        self._s_array = np.zeros([N_steps, spectrometer.wl.size])
        self._t_array = np.zeros(N_steps)
        self._s = np.zeros(spectrometer.wl.size)

        self.T0_um = T0_um

    def loop(self):
        step = 0
        self.stage.open_port()
        try:
            while step < self.N_steps:
                if self.stop_event.is_set():
                    self.exit()
                    return

                self.stage.send_message(
                    self.stage._cmd_move_relative, self._x_encoder_step
                )
                cmd_num, msg = self.stage.receive_message()  # wait for step complete
                (x_encoder,) = struct.unpack("l", msg)
                x = x_encoder / self.stage._max_pos * self.stage._max_range
                x *= mm / um  # convert to um

                t_fs = np.round((2 * (x - self.T0_um) * um / c) / fs, 3)
                self._t_array[step] = t_fs
                self._s[:] = self.spec.spectrum
                self._s_array[step] = self._s[:]

                self.progress.emit(
                    step, x, self._t_array[: step + 1], self._s_array[: step + 1]
                )

                step += 1
        finally:
            self.exit()

    def exit(self):
        self.stage.close_port()
        self.stop_event.clear()
        self.finished.emit()
