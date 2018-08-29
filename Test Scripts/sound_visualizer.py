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
        with sd.Stream(callback=self._print):
            sd.sleep(self.duration_sec * 1000)

    def _print(self, indata, *_):
        volume_norm = np.linalg.norm(indata) * self.scale
        self._values.append(volume_norm)
        print(self.symbol * int(volume_norm))


def _input_defaults(param_name: str, default_value, units: str = ""):
    prompt = "Enter your {0} (leave blank for {1}{2}): ".format(
        param_name, 
        default_value, 
        units
    )
    # Need to print separately due to remote terminal issue
    print(prompt)
    value_input = input()
    return value_input if value_input != '' else default_value


def main():
    scale = int(_input_defaults("scale", 10, "x"))
    duration = int(_input_defaults("duration", 10, " seconds"))
    symbol = _input_defaults("symbol", "|")

    sound_visualizer = SoundVisualizer(scale, duration, symbol) 
    sound_visualizer.visualize_print()

if __name__ == '__main__':
    main()
