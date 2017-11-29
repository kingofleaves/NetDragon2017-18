#include<SoftwareSerial.h>

#define TxD 3
#define RxD 2

SoftwareSerial bluetoothSerial(TxD, RxD);

char c;
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
long tnow, tnext = 0;
long full = 1400; // for 200
long twentyeight = 2000-200;
long theta = 270;
int turnCheck = 0;
int goCheck = 0;
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
  tnow = millis();           // get current millisec counter value
  if (bluetoothSerial.available())
  if (turnCheck == 0 && tnow-tnext >= full*theta/360) {
    analogWrite(PIN_EN_L, 0);
    digitalWrite(PIN_IN1_L, HIGH);
    digitalWrite(PIN_IN2_L, LOW);
    analogWrite(PIN_EN_R, 0);
    digitalWrite(PIN_IN1_R, LOW);
    digitalWrite(PIN_IN2_R, HIGH);
    turnCheck = 1;
    tnext = tnow + full*theta/360;
  }
  if (turnCheck == 0 && tnow>=tnext) {
    analogWrite(PIN_EN_L, 200);
    digitalWrite(PIN_IN1_L, HIGH);
    digitalWrite(PIN_IN2_L, LOW);
    analogWrite(PIN_EN_R, 200);
    digitalWrite(PIN_IN1_R, LOW);
    digitalWrite(PIN_IN2_R, HIGH);
  }
  if (turnCheck == 1 && tnow-tnext >= twentyeight) {
    analogWrite(PIN_EN_L, 0);
    digitalWrite(PIN_IN1_L, HIGH);
    digitalWrite(PIN_IN2_L, LOW);
    analogWrite(PIN_EN_R, 0);
    digitalWrite(PIN_IN1_R, LOW);
    digitalWrite(PIN_IN2_R, HIGH);
    turnCheck = 1;
  }
  if (turnCheck == 1 && tnow>=tnext) {
    analogWrite(PIN_EN_L, 200);
    digitalWrite(PIN_IN1_L, HIGH);
    digitalWrite(PIN_IN2_L, LOW);
    analogWrite(PIN_EN_R, 200);
    digitalWrite(PIN_IN1_R, HIGH);
    digitalWrite(PIN_IN2_R, LOW);
  }
}
