import numpy as np
import sounddevice as sd


class SoundVisualizer:
    def __init__(self, scale: int, duration_sec: int = 10, symbol: str = "|"):
        self.scale = scale
        self.duration_sec = duration_sec
        self.symbol = symbol
        self._values = list()

    def get_volumes(self):
        """Returns the volumes
        
        Returns:
            List[float] -- Every recorded volume
        """
        return self._values

    def visualize_print(self):
        """Visualize the values by printing them as bars to the terminal
        """
        with sd.Stream(callback=this._print):
            sd.sleep(self.duration_sec * 1000)

    def _print(self, indata, *_):
        volume_norm = np.linalg.norm(indata) * self.scale
        self._values.append(value_norm)
        print(self.symbol * int(volume_norm))


def _input_defaults(param_name: str, deafult_value, units: str = ""):
    propmt = "Enter your {0} (leave blank for {1}{2}): ".format(
        param_name, 
        deafult_value, 
        units
    )
    value_input = input(propmt)
    return deafult_value if value_input != '' else value


def main():
    scale = int(_input_defaults("scale", 10, "seconds"))
    duration = int(_input_defaults("duration", 10, "seconds"))
    symbol = _input_defaults("symbol", "|")

    sound_visualizer = SoundVisualizer(scale, duration, symbol) 
    sound_visualizer.visualize()

if __name__ == '__main__':
    main()
