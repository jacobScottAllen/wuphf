import asyncio
from functools import partial
import time

import numpy as numpy
import sounddevice as sd

from omf import OMF


DURATION_MS = 10 * 1000  # 10 seconds
SCALING_FACTOR = 10
THRESHOLD = 5


def volume_checker(indata, frames, time, status, omf: OMF):
    """Sends an OMF message if the volume threshold is exceeded
    
    Arguments:
        indata, frames, time, and status are passed in by the callback
        omf {OMF} -- The omf instance to pass the volume to
    """
    volume_norm = np.linalg.norm(indata) * SCALING_FACTOR

    if (volume_norm >= THRESHOLD):
        omf.insert_value(volume_norm)
        # TODO: Read from GPIO sensors    


def listen(omf: OMF):
    """Lets the callback listen indefinitely
    
    Arguments:
        omf {OMF} -- The omf instance passed into the callback
    """
    with sd.InputStream(callback=partial(volume_checker, omf=omf)):
        # Just wait forever
        while True:
            time.sleep(1)


def main():
    omf = OMF()

    while True:
        try:
            listen(omf)
        except Exception as ex:
            print(f"Listener crashed and will now restart. Error was: {ex}.")


if __name__ == "__main__":
    main()
