#include<SoftwareSerial.h>
#include "ArduinoJson-master\src\ArduinoJson.h"
#include "ArduinoJson-master\src\ArduinoJson\StaticJsonBuffer.hpp"
#define TxD 3
#define RxD 2

SoftwareSerial bluetoothSerial(TxD, RxD);

#define PIN_EN_L 11
#define PIN_IN1_L 12
#define PIN_IN2_L 13

#define PIN_EN_R 10
#define PIN_IN1_R 9
#define PIN_IN2_R 8
typedef enum {
  STATE_FORWARD, STATE_REVERSE, STATE_LEFT, STATE_RIGHT, STATE_PIVOT_L, STATE_PIVOT_R, STATE_STOP
} MotionStates_t;
// States of locomotion that the robot can take. (details in comments for handleMotors function)
int currState = STATE_STOP;
//long tnow, tnext = 0;
//long full = 1400; // for 200
//long twentyeight = 2000-200;
int turnCheck = 0;
int goCheck = 0;
int theta = 0;
void setup() {
  bluetoothSerial.begin(9600);
  Serial.begin(9600);
  // put your setup code here, to run once:
  pinMode(PIN_EN_L, OUTPUT);
  pinMode(PIN_IN1_L, OUTPUT);
  pinMode(PIN_IN2_L, OUTPUT);  
  pinMode(PIN_EN_R, OUTPUT);
  pinMode(PIN_IN1_R, OUTPUT);  
  pinMode(PIN_IN2_R, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  motor();
}

void motor() {
  char json[200];
  memset(json, 0, sizeof(char) * 200);
  int numBytes = bluetoothSerial.available();
  if (numBytes == 0) {
    analogWrite(PIN_EN_L, 0);
    digitalWrite(PIN_IN1_L, HIGH);
    digitalWrite(PIN_IN2_L, LOW);
    analogWrite(PIN_EN_R, 0);
    digitalWrite(PIN_IN1_R, LOW);
    digitalWrite(PIN_IN2_R, HIGH);
    return;
  }
  int count = 0;
  while (bluetoothSerial.peek()!= '-'){
    json[count] = bluetoothSerial.read();
    Serial.print(json[count]);
    count++;
  }
  bluetoothSerial.read(); // get rid of "-"
  Serial.println(json);
    StaticJsonBuffer<200> jsonBuffer;
    JsonObject& root = jsonBuffer.parseObject(json);
    float Front[2] = {root["Front"][0], root["Front"][1]};
    float Back[2] = {root["Back"][0], root["Back"][1]};
    float Target[2] = {root["Target"][0], root["Target"][1]};
    float B[2] = {(Front[0]+Back[0])/2, (Front[1]+Back[1])/2};
    float AB[2] = {(B[0]-Front[0]), (B[1]-Front[1])};
    float BC[2] = {(Target[0]-B[0]), (Target[1]-B[1])};
    theta = acos((AB[0]*BC[0]+AB[1]*BC[1])/(abs(AB)*abs(BC)));
    if (turnCheck == 0 && theta<5 && theta>-5) {
      analogWrite(PIN_EN_L, 0);
      digitalWrite(PIN_IN1_L, HIGH);
      digitalWrite(PIN_IN2_L, LOW);
      analogWrite(PIN_EN_R, 0);
      digitalWrite(PIN_IN1_R, LOW);
      digitalWrite(PIN_IN2_R, HIGH);
      turnCheck = 1;
    }
    if (turnCheck == 0 && theta>5) {
      analogWrite(PIN_EN_L, 200);
      digitalWrite(PIN_IN1_L, HIGH);
      digitalWrite(PIN_IN2_L, LOW);
      analogWrite(PIN_EN_R, 200);
      digitalWrite(PIN_IN1_R, LOW);
      digitalWrite(PIN_IN2_R, HIGH);
    }
    if (turnCheck == 1 && abs(BC)<10) {
      analogWrite(PIN_EN_L, 0);
      digitalWrite(PIN_IN1_L, HIGH);
      digitalWrite(PIN_IN2_L, LOW);
      analogWrite(PIN_EN_R, 0);
      digitalWrite(PIN_IN1_R, LOW);
      digitalWrite(PIN_IN2_R, HIGH);
      turnCheck = 0;
    }
    if (turnCheck == 1 && abs(BC)>10) {
      analogWrite(PIN_EN_L, 200);
      digitalWrite(PIN_IN1_L, HIGH);
      digitalWrite(PIN_IN2_L, LOW);
      analogWrite(PIN_EN_R, 200);
      digitalWrite(PIN_IN1_R, HIGH);
      digitalWrite(PIN_IN2_R, LOW);
    }
}
