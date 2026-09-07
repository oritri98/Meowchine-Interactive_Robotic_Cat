import serial
import pygame
import time

SERIAL_PORT = "COM10"
BAUD_RATE = 115200

# 1. Connect to ESP32
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2) # Give the ESP32 a moment to reset

