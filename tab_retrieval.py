# %% ----- imports
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, ifft, fftshift, ifftshift, fftfreq
from scipy.constants import c
from collections import namedtuple
from scipy.interpolate import InterpolatedUnivariateSpline, RegularGridInterpolator
import scipy
from phase_retrieval import blit
from phase_retrieval.BBO import BBOSHG as BBO
from PyQt5 import QtCore, QtGui, QtWidgets
import copy
import pyqtgraph as pg
from PyQt5.QtGui import QTransform
import threading

output = namedtuple("frog_data", ["t_grid", "wl_grid", "s"])

level_of_marginal_t = 1 / np.exp(1)
factor_bandwidth_v = 1.25

cmap = plt.get_cmap("RdBu_r")


def forward_transform(x, dx=1.0, axis=0):
    return fftshift(fft(ifftshift(x, axes=axis), axis=axis), axes=axis) * dx


def inverse_transform(x, dx=1.0, axis=0):
    return fftshift(ifft(ifftshift(x, axes=axis), axis=axis), axes=axis) / dx


def shg_frog(a_t, dt=1.0):
    o = a_t * np.c_[a_t]
    o_rs = np.zeros_like(o)
    for r in range(o.shape[0]):
        o_rs[r] = np.roll(o[r], -r)
    s_t = fftshift(o_rs, axes=1)
    s_v = forward_transform(s_t, dx=dt, axis=0)
    return s_v


def load_file(file):
    data = np.load(file)
    return output(data["t_grid"] * 1e-15, data["wl_grid"] * 1e-9, data["spectrogram"])


def shift(array, dx):
    ft = forward_transform(array)
    freq = fftshift(fftfreq(array.size))
    omega = 2 * np.pi * freq
    ft *= np.exp(1j * omega * dx)
    return inverse_transform(ft)


def soft_threshold(x, gamma):
    return np.where(x < gamma, 0, x - gamma * np.sign(x))


def create_curve(color="b", width=2, x=None, y=None):
    curve = pg.PlotDataItem(pen=pg.mkPen(color=color, width=width))
    if (x is not None) and (y is not None):
        curve.setData(x, y)
    return curve


