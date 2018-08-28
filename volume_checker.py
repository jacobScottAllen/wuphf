import time

import numpy as numpy
import sounddevice as sd

from omf import OMF


class VolumeChecker:
    """[summary]
    """
    def __init__(self, omf: OMF, scaling_factor: float, threshold: float):
        """
        Arguments:
            omf {OMF} -- The omf messenger
            scaling_factor {float} -- The amount to scale the volume by
            threshold {float} -- The volume threshold to trigger at
        """
        self._last_volume_norm = 0
        self.omf = omf
        self.scaling_factor = scaling_factor
        self.threshold = threshold

    def check_volume(self, indata, frames, time, status):
        """Sends an OMF message if the volume threshold is exceeded
    
        Arguments:
            indata, frames, time, and status are passed in by the callback
        """
        volume_norm = np.linalg.norm(indata) * self.scaling_factor
        
        if (volume_norm >= self.threshold && _last_volume_norm < self.threshold):
            self.omf.insert_value(volume_norm)
            # TODO: Read from GPIO sensors  
        
        _last_volume_norm = volume_norm  

    def listen_forever(self):
        """Lets the callback listen indefinitely
        
        Arguments:
            omf {OMF} -- The omf instance passed into the callback
        """
        with sd.InputStream(callback=self.check_volume):
            # Just wait forever
            while True:
                time.sleep(1)