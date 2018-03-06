/*  Control Sequence for Teach'A Sloth 
 *  Team NetDragon 2017-2018
 *  ME310, Stanford University.
 *  Managed by: Ye Wang
 */

#include <Servo.h>
#include <Stepper.h>
#include <SoftwareSerial.h>

// Bluetooth SoftwareSerial
static const int TxD = 2;
static const int RxD = 3;
SoftwareSerial btSerial(TxD, RxD);

// Head Control - single servo
static const int headPin = 10;
Servo headServo;  //servo for moving jaw for speaking
int headPos = 0;    // variable to store the servo position for speaking
int headPosInit = 0;
#define HEAD_DOWN 30
#define HEAD_MID 90
#define HEAD_UP 150

// Nodding Control 
#define NOD_INTERVAL 500 // in ms
long lastNodTime = 0; 
bool noddingDown = false;

// Arm Control - servo on left arm
static const int rArmPin = 9;
Servo rArmServo;
int rArmPos = 0;    // variable to store the servo position for speaking
int rArmPosInit = 0;
bool rArmMoving = false; // switch for whether sloth is speaking (servo)
#define ARM_IN 0
#define ARM_USER 90
#define ARM_SCREEN 180

// States
bool listening = false;
bool thinking = false;
bool speaking = false;


void setup() {
  Serial.begin(9600);
  btSerial.begin(9600);
  headServo.attach(headPin);  
  rArmServo.attach(rArmPin);  
}

void loop() {
  if (listening) {
    nod();
  }
  if (thinking) {
    think();
  }
//  if (speaking) {
//    moveHead();
//  }
//  if (screen) {
//    pointToScreen();
//  }
//  
  checkInput();
}

void checkInput(void) {
  char c = 0;
  if (Serial.available()) {
    c = Serial.read();
  }
  if (btSerial.available()) {
    c = btSerial.read();
  }
  if (c == 0) return;
  Serial.println(c);
  switch (c) {
    case 'n':
      Serial.println("nod");
      listening = !listening;
      break;
    case 's':
      speaking = !speaking;
      headPos = headPosInit;
      break;
    case 't':
      thinking = !thinking;
      break; 
    case 'a':
      // debug
      moveArm(0);
      moveHead(HEAD_UP);
      break;
    case 'b':
      // debug
      moveArm(90);
      moveHead(HEAD_MID);
      break;
    case 'c':
      // debug
      moveArm(180);
      moveHead(HEAD_DOWN);
      break;
  }
}

void nod(void) {
    if (millis() - lastNodTime < NOD_INTERVAL/2) return;
    if (noddingDown) {
       moveHead(HEAD_UP); 
    } else {
      moveHead(HEAD_DOWN);
    }
    noddingDown = !noddingDown;
    lastNodTime = millis();
}

void think(void) {
    // Move head down 
    moveHead(HEAD_DOWN);
    // Move arm in
    moveArm(ARM_IN);
}

void moveHead(int pos) {
  headServo.write(pos);              // tell servo to go to position in variable 'pos' 
}

void moveArm(int pos) {
  rArmServo.write(pos);
}

void swingRightArm(void) {
  if (rArmPos > 360) rArmPos -= 360;
  int servoInput = (rArmPos > 180 ? 360 - rArmPos : rArmPos);
  rArmServo.write(servoInput);              // tell servo to go to position in variable 'pos' 
  rArmPos++;
}

