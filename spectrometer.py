class StellarnetBlueWave:
    """
    Stellarnet Blue-wave spectrometer
    """

    def __init__(self, *args, **kwargs):
        global sn
        from spectrometer_hardware.stellarnet_driverLibs import stellarnet_driver3 as sn

        self.initialize()

        self._ext_trig = False

    def initialize(self):
        """
        fetch the spectrometer
        """

        self._spectrometer, self._wl = sn.array_get_spec(0)
        self._wl = self._wl.flatten()

    def reset(self):
        """
        free the spectrometer, make sure to call this before you close the
        program, terminating python does not free the spectrometer
        """

        self.spectrometer["device"].__del__()
        print("freed spectrometer")

    @property
    def spectrometer(self):
        """
        spectrometer instance created by initialize()
        """

        return self._spectrometer

    @property
    def wl(self):
        """
        wavelength axis created by initialize()
        """

        return self._wl

    @property
    def integration_time(self):
        """
        integration time in ms
        """

        return self.spectrometer["device"].get_config()["int_time"]

    @integration_time.setter
    def integration_time(self, int_time):
        """
        set the integration time (ms)
        """

        self.spectrometer["device"].set_config(int_time=int_time)

    @property
    def x_timing(self):
        """
        Digitization rate, I'm not actually too sure what the units are, but I
        think it's ms
        """

        return self.spectrometer["device"].get_config()["x_timing"]

    @x_timing.setter
    def x_timing(self, x_timing):
        """
        set the digitization rate
        """

        self.spectrometer["device"].set_config(x_timing=x_timing)

    @property
    def spectrum(self):
        """
        retrieve the spectrum
        """

        return self.spectrometer["device"].read_spectrum()

    @property
    def n_avg(self):
        """
        number of scans to average
        """

        return self.spectrometer["device"].get_config()["scans_to_avg"]

    @n_avg.setter
    def n_avg(self, n_avg):
        """
        set the number of scans to average
        """

        self.spectrometer["device"].set_config(scans_to_avg=n_avg)

    @property
    def x_smooth(self):
        """
        size of the boxcar smoothing window
        """

        return self.spectrometer["device"].get_config()["x_smooth"]

    @x_smooth.setter
    def x_smooth(self, x_smooth):
        """
        set the size of the boxcar smoothing window
        """

        self.spectrometer["device"].set_config(x_smooth=x_smooth)

    @property
    def ext_trig(self):
        """
        status of the external trigger
        """

        return self._ext_trig

    @ext_trig.setter
    def ext_trig(self, ext_trig):
        """
        set the status of the external trigger
        """

        sn.ext_trig(self.spectrometer, ext_trig)
        self._ext_trig = ext_trig


# %% ----- testing ------------------------------------------------------------
# s = StellarnetBlueWave()
# print(s.spectrometer["device"].get_config())
# s.reset()
