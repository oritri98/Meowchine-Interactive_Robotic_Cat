/*
  Scan-Bot: Cat Personality Build
  Merges: Ultrasonic (proximity) + OLED face + LCD (2nd I2C bus) + head servo sweep

  WIRING:
    OLED:  SDA -> GPIO 21, SCL -> GPIO 22, VCC -> 3.3V
    LCD:   SDA -> GPIO 33, SCL -> GPIO 32, VCC -> 5V (through level shifter), backpack addr below
    Ultrasonic: TRIG -> GPIO 5, ECHO -> GPIO 4 (through voltage divider)
    Servo: signal -> GPIO 18, powered from external 5V, NOT the ESP32 pin

  Set ENABLE_SERVO_SWEEP to false below if you don't want the head moving for this test.
*/

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ESP32Servo.h>

#define ENABLE_SERVO_SWEEP true

bool manualControl = true; // starts TRUE -- servos stay still until you send a keyboard command

// ================= OLED =================
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_SDA 21
#define OLED_SCL 22
#define OLED_RESET -1
#define OLED_ADDR 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

enum Expression { NEUTRAL, HAPPY, SURPRISED, SLEEPY, CURIOUS, WINK, ANGRY, LOVE, DIZZY, SAD, SNEAKY, PROUD, EXCITED };
Expression currentExpression = NEUTRAL;

bool isBlinking = false;
unsigned long blinkStartTime = 0;
unsigned long nextBlinkTime = 0;
const unsigned long BLINK_DURATION = 150;
int eyeOffsetX = 0;

unsigned long randomBlinkInterval() { return random(2000, 5000); }



