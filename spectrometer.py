from spectrometer_hardware.stellarnet_driverLibs import stellarnet_driver3 as sn


class StellarnetBlueWave:
    def __init__(self, *args, **kwargs):
        self.spectrometer, self.wl = sn.array_get_spec(0)
        self.wl = self.wl.flatten()
