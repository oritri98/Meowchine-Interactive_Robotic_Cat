# Meowchine — Interactive Robotic Cat

An interactive, cat-personality desk robot built on an ESP32, combining expressive
animatronics, proximity-based reactions, and real-time joystick/keyboard control.

**Team:** Ismat Erena Siddiquee and Afif Bin Zaman 
**Codename:** Meowchine

> This project is being uploaded separately to both team members' GitHub accounts.
> Both authors contributed equally to the design, hardware assembly, and firmware/software
> development — team credit here applies in full regardless of which repository or commit
> history it appears under.

---

## Overview

Meowchine is a cat-like robot with a movable head, a rotating waist/body, and a
gesturing paw, built around an ESP32 microcontroller. It expresses "personality"
through a combination of an animated OLED face, short text messages on a 16x2 LCD,
and physical servo poses — reacting to proximity via an ultrasonic sensor, and
otherwise controllable directly by a person over USB (keyboard) or an Xbox 360
controller (joystick).

The robot can dip into several distinct expressions (happy, sad, angry, wink, love,
dizzy, sneaky, proud, excited, sleepy, curious, surprised), perform a short animated
wiggle, and run a multi-stage "photo pose" sequence (countdown → wink → hold) —
alongside continuous head/waist/paw control from a controller or keyboard.

---

## Feature status (v0.5)

| Feature | Status |
|---|---|
| Head pan (0–180°) | ✅ Working |
| Waist/body rotation (0–180°) | ✅ Working (mechanically limited — see Known Limitations) |
| Paw gesture servo | ✅ Working |
| OLED animated face (12 expressions incl. idle blink) | ✅ Working |
| LCD status/dialogue text | ✅ Working, on a separate I2C bus |
| Ultrasonic proximity sensing | ✅ Working — drives automatic "cat mood" reactions (idle → curious → happy → startled) with debounce and an idle "falls asleep" timer |
| Keyboard control (USB serial) | ✅ Working |
| Xbox 360 controller support | ✅ Working — sticks for head/waist, triggers for paw, buttons for presets/expressions |
| Photo pose sequence | ✅ Working |
| PIR motion sensor | 🔜 Planned — wiring defined, not yet integrated into firmware logic |
| LDR (ambient light) sensor | 🔜 Planned — wiring defined, not yet integrated into firmware logic |
| Autonomous mode (full sensor-driven behavior blending with manual override) | 🔜 Planned |
| High-five / paw-touch interaction | 🔜 Planned |
| WiFi/wireless control | ⏸️ Prototyped in an earlier revision (WebSocket-based), not in the current build — control is currently USB-serial based |

---

## Hardware

- ESP32 dev board (Espressif ESP32 Dev Module)
- 3× SG90 9g micro servos (head, waist/body, paw)
- HC-SR04 ultrasonic distance sensor
- SSD1306 128×64 I2C OLED display
- 16×2 character LCD with I2C (PCF8574) backpack
- PIR motion sensor (planned integration)
- LDR photoresistor (planned integration)
- 2× 3.7V Li-ion cells (series) + buck converter (regulated to 5V) for servo/peripheral power
- Bidirectional logic level shifter (for the 5V LCD on 3.3V-logic ESP32 pins)
- Foam board body/enclosure, hand-built with a stand base (no legs — v0.5 does not walk)

## Pin connections

| Component | ESP32 Pin | Notes |
|---|---|---|
| Head servo | GPIO 18 | External 5V supply, not the ESP32 pin |
| Waist/body servo | GPIO 25 | Same external 5V rail as above |
| Paw servo | GPIO 26 | Same external 5V rail as above |
| Ultrasonic TRIG | GPIO 5 | |
| Ultrasonic ECHO | GPIO 4 | Via voltage divider (5V → ~3.3V) |
| PIR OUT (planned) | GPIO 13 | |
| LDR (planned) | GPIO 34 | ADC1 — safe alongside WiFi if reintroduced later |
| OLED SDA / SCL | GPIO 21 / GPIO 22 | 3.3V logic, address `0x3C` |
| LCD SDA / SCL | GPIO 33 / GPIO 32 | Separate I2C bus, run through a level shifter to 5V logic, address `0x27` (or `0x3F`, verify with an I2C scanner) |

