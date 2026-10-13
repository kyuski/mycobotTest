# myCobot 280 M5Stack: Setup Guide

Quick setup for connecting a myCobot 280 M5Stack to a Windows PC and running
the two standalone scripts:

| File | What it does |
|---|---|
| `get_angles.py` | Prints the current angle of each joint |
| `smoke_test.py` | Reads angles, flashes the LED red then green, moves the arm to the upright pose |

---

## 1. What you need

- myCobot 280 M5Stack arm
- 12V power adapter (barrel jack) **and** the USB-C cable. USB alone will not move the arm.
- Windows PC
- Python 3.9 or newer (check with `python --version`)

---

## 2. Install Python package

Open Command Prompt or PowerShell:

```
pip install pymycobot
```

Check the install:

```
python -c "import pymycobot; print(pymycobot.__version__)"
```

---

## 3. Connect the arm

1. Place the arm on a flat surface with room around it. Clamp the base down if you can.
2. Plug the **12V adapter** into the arm's base and a wall outlet.
3. Plug the **USB-C cable** into the M5Stack (the screen on the side of the base) and into your PC.
4. Power on the arm (switch on the base).

### Set Transponder mode (required)

The arm only responds to Python commands when the M5Stack screen is in
**Transponder** mode.

1. On the M5Stack screen, use the buttons to open the mode menu.
2. Select **Transponder** (the screen should show it as active).

If you skip this, `get_angles.py` will print `-1` values or "not responding".

---

## 4. Find the COM port

1. Open **Device Manager** (right-click the Start button, then Device Manager).
2. Expand **Ports (COM & LPT)**.
3. Note the port for the arm, for example `COM5`. Unplug and replug the USB cable to see which entry appears and disappears.

**If no new COM port appears**, Windows needs a USB-serial driver. Check the
entry under *Other devices* or *Universal Serial Bus devices*, then install the
matching driver, depending on which chip your unit uses:

- CP210x driver (Silicon Labs)
- CH340 / CH9102 driver (WCH)

Reboot if prompted, then check Device Manager again. Use a data-capable USB
cable. Some charge-only cables will not show a port.

---

## 5. Run the scripts

Edit the `PORT = "COM5"` line at the top of each script, or pass the port on
the command line.

### Read current angles

```
python get_angles.py
python get_angles.py COM7
```

Expected output:

```
Current joint angles (degrees):
  Joint 1:     0.35
  Joint 2:     0.17
  ...
As a list: [0.35, 0.17, 149.5, 24.43, 0.26, 0.43]
```

### Smoke test (moves the arm)

**Clear the area around the arm first.** It moves to the upright pose
`[0, 0, 150, 25, 0, 0]`.

```
python smoke_test.py
python smoke_test.py COM7
```

What you should see:

1. Current angles printed
2. Atom LED turns red, then green
3. Arm moves upright (speed 40) and the final angles print

Close any other program using the COM port (the ROAM GUI, Arduino IDE, etc.)
before running either script. Only one program can open the port at a time.

---

## 6. Using it in your own scripts

```python
from pymycobot import MyCobot280

mc = MyCobot280("COM5", 115200)

print(mc.get_angles())                       # read joint angles
mc.set_color(0, 255, 0)                      # LED color (R, G, B)
mc.send_angles([0, 0, 150, 25, 0, 0], 40)    # move all joints, speed 1-100
mc.send_angle(1, 30, 30)                     # move one joint (joint, angle, speed)
```

Joint angle limits are about -165 to +165 degrees. Joint 1 and joint 2 differ
slightly, so check the pymycobot docs before sending extreme values.

---

## 7. Troubleshooting

| Symptom | Fix |
|---|---|
| `get_angles` prints `-1` or `None` | Put the M5Stack in **Transponder** mode; check 12V power |
| `could not open port` / `Access is denied` | Another program holds the port; close it, or unplug and replug USB |
| COM port not in Device Manager | Install the USB-serial driver (step 4); try another USB cable or port |
| LED works but arm will not move | Confirm the 12V adapter is plugged in; try `mc.power_on()` before `send_angles`; run `mc.is_power_on()` to check |
| Arm moves to a slightly different pose than requested | Normal servo tolerance (about 0.5 degrees); allow more settle time after the move |
| Still unresponsive after all of the above | Re-flash the Atom / Transponder firmware using Elephant Robotics' firmware tool |

Official docs: https://docs.elephantrobotics.com
