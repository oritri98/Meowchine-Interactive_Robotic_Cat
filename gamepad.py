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

