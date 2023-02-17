import argparse
import itertools
from time import sleep

from belay import Device


class MyDevice(Device):
    def __pre_autoinit__(self):
        # Sync over the ``debouncedpin`` dependency
        self.sync(".belay/dependencies/main", "/lib")

    @Device.setup(autoinit=True)
    def setup():
        from debouncedpin import DebouncedLedPin
        from machine import Pin

        pin = DebouncedLedPin(2, Pin.PULL_UP)  # GPIO2

    @Device.task
    def pin(val=None) -> bool:
        return bool(pin(val))

    @Device.teardown
    def turn_off_led():
        pin.off()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="Micropython device port; e.g. /dev/ttyUSB0")
    args = parser.parse_args()

    device = MyDevice(args.port)

    for i in itertools.count(1):
        switch_state = device.pin()
        print(f"Switch State: {switch_state}")
        device.pin(i % 2)
        sleep(0.5)


if __name__ == "__main__":
    main()
