"""
get_angles.py
-------------
Read and print the current joint angles of a myCobot 280 M5Stack.

Usage:
    python get_angles.py            # uses PORT below
    python get_angles.py COM7       # override port from the command line

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

    angles = mc.get_angles()

    # None, an empty list, or all -1 means the arm isn't answering,
    # usually because the M5Stack isn't in Transponder mode.
    if not angles or all(a == -1 for a in angles):
        print(f"Got {angles}: arm not responding.")
        print("Check that the M5Stack LCD shows 'Transponder' and that the")
        print("12V power is connected.")
        return

    print("\nCurrent joint angles (degrees):")
    for i, a in enumerate(angles, start=1):
        print(f"  Joint {i}: {a:>8.2f}")
    print(f"\nAs a list: {angles}")


if __name__ == "__main__":
    main()
