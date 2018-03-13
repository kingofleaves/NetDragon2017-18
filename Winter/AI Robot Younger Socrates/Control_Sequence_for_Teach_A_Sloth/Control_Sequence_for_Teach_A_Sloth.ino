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
#define HEAD_CW 160
#define HEAD_STOP 90
#define HEAD_CCW 20

// Nodding Control 
#define NOD_INTERVAL 1000 // in ms
#define NOD_FLIP 400
long lastNodTime = 0; 
bool noddingDown = false;

// Arm Control - servo on left arm
static const int rArmPin = 9;
Servo rArmServo;
int rArmPos = 0;    // variable to store the servo position for speaking
int rArmPosInit = 0;
bool rArmMoving = false; // switch for whether sloth is speaking (servo)
#define ARM_IN 160
#define ARM_FORWARD 80
#define ARM_OUT 0

// States
bool listening = false;
bool thinking = false;
bool speaking = false;


void setup() {
  Serial.begin(9600);
  btSerial.begin(9600);
  headServo.attach(headPin);  
  rArmServo.attach(rArmPin);  
  moveArm(ARM_FORWARD);
  moveHead(HEAD_STOP);
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
      nod();
      break;
    case 'm':
      stopNod();
      break;
    case 'l':
      nodOnce();
      break;
    case 's':
      speaking = !speaking;
      headPos = headPosInit;
      break;
    case 'p':
      moveArm(ARM_OUT);
      moveHead(HEAD_STOP);
      break;
    case 'u':
      moveArm(ARM_FORWARD);
      moveHead(HEAD_STOP);
      break; 
    case 'w':
      wave();
      break; 
    case 't':
      // thinking = !thinking;
      think();
      break; 
    case 'a':
      // debug
      moveArm(ARM_OUT);
      break;
    case 'b':
      // debug
      moveArm(ARM_FORWARD);
      break;
    case 'c':
      // debug
      moveArm(ARM_IN);
      break;
    case 'd':
      // debug
      moveArm(HEAD_CCW);
      break;
  }
}

void nod(void) {
  moveHead(HEAD_CW);
}

void stopNod() {
  moveHead(HEAD_STOP);
}

void nodOnce(){
  moveHead(HEAD_CW);
  delay(500);
  moveHead(HEAD_STOP);
}

void wave() {
  // Temp blocking function
  int waveDelay = 400;
  for (int i = 0; i < 5; i++) {
    moveArm(ARM_OUT);
    delay(waveDelay);
    moveArm(ARM_IN);
    delay(waveDelay);
  } 
}

void think(void) {
    // Move head down 
//    moveHead(HEAD_DOWN);
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

