from spectrometer_hardware.stellarnet_driverLibs import stellarnet_driver3 as sn


class StellarnetBlueWave:
    def __init__(self, *args, **kwargs):
        self.initialize()

        self._ext_trig = False

    def initialize(self):
        self._spectrometer, self._wl = sn.array_get_spec(0)
        self._wl = self._wl.flatten()

    def reset(self):
        self.spectrometer["device"].__del__()
        print("freed spectrometer")

    @property
    def spectrometer(self):
        return self._spectrometer

    @property
    def wl(self):
        return self._wl

    @property
    def integration_time(self):
        return self.spectrometer["device"].get_config()["int_time"]

    @integration_time.setter
    def integration_time(self, int_time):
        self.spectrometer["device"].set_config(int_time=int_time)

    @property
    def x_timing(self):
        return self.spectrometer["device"].get_config()["x_timing"]

    @x_timing.setter
    def x_timing(self, x_timing):
        self.spectrometer["device"].set_config(x_timing=x_timing)

    @property
    def spectrum(self):
        return self.spectrometer["device"].read_spectrum()

    @property
    def n_avg(self):
        return self.spectrometer["device"].get_config()["scans_to_avg"]

    @n_avg.setter
    def n_avg(self, n_avg):
        self.spectrometer["device"].set_config(scans_to_avg=n_avg)

    @property
    def x_smooth(self):
        return self.spectrometer["device"].get_config()["x_smooth"]

    @x_smooth.setter
    def x_smooth(self, x_smooth):
        self.spectrometer["device"].set_config(x_smooth=x_smooth)

    @property
    def ext_trig(self):
        return self._ext_trig

    @ext_trig.setter
    def ext_trig(self, ext_trig):
        sn.ext_trig(self.spectrometer, ext_trig)
        self._ext_trig = ext_trig


s = StellarnetBlueWave()
print(s.spectrometer["device"].get_config())
s.reset()
