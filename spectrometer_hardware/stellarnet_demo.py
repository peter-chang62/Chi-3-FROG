# import the usb driver
from stellarnet_driverLibs import stellarnet_driver3 as sn

# import logging module
import logging

logging.basicConfig(format="%(asctime)s %(message)s")


# Function defination to get data
def getSpectrum(spectrometer, wav):
    logging.warning("requesting spectrum")
    spectrum = sn.array_spectrum(spectrometer, wav)
    logging.warning("recieved spectrum")
    return spectrum


# function defination to set parameter
def setParam(spectrometer, wav, inttime, scansavg, smooth, xtiming):
    logging.warning("Setting Parameters")
    spectrometer["device"].set_config(
        int_time=inttime, scans_to_avg=scansavg, x_smooth=smooth, x_timing=xtiming
    )


# Function defination to reset hardware by using """Destructor. Release device resources."""  Make sure call "spectrometer, wav = sn.array_get_spec(0)" to init spectrometer again
def reset(spectrometer):
    spectrometer["device"].__del__()


# Function Defination to Enable or Disable Ext Trigger by Passing True or False, If pass True than Timeout function will be disable, so user can also use this function as timeout enable/disbale
def external_trigger(spectrometer, trigger):
    sn.ext_trig(spectrometer, trigger)


# This resturn a Version number of compilation date of driver
version = sn.version()
print(version)

# init Spectrometer
spectrometer, wav = sn.array_get_spec(
    0
)  # 0 for first channel and 1 for second channel , up to 127 spectrometers

# Device parameters to set
inttime = 50
scansavg = 1
smooth = 0
xtiming = 3

# Get current device parameter
currentParam = spectrometer["device"].get_config()

# Call to Enable or Disable External Trigger by default is Disbale=False
external_trigger(spectrometer, False)

# Check to see any parameters change, id so call setParam
if (
    (currentParam["int_time"] != inttime)
    or (currentParam["scans_to_avg"] != scansavg)
    or (currentParam["x_smooth"] != smooth)
    or (currentParam["x_timing"] != xtiming)
):
    setParam(
        spectrometer, wav, inttime, scansavg, smooth, xtiming
    )  # Only call this function on first call to get spectrum  and when you change any parameters i.e inttime, scansavg, smooth, also call
    # getSpectrum twice after this call as first time the data may not be true for its inttime so we throw away that.
    for i in range(2):  # Call getSpectrum twice and discard first one!
        data = getSpectrum(spectrometer, wav)
else:
    data = getSpectrum(spectrometer, wav)  # if no parameters changes just get data once

# Print data/spect
print(data)
