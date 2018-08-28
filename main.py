from omf import OMF
from volume_checker import VolumeChecker


def main():
    omf = OMF()
    volume_checker = VolumeChecker(omf, scaling_factor=10, threshold=5)

    while True:
        try:
            volume_checker.listen_forever()
        except Exception as ex:
            print("Listener crashed and will now restart. Error was: " + {ex} + ".")


if __name__ == "__main__":
    main()
