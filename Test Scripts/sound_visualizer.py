import numpy as np
import sounddevice as sd

duration = 10 * 1000 # 10 seconds

def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    print("|" * int(volume_norm))

with sd.Stream(callback=print_sound):
    sd.sleep(duration)
