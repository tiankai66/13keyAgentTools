// 13keyAgentTools Rev 0.2
// Arduino Micro MVP firmware for a multi-agent macro keyboard.

#include <Keyboard.h>
#include <stdio.h>
#include <string.h>

// Set to 1 after installing Adafruit NeoPixel and wiring the quota strip.
#ifndef ENABLE_RGB
#define ENABLE_RGB 0
#endif

#if ENABLE_RGB
#include <Adafruit_NeoPixel.h>
#define RGB_COUNT 12
Adafruit_NeoPixel pixels(RGB_COUNT, A3, NEO_GRB + NEO_KHZ800);
#endif

const uint8_t ROW_COUNT = 4;
const uint8_t COL_COUNT = 4;
const uint8_t rowPins[ROW_COUNT] = {4, 5, 6, 7};
const uint8_t colPins[COL_COUNT] = {8, 9, 10, 11};

const uint8_t encoderA = 14;
const uint8_t encoderB = 15;
const uint8_t encoderSwitch = 16;
const uint8_t volumeEncoderA = 2;
const uint8_t volumeEncoderB = 3;
const uint8_t volumeEncoderSwitch = 12;
const uint8_t joystickX = A0;
const uint8_t joystickY = A1;
const uint8_t touchPin = A2;

const uint32_t debounceMs = 25;
const int16_t joystickDeadzone = 220;
const uint32_t joystickRepeatMs = 250;

enum Action : uint8_t {
  ACTION_NONE = 0,
  ACTION_ACCEPT,
  ACTION_REJECT,
  ACTION_NEW_CHAT,
  ACTION_PUSH_TO_TALK,
  ACTION_FUNCTION_1,
  ACTION_FUNCTION_2,
  ACTION_FUNCTION_3,
  ACTION_FUNCTION_4,
  ACTION_FUNCTION_5,
  ACTION_FUNCTION_6,
  ACTION_FUNCTION_7,
  ACTION_FUNCTION_8,
  ACTION_FUNCTION_9,
  ACTION_LAYER,
};

// 4x4 matrix; three positions are intentionally unused.
const Action actions[ROW_COUNT][COL_COUNT] = {
  {ACTION_ACCEPT, ACTION_REJECT, ACTION_NEW_CHAT, ACTION_PUSH_TO_TALK},
  {ACTION_FUNCTION_1, ACTION_FUNCTION_2, ACTION_FUNCTION_3, ACTION_FUNCTION_4},
  {ACTION_FUNCTION_5, ACTION_FUNCTION_6, ACTION_FUNCTION_7, ACTION_FUNCTION_8},
  {ACTION_NONE, ACTION_FUNCTION_9, ACTION_NONE, ACTION_NONE},
};

bool matrixStable[ROW_COUNT][COL_COUNT] = {};
uint32_t matrixChangedAt[ROW_COUNT][COL_COUNT] = {};

uint8_t lastEncoderState = 0;
bool lastEncoderSwitch = HIGH;
uint8_t lastVolumeEncoderState = 0;
bool lastVolumeEncoderSwitch = HIGH;
bool lastTouchState = LOW;
uint32_t lastJoystickEventAt = 0;
int16_t joystickCenterX = 512;
int16_t joystickCenterY = 512;

void tapKey(uint8_t key) {
  Keyboard.press(key);
  delay(8);
  Keyboard.release(key);
}

void sendCombo(uint8_t modifier, uint8_t key) {
  Keyboard.press(modifier);
  Keyboard.press(key);
  delay(8);
  Keyboard.release(key);
  Keyboard.release(modifier);
}

void sendFunction(uint8_t functionNumber) {
  // Arduino Keyboard defines KEY_F1..KEY_F12. Keep function keys as
  // Temporary host-side workflow hooks until per-agent shortcuts are configured.
  switch (functionNumber) {
    case 1: tapKey(KEY_F1); break;
    case 2: tapKey(KEY_F2); break;
    case 3: tapKey(KEY_F3); break;
    case 4: tapKey(KEY_F4); break;
    case 5: tapKey(KEY_F5); break;
    case 6: tapKey(KEY_F6); break;
    case 7: tapKey(KEY_F7); break;
    case 8: tapKey(KEY_F8); break;
    case 9: tapKey(KEY_F9); break;
    case 10: tapKey(KEY_F10); break;
    case 11: tapKey(KEY_F11); break;
    case 12: tapKey(KEY_F12); break;
    default: break;
  }
}

