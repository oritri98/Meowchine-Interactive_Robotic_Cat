# Keyboard control for scan-bot's 3 servos over USB Serial.
# Install first:  pip install pyserial keyboard
# NOTE: close PlatformIO's Serial Monitor before running this --
# only one program can hold the COM port open at a time.

import serial
import keyboard
import time

SERIAL_PORT = "COM10"  # <-- change to your ESP32's actual port
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # give the ESP32 a moment -- opening the port resets it

print("Keyboard control ready. Keys:")
print("  1 / 2  -> head left / right")
print("  3 / 4  -> body left / right")
print("  5 / 6  -> paw left / right")
print("  0      -> center all three")
print("  p      -> photo pose (countdown + wink!)")
print("  w      -> wink")
print("  a      -> angry")
print("  l      -> love")
print("  z      -> dizzy")
print("  s      -> sad")
print("  n      -> sneaky")
print("  u      -> proud")
print("  e      -> excited (wiggle!)")
print("  r      -> resume auto sweep")
print("  ESC    -> quit")

KEYS = ["1", "2", "3", "4", "5", "6", "0", "p", "w", "a", "l", "z", "s", "n", "u", "e", "r"]


def on_key(event):
    if event.name in KEYS:
        ser.write(event.name.encode())
        print(f"Sent: {event.name}")


for k in KEYS:
    keyboard.on_press_key(k, on_key)

keyboard.wait("esc")
ser.close()
print("Closed.")