class RetrievalTab:
    def __init__(self, ui):
        self.ui = ui

        self.data = None
        self.bckgnd = None

        self.s = None
        self.t_grid = None
        self.v_grid = None
        self.marginal_t = None
        self.marginal_v = None

        self.s_v_new = None
        self.v_grid_new = None
        self.t_grid_new = None

        self.lr_t = None
        self.lr_v = None

        self.im_exp = pg.ImageItem()
        self._transform_im_exp = QTransform()
        self._plot_item_exp = self.ui.gv_ret_exp.addPlot()
        self._plot_item_exp.addItem(self.im_exp)

        self.im_recon = pg.ImageItem()
        self._transform_im_recon = QTransform()
        self._plot_item_recon = self.ui.gv_ret_recon.addPlot()
        self._plot_item_recon.addItem(self.im_recon)

        self.curve_marginal_t = create_curve("w")
        self.ui.gv_ret_marginal_t.addItem(self.curve_marginal_t)

        self.curve_marginal_v = create_curve("w")
        self.ui.gv_ret_marginal_v.addItem(self.curve_marginal_v)

        self.connect_push_bottons_signals_slots()
        self.connect_radio_button_signals_slot()
        self.set_validators()

        pi_marginal_v = self.ui.gv_ret_marginal_v.plotItem
        self.vb_marginal_v = pg.ViewBox()
        self.vb_marginal_v.setXLink(pi_marginal_v)
        pi_marginal_v.showAxis("right")
        pi_marginal_v.getAxis("right").linkToView(self.vb_marginal_v)
        pi_marginal_v.scene().addItem(self.vb_marginal_v)
        # pi_marginal_v.getAxis("right").setLabel("phi")
        self.vb_marginal_v.setYRange(-360 * 2, 360 * 2)

        def updateViews_gv_ret_marginal_v():
            self.vb_marginal_v.setGeometry(pi_marginal_v.vb.sceneBoundingRect())
            self.vb_marginal_v.linkedViewChanged(
                pi_marginal_v.vb, self.vb_marginal_v.XAxis
            )

        pi_marginal_v.vb.sigResized.connect(updateViews_gv_ret_marginal_v)

        self.curve_p_t = create_curve("b")
        self.curve_p_v = create_curve("b")
        self.curve_phi_v = create_curve("r")

        self.rb_focus_on_marginals = True

        self.thread_retrieval = QtCore.QThread()
        self.worker_retrieval = None

    def connect_push_bottons_signals_slots(self):
        self.ui.pb_load_frog.clicked.connect(self.slot_pb_load_frog)
        self.ui.pb_crop_frog.clicked.connect(self.slot_pb_crop_frog)
        self.ui.pb_start_ret.clicked.connect(self.slot_pb_start_retrieval)
        self.ui.pb_stop_ret.clicked.connect(self.slot_pb_stop_ret)
        self.ui.pb_save_ret.clicked.connect(self.slot_pb_save_retrieval)

    def connect_radio_button_signals_slot(self):
        self.ui.rb_marginals.toggled.connect(self.slot_rb_marginals)

    def set_validators(self):
        self.ui.le_niter.setValidator(QtGui.QIntValidator())

    def create_threads_workers(self):
        self.stop_retrieval_event = threading.Event()
        self.worker_retrieval = WorkerRetrieval(
            self.s_v_new, self.t_grid_new, None, self.stop_retrieval_event
        )
        self.worker_retrieval.moveToThread(self.thread_retrieval)
        self.thread_retrieval.started.connect(self.worker_retrieval.loop)
        self.worker_retrieval.progress_fields.connect(self.slot_retrieval_update)
        self.worker_retrieval.progress_iter.connect(self.slot_progbar_iter_update)
        self.worker_retrieval.progress_windows.connect(self.slot_progbar_windows_update)
        self.worker_retrieval.retrieval_completed.connect(self.slot_retrieval_completed)
        self.worker_retrieval.finished.connect(self.thread_retrieval.quit)
        self.worker_retrieval.finished.connect(self.slot_worker_retrieval_finished)

    def slot_worker_retrieval_finished(self):
        pass

    def slot_pb_stop_ret(self):
        if self.thread_retrieval.isRunning():
            self.stop_retrieval_event.set()

    def slot_rb_marginals(self):
        if self.ui.rb_marginals.isChecked():
            if not self.rb_focus_on_marginals:
                self.ui.gv_ret_marginal_t.addItem(self.curve_marginal_t)
                self.ui.gv_ret_marginal_v.addItem(self.curve_marginal_v)
                if self.lr_t is not None:
                    self.ui.gv_ret_marginal_t.addItem(self.lr_t)
                    self.ui.gv_ret_marginal_v.addItem(self.lr_v)

                self.ui.gv_ret_marginal_t.removeItem(self.curve_p_t)
                self.ui.gv_ret_marginal_v.removeItem(self.curve_p_v)
                self.vb_marginal_v.removeItem(self.curve_phi_v)

                self.rb_focus_on_marginals = True
        else:
            if self.rb_focus_on_marginals:
                self.ui.gv_ret_marginal_t.removeItem(self.curve_marginal_t)
                self.ui.gv_ret_marginal_v.removeItem(self.curve_marginal_v)
                if self.lr_t is not None:
                    self.ui.gv_ret_marginal_t.removeItem(self.lr_t)
                    self.ui.gv_ret_marginal_v.removeItem(self.lr_v)

                self.ui.gv_ret_marginal_t.addItem(self.curve_p_t)
                self.ui.gv_ret_marginal_v.addItem(self.curve_p_v)
                self.vb_marginal_v.addItem(self.curve_phi_v)

                self.rb_focus_on_marginals = False

    def slot_pb_load_frog(self):
        if self.thread_retrieval.isRunning():
            self.ui.tb_ret_error.setPlainText("stop retrieval first")
            return

        filename_frog = QtWidgets.QFileDialog.getOpenFileName(caption="load FROG")[0]
        if filename_frog == "":
            return
        else:
            try:
                data = load_file(filename_frog)
            except Exception:
                self.ui.tb_ret_error.setPlainText(
                    "file is not frog data, or file is incorrect format"
                )
                return

        filename_bckgnd = QtWidgets.QFileDialog.getOpenFileName(
            caption="load background"
        )[0]
        if filename_bckgnd == "":
            return
        else:
            try:
                bckgnd = load_file(filename_bckgnd)
            except Exception:
                self.ui.tb_ret_error.setPlainText(
                    "file is not frog data, or file is incorrect format"
                )
                return

        self.data = data
        self.bckgnd = bckgnd

        self.subtract_bckgnd_and_center_frog()

    def subtract_bckgnd_and_center_frog(self):
        if self.data is None:
            self.ui.tb_ret_error.setPlainText("no frog data loaded yet")
            return
        if self.bckgnd is None:
            self.ui.tb_ret_error.setPlainText("no frog data loaded yet")
            return

        s = self.data.s - self.bckgnd.s * 1.01
        s = np.where(s < 0, 0, s)

        # center frog trace in time
        marginal_t = np.sum(s, axis=1)
        idx = marginal_t.argmax()
        n = min([idx, self.data.t_grid.size - idx]) * 2
        n = n if n % 2 == 0 else n - 1
        s = s[idx - n // 2 : idx + n // 2]
        t_grid = self.data.t_grid - self.data.t_grid[idx]
        t_grid = t_grid[idx - n // 2 : idx + n // 2]
        v_grid = c / self.data.wl_grid

        self.s = s
        self.t_grid = t_grid
        self.v_grid = v_grid
        self.marginal_t = np.sum(s, axis=1)
        self.marginal_t /= self.marginal_t.max()
        self.marginal_v = np.sum(s, axis=0)
        self.marginal_v /= self.marginal_v.max()

        # ----- plot FROG to gui ----------------------------------------------
        self._transform_im_exp = QTransform()
        x, y = self.t_grid * 1e15, self.data.wl_grid * 1e9
        self._transform_im_exp.translate(x[0], y[0])
        self._transform_im_exp.scale(
            (x[-1] - x[0]) / (self.s.shape[0] - 1),
            (y[-1] - y[0]) / (self.s.shape[1] - 1),
        )
        self.im_exp.setTransform(self._transform_im_exp)
        self.im_exp.setImage(cmap(self.s / self.s.max()))

        # ----- plot marginals to gui -----------------------------------------
        self.curve_marginal_t.setData(self.t_grid * 1e15, self.marginal_t)
        self.curve_marginal_v.setData(self.v_grid * 1e-12, self.marginal_v)

        # ----- create linearRegionItems on marginals -------------------------
        if not self.ui.rb_marginals.isChecked():
            self.ui.rb_marginals.setChecked(True)  # automatically toggles the other
            self.slot_rb_marginals()

        if self.lr_t is not None:
            self.ui.gv_ret_marginal_t.removeItem(self.lr_t)
            self.ui.gv_ret_marginal_v.removeItem(self.lr_v)

        self.lr_t = pg.LinearRegionItem(
            [self.t_grid[0] * 1e15, self.t_grid[-1] * 1e15],
            bounds=[self.t_grid[0] * 1e15, self.t_grid[-1] * 1e15],
        )
        self.lr_v = pg.LinearRegionItem(
            [self.v_grid.min() * 1e-12, self.v_grid.max() * 1e-12],
            bounds=[self.v_grid.min() * 1e-12, self.v_grid.max() * 1e-12],
        )
        self.ui.gv_ret_marginal_t.addItem(self.lr_t)
        self.ui.gv_ret_marginal_v.addItem(self.lr_v)

        def even_limits():
            l, r = self.lr_t.getRegion()
            t_lim = self.t_grid[0] * 1e15, self.t_grid[-1] * 1e15

            span = abs(r - l)
            start = max([t_lim[0], -span / 2])
            end = min([t_lim[1], span / 2])
            self.lr_t.setRegion([start, end])

        self.lr_t.sigRegionChanged.connect(even_limits)

    def slot_pb_crop_frog(self):
        if self.s is None:
            self.ui.tb_ret_error.setPlainText("no frog data loaded yet")
            return

        if self.thread_retrieval.isRunning():
            self.ui.tb_ret_error.setPlainText("stop retrieval first")
            return

        # filter the frog in freuqency based on user set retion
        # crop to the 20dB bandwidth of the filtered frog
        v_lim = np.asarray(self.lr_v.getRegion()) * 1e12
        idx_v = np.logical_and(v_lim[0] < self.v_grid, self.v_grid < v_lim[-1])
        s = self.s.copy()
        s[:, ~idx_v] = 0
        marginal_v = np.sum(s, axis=0)
        marginal_v /= marginal_v.max()
        marginal_v_interp = InterpolatedUnivariateSpline(
            self.v_grid[::-1], marginal_v[::-1] - 0.01
        )
        roots_v = marginal_v_interp.roots()

        if len(roots_v) < 2:
            self.ui.tb_ret_error.setPlainText("frequency crop is too narrow")
            return

        roots_v = roots_v[[0, -1]]
        bandwidth_v = np.diff(roots_v) * factor_bandwidth_v
        v0 = (roots_v[-1] - roots_v[0]) / 2 + roots_v[0]

        # set the retrieval time window and crop the frog to this time window
        t_lim = np.asarray(self.lr_t.getRegion()) * 1e-15
        idx_t = np.logical_and(t_lim[0] < self.t_grid, self.t_grid < t_lim[-1])
        bandwidth_t = self.t_grid[idx_t].max() - self.t_grid[idx_t].min()
        n_points = int(np.ceil(bandwidth_t * bandwidth_v)[0])

        if n_points == 0:
            self.ui.tb_ret_error.setPlainText("time crop is too narrow")
            return

        # final retrieval grid
        n_points = n_points if n_points % 2 == 0 else n_points + 1
        t_grid_new = np.linspace(-bandwidth_t / 2, bandwidth_t / 2, n_points)
        dt = t_grid_new[1] - t_grid_new[0]
        v_grid_new = fftshift(fftfreq(n_points, dt)) + v0

        # create interpolation object and interpolate experimental frog onto
        # the retrieval grid
        self.s_v_interp = RegularGridInterpolator(
            (self.t_grid, self.v_grid),
            s * c / self.v_grid**2,
            bounds_error=False,
            fill_value=0.0,
        )
        T_grid_new, V_grid_new = np.meshgrid(t_grid_new, v_grid_new, indexing="ij")
        s_v_new = self.s_v_interp((T_grid_new, V_grid_new))
        s_v_new /= s_v_new.max()

        # ----- divide by phasematching ---------------------------------------
        bbo = BBO()
        R = bbo.R(
            wl_um=c / v_grid_new * 1e6,
            length_um=50,
            theta_pm_rad=bbo.phase_match_angle_rad(1.55),
            alpha_rad=np.arctan(
                0.25 / 6.0,
            ),
        )
        s_v_new /= R
        s_v_new /= s_v_new.max()

        self.s_v_new = s_v_new
        self.v_grid_new = v_grid_new
        self.t_grid_new = t_grid_new

        # ----- plot FROG to gui ----------------------------------------------
        self._transform_im_exp = QTransform()
        x, y = self.t_grid_new * 1e15, self.v_grid_new * 1e-12
        self._transform_im_exp.translate(x[0], y[0])
        self._transform_im_exp.scale(
            (x[-1] - x[0]) / (self.s_v_new.shape[0] - 1),
            (y[-1] - y[0]) / (self.s_v_new.shape[1] - 1),
        )
        self.im_exp.setTransform(self._transform_im_exp)
        self.im_exp.setImage(cmap(self.s_v_new))

        self.ui.tb_ret_error.setPlainText("frog crop finished")

        self.create_threads_workers()

    def slot_pb_start_retrieval(self):
        if self.s_v_new is None:
            self.ui.tb_ret_error.setPlainText("no frog has been loaded and cropped yet")
            return

        if self.thread_retrieval.isRunning():
            self.ui.tb_ret_error.setPlainText("stop retrieval first")
            return

        # ----- retrieval -----------------------------------------------------
        string = self.ui.le_niter.text()
        if string == "":
            self.ui.tb_ret_error.setPlainText("set number of iterations")
            return
        self.N_iter = int(self.ui.le_niter.text())
        if self.N_iter < 2:
            self.ui.tb_ret_error.setPlainText("number of must be >= 2")
            return
        self.plot_initialized = False
        self.worker_retrieval.re_init_values(
            self.s_v_new, self.t_grid_new, self.N_iter, self.stop_retrieval_event
        )

        if self.ui.rb_marginals.isChecked():
            self.ui.rb_retrieval.setChecked(True)  # automatically toggles the other
            self.slot_rb_marginals()

        self.ui.progbar_iter.setValue(0)
        self.ui.progbar_windows.setValue(0)
        self.thread_retrieval.start()

    def slot_retrieval_update(self, s_v_recon, p_t, p_v, phi):
        n_points = s_v_recon.shape[0]
        if not self.plot_initialized:
            self._transform_im_recon = QTransform()
            x, y = self.t_grid_new * 1e15, self.v_grid_new * 1e-12
            self._transform_im_recon.translate(x[0], y[0])
            self._transform_im_recon.scale(
                (x[-1] - x[0]) / (n_points - 1),
                (y[-1] - y[0]) / (n_points - 1),
            )
            self.im_recon.setTransform(self._transform_im_recon)
            self.plot_initialized = True

        self.im_recon.setImage(cmap(s_v_recon))
        self.curve_p_t.setData(self.t_grid_new * 1e15, p_t)
        self.curve_p_v.setData(self.v_grid_new * 1e-12, p_v)
        self.curve_phi_v.setData(self.v_grid_new * 1e-12, phi)

    def slot_progbar_iter_update(self, n):
        self.ui.progbar_iter.setValue(n)

    def slot_progbar_windows_update(self, n):
        self.ui.progbar_windows.setValue(n)

    def slot_retrieval_completed(self, p_t):
        roots = InterpolatedUnivariateSpline(
            self.t_grid_new, p_t / p_t.max() - 0.5
        ).roots()
        if len(roots < 2):
            return
        t_width = np.diff(roots[[0, -1]]) * 1e15
        self.ui.tb_ret_error.setPlainText(f"FWHM = {np.round(t_width, 3)} fs")

    def slot_pb_save_retrieval(self):
        if self.thread_retrieval.isRunning():
            self.ui.tb_ret_error.setPlainText("stop retrieval first")
            return

        if self.worker_retrieval is None:
            self.ui.tb_ret_error.setPlainText("no retrieval has been run")
            return

        if self.worker_retrieval.a_v is None:
            self.ui.tb_ret_error.setPlainText("no retrieval has been run")
            return

        filename = QtWidgets.QFileDialog.getSaveFileName(caption="save FROG")[0]
        if filename == "":
            return

        if filename[-4:].lower() != ".npz":
            filename += ".npz"

        np.savez(
            filename,
            t_grid=self.t_grid_new,
            v_grid=self.v_grid_new,
            a_t=self.worker_retrieval.E_i_best,
            a_v=self.worker_retrieval.a_v,
        )
        self.ui.tb_ret_error.setPlainText("finished saving")


class WorkerRetrieval(QtCore.QObject):
    progress_fields = QtCore.pyqtSignal(np.ndarray, np.ndarray, np.ndarray, np.ndarray)
    progress_iter = QtCore.pyqtSignal(int)
    progress_windows = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal()
    retrieval_completed = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, s_v_new, t_grid_new, N_iter, stop_event):
        super().__init__()
        self.re_init_values(s_v_new, t_grid_new, N_iter, stop_event)

    def re_init_values(self, s_v_new, t_grid_new, N_iter, stop_event):
        self.s_v_new = s_v_new
        self.t_grid_new = t_grid_new
        self.N_iter = N_iter
        self.stop_event = stop_event

        self.E_i_best = None
        self.a_v = None

    def loop(self):
        # ----- time windows --------------------------------------------------
        marginal_t = np.sum(self.s_v_new, axis=1)
        marginal_t /= marginal_t.max()
        marginal_t_interp = InterpolatedUnivariateSpline(
            self.t_grid_new, marginal_t - level_of_marginal_t
        )
        roots_t = marginal_t_interp.roots()

        idx_0 = abs(self.t_grid_new - roots_t[0]).argmin()
        idx_1 = abs(self.t_grid_new - roots_t[-1]).argmin()
        idx_width = idx_1 - idx_0
        idx_width = idx_width if idx_width % 2 == 0 else idx_width + 1

        n_points = self.s_v_new.shape[0]
        center = n_points // 2
        N_windows = int(np.ceil(n_points / idx_width))
        idx_subset_list = []
        idx_full = np.arange(n_points)
        for i in range(1, N_windows + 1):
            start = center - i * idx_width // 2
            start = 0 if start < 0 else start

            end = center + i * idx_width // 2
            end = n_points if end > n_points else end

            subset = idx_full[start:end]
            idx_subset_list.append(subset)

        # ----- initial guess -------------------------------------------------
        E_i = scipy.signal.windows.gaussian(n_points, idx_width).astype(complex)
        self.E_i_best = np.zeros_like(E_i)

        # ----- retrieval -----------------------------------------------------
        N_iter = self.N_iter
        dt = self.t_grid_new[1] - self.t_grid_new[0]
        s_v_new = self.s_v_new
        for n, idx_subset in enumerate(idx_subset_list):
            for i in range(N_iter):
                idx_subset_scrambled = np.random.permutation(idx_subset)
                alpha = np.random.uniform(low=0.1, high=0.5)

                for k in idx_subset_scrambled:
                    if self.stop_event.is_set():
                        self.exit()
                        return

                    delay = k - center

                    E_i_k = shift(E_i, delay)
                    Psi_i_k = E_i * E_i_k
                    Phi_i_k = forward_transform(Psi_i_k, dx=dt)
                    phase = np.unwrap(np.angle(Phi_i_k))
                    Phi_i_k_new = np.sqrt(s_v_new[k]) * np.exp(1j * phase)

                    # snr soft thresholding...

                    Psi_i_k_new = inverse_transform(Phi_i_k_new, dx=dt)

                    factor = Psi_i_k_new - Psi_i_k
                    obj_update = np.conj(E_i_k) / (abs(E_i_k) ** 2).max() * factor
                    probe_update = np.conj(E_i) / (abs(E_i) ** 2).max() * factor
                    probe_update = shift(probe_update, -delay)

                    E_i += alpha * (obj_update + probe_update)
                    E_i = np.roll(E_i, center - (abs(E_i) ** 2).argmax())

                # error calculation
                s_v_k = (abs(shg_frog(E_i, dt)) ** 2).T

                # calculate error based on the subset of the spectrogram being
                # retrieved
                num = np.sqrt(np.mean((s_v_k[idx_subset] - s_v_new[idx_subset]) ** 2))
                denom = np.sqrt(np.mean(s_v_new[idx_subset] ** 2))
                error = num / denom

                if i == 0:
                    # initialize
                    error_best = error
                    self.E_i_best[:] = E_i[:]

                else:
                    if error < error_best:
                        self.E_i_best[:] = E_i[:]
                        error_best = error

                        s_v_recon = (abs(shg_frog(self.E_i_best, dt)) ** 2).T
                        p_t = abs(self.E_i_best) ** 2
                        self.a_v = forward_transform(self.E_i_best, dt)
                        p_v = abs(self.a_v) ** 2
                        phi = np.unwrap(np.angle(self.a_v))
                        phi -= phi[n_points // 2]
                        phi *= 180 / np.pi

                        self.progress_fields.emit(s_v_recon, p_t, p_v, phi)

                self.progress_iter.emit(int(np.round((i + 1) * 100 / N_iter)))
            self.progress_windows.emit(
                int(np.round((n + 1) * 100 / len(idx_subset_list)))
            )

        self.exit()
        self.retrieval_completed.emit(p_t)

    def exit(self):
        self.finished.emit()
        self.stop_event.clear()
