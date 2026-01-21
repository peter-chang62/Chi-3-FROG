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

    def connect_push_bottons_signals_slots(self):
        self.ui.pb_load_frog.clicked.connect(self.slot_pb_load_frog)
        self.ui.pb_crop_frog.clicked.connect(self.slot_pb_crop_frog)

    def slot_pb_load_frog(self):
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

        filename_bckgnd = QtWidgets.QFileDialog.getOpenFileName(caption="load FROG")[0]
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

        # create interpolation object
        v_grid = c / self.data.wl_grid
        self.s_v_interp = RegularGridInterpolator(
            (t_grid, v_grid),
            s * c / v_grid**2,
            bounds_error=False,
            fill_value=0.0,
        )

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
            (x[-1] - x[0]) / (self.s.shape[0]),
            (y[-1] - y[0]) / (self.s.shape[1]),
        )
        self.im_exp.setTransform(self._transform_im_exp)
        self.im_exp.setImage(cmap(self.s / self.s.max()))

        # ----- plot marginals to gui -----------------------------------------
        self.curve_marginal_t.setData(self.t_grid * 1e15, self.marginal_t)
        self.curve_marginal_v.setData(self.v_grid * 1e-12, self.marginal_v)

        # ----- create linearRegionItems on marginals -------------------------
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

        t_lim = np.asarray(self.lr_t.getRegion()) * 1e-15
        v_lim = np.asarray(self.lr_v.getRegion()) * 1e12
        idx_t = np.logical_and(t_lim[0] < self.t_grid, self.t_grid < t_lim[-1])
        idx_v = np.logical_and(v_lim[0] < self.v_grid, self.v_grid < v_lim[-1])

        marginal_v_interp = InterpolatedUnivariateSpline(
            self.v_grid[idx_v][::-1], self.marginal_v[idx_v][::-1] - 0.01
        )
        roots_v = marginal_v_interp.roots()

        if len(roots_v) < 2:
            self.ui.tb_ret_error.setPlainText("frequency crop is too narrow")
            return

        roots_v = roots_v[[0, -1]]
        bandwidth_v = np.diff(roots_v) * factor_bandwidth_v
        v0 = (roots_v[-1] - roots_v[0]) / 2 + roots_v[0]
        bandwidth_t = self.t_grid[idx_t].max() - self.t_grid[idx_t].min()
        n_points = int(np.ceil(bandwidth_t * bandwidth_v)[0])

        if n_points == 0:
            self.ui.tb_ret_error.setPlainText("time crop is too narrow")
            return

        n_points = n_points if n_points % 2 == 0 else n_points + 1
        t_grid_new = np.linspace(-bandwidth_t / 2, bandwidth_t / 2, n_points)
        dt = t_grid_new[1] - t_grid_new[0]
        v_grid_new = fftshift(fftfreq(n_points, dt)) + v0
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
            (x[-1] - x[0]) / (self.s_v_new.shape[0]),
            (y[-1] - y[0]) / (self.s_v_new.shape[1]),
        )
        self.im_exp.setTransform(self._transform_im_exp)
        self.im_exp.setImage(cmap(self.s_v_new))

        self.ui.tb_ret_error.setPlainText("frog crop finished")
