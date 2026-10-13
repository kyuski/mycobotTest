"""
smoke_test.py
-------------
Basic myCobot 280 M5Stack smoke test. Standalone: no framework, just
pymycobot. Connects, reads angles, flashes the LED, then moves the arm
to the upright pose.

Usage:
    python smoke_test.py            # uses PORT below
    python smoke_test.py COM7       # override port from the command line

Prerequisites:
    - pip install pymycobot
    - 12V barrel jack AND USB-C connected
    - M5Stack LCD showing "Transponder" mode
"""

import sys
import time

from pymycobot import MyCobot280

# Edit to match your arm's COM port (Device Manager > Ports)
PORT = "COM5"
BAUD = 115200


def main():
    port = sys.argv[1] if len(sys.argv) > 1 else PORT

    print(f"Connecting to {port} at {BAUD}...")
    mc = MyCobot280(port, BAUD)
    time.sleep(2)  # let the serial connection settle

    # 1. Read angles to confirm the arm is talking back
    angles = mc.get_angles()
    print(f"Current joint angles: {angles}")
    if not angles or all(a == -1 for a in angles):
        print("Arm not responding. Check Transponder mode and 12V power.")
        return

    # 2. LED check: red, then green
    mc.set_color(255, 0, 0)
    print("Atom LED: red")
    time.sleep(1)
    mc.set_color(0, 255, 0)
    print("Atom LED: green")
    time.sleep(1)

    # 3. Move to the upright pose at a moderate speed
    print("Moving to upright pose [0, 0, 150, 25, 0, 0] at speed 40...")
    mc.send_angles([0, 0, 150, 25, 0, 0], 40)
    time.sleep(5)
    print(f"Final angles: {mc.get_angles()}")


if __name__ == "__main__":
    main()
