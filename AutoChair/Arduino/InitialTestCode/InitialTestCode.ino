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
float theta = 0;
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
    Serial.print("");
    count++;
  }
  Serial.print(json);
  Serial.print('\n');
  bluetoothSerial.read(); // get rid of "-"
    StaticJsonBuffer<200> jsonBuffer;
    JsonObject& root = jsonBuffer.parseObject(json);
    int Front[2];
    Front[0] = root["Front"][0];
    Front[1] = root["Front"][1];
    int Back[2];
    Back[0] = root["Back"][0];
    Back[1] = root["Back"][1];
    int Target[2];
    Target[0] = root["Target"][0];
    Target[1] = root["Target"][1];
    float B[2];
    B[0] = ((float)Front[0]+Back[0])/2;
    B[1] = ((float)Front[1]+Back[1])/2;
    float AB[2];
    AB[0] = (B[0]-Front[0]);
    AB[1] = (B[1]-Front[1]);
    float BC[2];
    BC[0] = (Target[0]-B[0]);
    BC[1] = (Target[1]-B[1]);
    theta = acos((AB[0]*BC[0]+AB[1]*BC[1])/(abs(AB)*abs(BC)));
    Serial.print("Front:");
    Serial.print(Front[0]);
    Serial.print(',');
    Serial.print(Front[1]);
    Serial.print('\n');
    Serial.print("Back:");
    Serial.print(Back[0]);
    Serial.print(',');
    Serial.print(Back[1]);
    Serial.print('\n');
    Serial.print("Target:");
    Serial.print(Target[0]);
    Serial.print(',');
    Serial.print(Target[1]);
    Serial.print('\n');
    if (turnCheck == 0 && theta<0.5 && theta>-0.5) {
      analogWrite(PIN_EN_L, 0);
      digitalWrite(PIN_IN1_L, HIGH);
      digitalWrite(PIN_IN2_L, LOW);
      analogWrite(PIN_EN_R, 0);
      digitalWrite(PIN_IN1_R, LOW);
      digitalWrite(PIN_IN2_R, HIGH);
      turnCheck = 1;
    }
    if (turnCheck == 0 && theta>0.5) {
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