void emitAction(Action action) {
  switch (action) {
    case ACTION_ACCEPT:
      tapKey(KEY_RETURN);
      break;
    case ACTION_REJECT:
      tapKey(KEY_ESC);
      break;
    case ACTION_NEW_CHAT:
      sendCombo(KEY_LEFT_CTRL, 'n');
      break;
    case ACTION_PUSH_TO_TALK:
      Keyboard.press(KEY_LEFT_CTRL);
      Keyboard.press(KEY_LEFT_SHIFT);
      Keyboard.press('d');
      delay(8);
      Keyboard.release('d');
      Keyboard.release(KEY_LEFT_SHIFT);
      Keyboard.release(KEY_LEFT_CTRL);
      break;
    case ACTION_FUNCTION_1: sendFunction(1); break;
    case ACTION_FUNCTION_2: sendFunction(2); break;
    case ACTION_FUNCTION_3: sendFunction(3); break;
    case ACTION_FUNCTION_4: sendFunction(4); break;
    case ACTION_FUNCTION_5: sendFunction(5); break;
    case ACTION_FUNCTION_6: sendFunction(6); break;
    case ACTION_FUNCTION_7: sendFunction(7); break;
    case ACTION_FUNCTION_8: sendFunction(8); break;
    case ACTION_FUNCTION_9: sendFunction(9); break;
    case ACTION_LAYER: sendFunction(10); break;
    case ACTION_NONE: break;
  }
}

void setupMatrix() {
  for (uint8_t row = 0; row < ROW_COUNT; row++) {
    pinMode(rowPins[row], OUTPUT);
    digitalWrite(rowPins[row], HIGH);
  }
  for (uint8_t col = 0; col < COL_COUNT; col++) {
    pinMode(colPins[col], INPUT_PULLUP);
  }
}

void scanMatrix() {
  const uint32_t now = millis();

  for (uint8_t row = 0; row < ROW_COUNT; row++) {
    for (uint8_t other = 0; other < ROW_COUNT; other++) {
      digitalWrite(rowPins[other], HIGH);
    }
    digitalWrite(rowPins[row], LOW);
    delayMicroseconds(30);

    for (uint8_t col = 0; col < COL_COUNT; col++) {
      const bool pressed = digitalRead(colPins[col]) == LOW;
      if (pressed != matrixStable[row][col]) {
        if (now - matrixChangedAt[row][col] >= debounceMs) {
          matrixStable[row][col] = pressed;
          if (pressed) {
            emitAction(actions[row][col]);
          }
        }
      } else {
        matrixChangedAt[row][col] = now;
      }
    }
  }
  digitalWrite(rowPins[0], HIGH);
}

void scanEncoder() {
  const uint8_t currentState = (digitalRead(encoderA) << 1) | digitalRead(encoderB);
  if (currentState != lastEncoderState) {
    const bool clockwise =
      (lastEncoderState == 0 && currentState == 1) ||
      (lastEncoderState == 1 && currentState == 3) ||
      (lastEncoderState == 3 && currentState == 2) ||
      (lastEncoderState == 2 && currentState == 0);
    sendFunction(clockwise ? 12 : 11);
    lastEncoderState = currentState;
  }

  const bool currentSwitch = digitalRead(encoderSwitch);
  if (currentSwitch != lastEncoderSwitch) {
    delay(3);
    if (digitalRead(encoderSwitch) == LOW) {
      sendFunction(10);
    }
    lastEncoderSwitch = currentSwitch;
  }
}

void scanVolumeEncoder() {
  const uint8_t currentState =
    (digitalRead(volumeEncoderA) << 1) | digitalRead(volumeEncoderB);
  if (currentState != lastVolumeEncoderState) {
    const bool clockwise =
      (lastVolumeEncoderState == 0 && currentState == 1) ||
      (lastVolumeEncoderState == 1 && currentState == 3) ||
      (lastVolumeEncoderState == 3 && currentState == 2) ||
      (lastVolumeEncoderState == 2 && currentState == 0);
    // Temporary F11/F12 hooks; map these to USB Consumer volume codes later.
    sendFunction(clockwise ? 12 : 11);
    lastVolumeEncoderState = currentState;
  }

  const bool currentSwitch = digitalRead(volumeEncoderSwitch);
  if (currentSwitch != lastVolumeEncoderSwitch) {
    delay(3);
    if (digitalRead(volumeEncoderSwitch) == LOW) {
      sendFunction(10);
    }
    lastVolumeEncoderSwitch = currentSwitch;
  }
}