All grounds (ESP32, servo power supply, sensors, displays) share a common ground rail.

---

## Repository contents

| File | Purpose |
|---|---|
| `catbot_merged.cpp` | Main ESP32 firmware — servo control, OLED face state machine, LCD driver, ultrasonic-driven cat mood logic, serial command parser |
| `platformio.ini` | PlatformIO project configuration and library dependencies |
| `control.py` | PC-side Xbox 360 controller client (sticks + triggers + buttons → serial commands) |
| `keyboard_control_client.py` | PC-side keyboard testing client (single-key servo/expression control) |

## Firmware setup

1. Open the project in VS Code with the PlatformIO extension.
2. Board: **Espressif ESP32 Dev Module**.
3. Libraries (declared in `platformio.ini`): `ESP32Servo`, `Adafruit GFX Library`,
   `Adafruit SSD1306`. (`WebSockets` and `ArduinoJson` are also listed from an earlier
   wireless-control prototype and aren't required by the current build.)
4. Build and upload `catbot_merged.cpp` as `src/main.cpp`.

## PC control setup

```
pip install pyserial keyboard pygame
```

- `keyboard_control_client.py` — set `SERIAL_PORT` to your ESP32's COM port, close
  the PlatformIO Serial Monitor first (only one program can hold the port), then run.
- `control.py` — same port setup, requires an Xbox 360 controller connected.
  **Verify your controller's axis indices before relying on it** — these vary by
  driver/OS. Print `joystick.get_axis(i)` for each axis while moving each
  stick/trigger to confirm which index maps to what on your machine.

### Keyboard controls

| Key(s) | Action |
|---|---|
| `1` / `2` | Head left / right (5° nudge) |
| `3` / `4` | Waist left / right (5° nudge) |
| `5` / `6` | Paw down / up (5° nudge) |
| `0` | Center all three servos |
| `p` | Photo pose sequence (countdown → wink → hold) |
| `w` / `a` / `l` / `z` / `s` / `n` / `u` / `e` | Wink / Angry / Love / Dizzy / Sad / Sneaky / Proud / Excited |
| `r` | Resume automatic proximity-driven behavior |
| `Esc` | Quit the control script |

### Controller mapping (`control.py`)

| Input | Action |
|---|---|
| Left stick X | Waist rotation |
| Right stick X | Head rotation |
| Left Trigger (LT) | Paw down |
| Right Trigger (RT) | Paw up |
| LB | Center all servos |
| RB | Photo pose |
| Start | Resume automatic mode |
| Back | Quit |

---

## Known limitations (v0.5)

- **Waist/body rotation is functional but not fully smooth.** The body currently
  rests directly on the servo horn with no dedicated bearing, so the SG90 is both
  supporting structural weight and driving rotation at once — this is a known,
  accepted trade-off for this version rather than a bug. Planned fix: add a bearing
  or center pivot in the next revision.
- PIR and LDR are wired-for but not yet read by firmware logic.
- No wireless control in the current build (USB serial only); an earlier WiFi/WebSocket
  prototype exists in project history but was set aside for this version.
- The robot cannot walk — it's mounted on a fixed stand for this version by design.

## Roadmap

- Integrate PIR (startle reactions) and LDR (light-driven mood/sleep behavior)
- Add a bearing/pivot to smooth out waist rotation
- Autonomous mode: blend sensor-driven reactions with manual override seamlessly
- Paw-touch / high-five interaction handling
- Revisit wireless (WiFi) control for an untethered build

---

## Credits

Built by **Ismat Erena Siddiquee** and **Afif Bin Zaman** as an equal collaboration —
hardware assembly, firmware, and control software were developed together.
