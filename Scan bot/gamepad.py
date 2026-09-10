import serial
import pygame
import time

SERIAL_PORT = "COM10"
BAUD_RATE = 115200

# 1. Connect to ESP32
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2) # Give the ESP32 a moment to reset

# 2. Initialize Controller
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller found. Please plug it in!")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Connected to: {joystick.get_name()}")
print("Press 'Back' on the controller to quit.")

# 3. Main Event Loop
clock = pygame.time.Clock()
running = True

# 3. Main Event Loop
clock = pygame.time.Clock()
running = True

# A deadzone prevents tiny stick drifts from making the robot jitter
DEADZONE = 0.5 

# Triggers rest at -1 (unpressed) and go to +1 (fully pressed).
# This threshold decides how far you need to pull a trigger before it counts as "pressed".
TRIGGER_THRESHOLD = -0.5

while running:
    # --- 1. Handle Button Clicks ---
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 4: ser.write(b'0') # LB -> Center All
            elif event.button == 5: ser.write(b'p') # RB -> Photo Pose
            elif event.button == 7: ser.write(b'r') # Start -> Resume Auto
            elif event.button == 6: running = False # Back -> Quit

    # --- 2. Poll Analog Sticks ---
    # Left Stick X-axis (Axis 0) controls Body
    left_x = joystick.get_axis(0)
    if left_x < -DEADZONE:
        ser.write(b'3') # Body Left
    elif left_x > DEADZONE:
        ser.write(b'4') # Body Right

    # Right Stick X-axis (Usually Axis 2 or 3) controls Head
    right_x = joystick.get_axis(2) 
    if right_x < -DEADZONE:
        ser.write(b'1') # Head Left
    elif right_x > DEADZONE:
        ser.write(b'2') # Head Right

    # --- 3. Poll Triggers for Paw ---
    # LT -> paw down, RT -> paw up
    left_trigger = joystick.get_axis(4)
    right_trigger = joystick.get_axis(5)
    if left_trigger > TRIGGER_THRESHOLD:
        ser.write(b'5') # LT -> Paw Down
    if right_trigger > TRIGGER_THRESHOLD:
        ser.write(b'6') # RT -> Paw Up

    clock.tick(30) # Sends commands 30 times per second while holding the stick

ser.close()
pygame.quit()
print("Closed.")