void scanTouch() {
  const bool currentTouch = digitalRead(touchPin);
  if (currentTouch != lastTouchState) {
    delay(3);
    if (currentTouch == HIGH) {
      sendFunction(10);
    }
    lastTouchState = currentTouch;
  }
}

void scanJoystick() {
  const int16_t x = analogRead(joystickX);
  const int16_t y = analogRead(joystickY);
  const int16_t dx = x - joystickCenterX;
  const int16_t dy = y - joystickCenterY;
  if (millis() - lastJoystickEventAt < joystickRepeatMs) {
    return;
  }

  uint8_t functionNumber = 0;
  if (abs(dx) > joystickDeadzone || abs(dy) > joystickDeadzone) {
    if (abs(dx) >= abs(dy)) {
      functionNumber = dx > 0 ? 1 : 2;
    } else {
      functionNumber = dy > 0 ? 3 : 4;
    }
    sendFunction(functionNumber);
    lastJoystickEventAt = millis();
  }
}

void setRgb(uint8_t index, uint8_t red, uint8_t green, uint8_t blue) {
#if ENABLE_RGB
  if (index >= RGB_COUNT) {
    return;
  }
  pixels.setPixelColor(index, pixels.Color(red, green, blue));
  pixels.show();
#else
  (void)index;
  (void)red;
  (void)green;
  (void)blue;
#endif
}

void clearRgb() {
#if ENABLE_RGB
  pixels.clear();
  pixels.show();
#endif
}

void setQuotaPercent(uint8_t percent) {
#if ENABLE_RGB
  const uint8_t clamped = percent > 100 ? 100 : percent;
  const uint8_t lit = (static_cast<uint16_t>(clamped) * RGB_COUNT) / 100;
  uint8_t red = 0;
  uint8_t green = 0;
  uint8_t blue = 0;
  if (clamped <= 25) {
    red = 180;
  } else if (clamped <= 60) {
    red = 180;
    green = 100;
  } else {
    green = 180;
  }

  for (uint8_t index = 0; index < RGB_COUNT; index++) {
    if (index < lit) {
      pixels.setPixelColor(index, pixels.Color(red, green, blue));
    } else {
      pixels.setPixelColor(index, 0);
    }
  }
  pixels.show();
#else
  (void)percent;
#endif
}

void handleSerialCommand() {
  static char buffer[48];
  static uint8_t length = 0;

  while (Serial.available()) {
    const char ch = static_cast<char>(Serial.read());
    if (ch == '\n' || ch == '\r') {
      buffer[length] = '\0';
      uint16_t index = 0;
      uint16_t red = 0;
      uint16_t green = 0;
      uint16_t blue = 0;
      uint16_t percent = 0;
      if (sscanf(buffer, "LED %hu %hu %hu %hu", &index, &red, &green, &blue) == 4) {
        setRgb(index, red, green, blue);
      } else if (sscanf(buffer, "QUOTA %hu", &percent) == 1) {
        setQuotaPercent(percent > 100 ? 100 : percent);
      } else if (strcmp(buffer, "CLEAR") == 0) {
        clearRgb();
      }
      length = 0;
    } else if (length < sizeof(buffer) - 1) {
      buffer[length++] = ch;
    }
  }
}

void setup() {
  setupMatrix();
  pinMode(encoderA, INPUT_PULLUP);
  pinMode(encoderB, INPUT_PULLUP);
  pinMode(encoderSwitch, INPUT_PULLUP);
  pinMode(volumeEncoderA, INPUT_PULLUP);
  pinMode(volumeEncoderB, INPUT_PULLUP);
  pinMode(volumeEncoderSwitch, INPUT_PULLUP);
  pinMode(touchPin, INPUT_PULLUP);

  delay(250);
  joystickCenterX = analogRead(joystickX);
  joystickCenterY = analogRead(joystickY);
  lastEncoderState = (digitalRead(encoderA) << 1) | digitalRead(encoderB);
  lastEncoderSwitch = digitalRead(encoderSwitch);
  lastVolumeEncoderState =
    (digitalRead(volumeEncoderA) << 1) | digitalRead(volumeEncoderB);
  lastVolumeEncoderSwitch = digitalRead(volumeEncoderSwitch);
  lastTouchState = digitalRead(touchPin);

  Keyboard.begin();
  Serial.begin(115200);

#if ENABLE_RGB
  pixels.begin();
  pixels.setBrightness(32);
  pixels.clear();
  pixels.show();
#endif
}

void loop() {
  scanMatrix();
  scanEncoder();
  scanVolumeEncoder();
  scanTouch();
  scanJoystick();
  handleSerialCommand();
}
