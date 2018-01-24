#include<SoftwareSerial.h>
#include "ArduinoJson-master\src\ArduinoJson.h"
#include "ArduinoJson-master\src\ArduinoJson\StaticJsonBuffer.hpp"
#define TxD 3 // RX
#define RxD 2 // TX

SoftwareSerial bluetoothSerial(TxD, RxD); // RX, TX

#define PIN_EN_L 11
#define PIN_IN1_L 12
#define PIN_IN2_L 13

#define PIN_EN_R 10
#define PIN_IN1_R 9
#define PIN_IN2_R 8

#define MOTOR_SPEED 200

int turnCheck = 0;
int goCheck = 0;
float theta = 0;

// JSON Stuff
char json[200];
int count = 0;
char message = 0;

void setup() {
  memset(json, 0, sizeof(char) * 200);
  bluetoothSerial.begin(9600);
  Serial.begin(9600);
  pinMode(PIN_EN_L, OUTPUT);
  pinMode(PIN_IN1_L, OUTPUT);
  pinMode(PIN_IN2_L, OUTPUT);
  pinMode(PIN_EN_R, OUTPUT);
  pinMode(PIN_IN1_R, OUTPUT);
  pinMode(PIN_IN2_R, OUTPUT);
}

void loop() {
  motor();
}

void motor() {
  int numBytes = bluetoothSerial.available();
  //  if (numBytes == 0) {
  //    analogWrite(PIN_EN_L, 0);
  //    digitalWrite(PIN_IN1_L, HIGH);
  //    digitalWrite(PIN_IN2_L, HIGH);
  //    analogWrite(PIN_EN_R, 0);
  //    digitalWrite(PIN_IN1_R, HIGH);
  //    digitalWrite(PIN_IN2_R, HIGH);
  //    return;
  //  }
  if (bluetoothSerial.available()) {
    message = (char)bluetoothSerial.read();
  }
  // Serial.println(message);
  // State switch for turning/moving forward
  if (message == '0') {
    // STOP!
    analogWrite(PIN_EN_L, 0);
    digitalWrite(PIN_IN1_L, LOW);
    digitalWrite(PIN_IN2_L, HIGH);
    analogWrite(PIN_EN_R, 0);
    digitalWrite(PIN_IN1_R, HIGH);
    digitalWrite(PIN_IN2_R, LOW);
  }
  if (message == '1') {
    // Forward
    analogWrite(PIN_EN_L, MOTOR_SPEED);
    digitalWrite(PIN_IN1_L, LOW);
    digitalWrite(PIN_IN2_L, HIGH);
    analogWrite(PIN_EN_R, MOTOR_SPEED);
    digitalWrite(PIN_IN1_R, HIGH);
    digitalWrite(PIN_IN2_R, LOW);
  }
  if (message == '2') {
    // Turn Right
    analogWrite(PIN_EN_L, MOTOR_SPEED);
    digitalWrite(PIN_IN1_L, HIGH);
    digitalWrite(PIN_IN2_L, LOW);
    analogWrite(PIN_EN_R, MOTOR_SPEED);
    digitalWrite(PIN_IN1_R, HIGH);
    digitalWrite(PIN_IN2_R, LOW);
  }
  if (message == '3') {
    // Turn Left
    analogWrite(PIN_EN_L, MOTOR_SPEED);
    digitalWrite(PIN_IN1_L, LOW);
    digitalWrite(PIN_IN2_L, HIGH);
    analogWrite(PIN_EN_R, MOTOR_SPEED);
    digitalWrite(PIN_IN1_R, LOW);
    digitalWrite(PIN_IN2_R, HIGH);
  }
  if (message == '4') {
    // Backward
    analogWrite(PIN_EN_L, MOTOR_SPEED);
    digitalWrite(PIN_IN1_L, HIGH);
    digitalWrite(PIN_IN2_L, LOW);
    analogWrite(PIN_EN_R, MOTOR_SPEED);
    digitalWrite(PIN_IN1_R, LOW);
    digitalWrite(PIN_IN2_R, HIGH);
  }
}
