import time

import numpy as np
import sounddevice as sd

from omf import OMF


class VolumeChecker:
    """Class for reporting loud volumes
    """
    def __init__(self, 
                 omf: OMF, 
                 scaling_factor: float, 
                 threshold: float,
                 callback = None, 
                 sleep_sec = 1):
        """
        Arguments:
            omf {OMF} -- The omf messenger
            scaling_factor {float} -- The amount to scale the volume by
            sleep_sec {int} -- How many seconds to sleep after sending a message
        
        Keyword Arguments:
            callback {Func} -- function to call when level is surpassed
            threshold {float} -- The volume threshold to trigger at
        """
        self._last_volume_norm = 0
        self.omf = omf
        self.scaling_factor = scaling_factor
        self.callback = callback
        self.threshold = threshold

    def check_volume(self, indata, *_):
        """Sends an OMF message if the volume threshold is exceeded
    
        Arguments:
            indata {numpy.matrix} -- the volume data
            *_ are params passed in by the callback but never used
        """
        volume_norm = np.linalg.norm(indata) * self.scaling_factor
        
        if (volume_norm >= self.threshold and self._last_volume_norm < self.threshold):
            self.omf.insert_value(volume_norm)
            if (self.callback is not None):
                self.callback()
        
        self._last_volume_norm = volume_norm

    def listen_forever(self):
        """Lets the callback listen indefinitely
        """
        with sd.InputStream(callback=self.check_volume):
            # Just wait forever
            while True:
                time.sleep(1)
