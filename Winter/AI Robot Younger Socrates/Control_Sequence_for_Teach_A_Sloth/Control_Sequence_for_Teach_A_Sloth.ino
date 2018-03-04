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


// Nodding Control - Stepper Motor 
static const int stepsPerRevolution = 48;  // change this to fit the number of steps per Loop
static int nodSpeed = 20;
static const int stepsPerLoop = 8;
static const int stepperIn1Pin = 4;
static const int stepperIn2Pin = 5;
static const int stepperIn3Pin = 6;
static const int stepperIn4Pin = 7;
Stepper nodStepper(stepsPerRevolution, stepperIn1Pin, stepperIn2Pin, stepperIn3Pin, stepperIn4Pin);
bool isNodding = false; // switch for whether sloth is nodding (servo)
bool nodDownwards = false;

// Jaw Control - single servo
static const int jawPin = 10;
Servo jawServo;  //servo for moving jaw for speaking
int jawPos = 0;    // variable to store the servo position for speaking
int jawPosInit = 0;
bool isSpeaking = false; // switch for whether sloth is speaking (servo)

// Arm Control - servo on left arm
static const int rArmPin = 9;
Servo rArmServo;
int rArmPos = 0;    // variable to store the servo position for speaking
int rArmPosInit = 0;
bool rArmMoving = false; // switch for whether sloth is speaking (servo)
#define ARM_IN 0
#define ARM_USER 90
#define ARM_SCREEN 180


void setup() {
  Serial.begin(9600);
  btSerial.begin(9600);
  nodStepper.setSpeed(nodSpeed);
  jawServo.attach(jawPin);  
  rArmServo.attach(rArmPin);  
}

void loop() {
//  if (listening) {
//    nod();
//  }
//  if (thinking) {
//    think();
//  }
//  if (speaking) {
//    moveJaw();
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
      isNodding = !isNodding;
      break;
    case 's':
      isSpeaking = !isSpeaking;
      jawPos = jawPosInit;
      moveJaw();
      break;
    case 't':
      // tilt head;
      break; 
    case 'a':
      // debug
      moveArm(0);
      break;
    case 'b':
      // debug
      moveArm(90);
      break;
    case 'c':
      // debug
      moveArm(180);
      break;
    case 'd':
      // debug
      moveArm(270);
      break;
    case 'e':
      // debug
      moveArm(360);
      break;
    case 'z':
      // debug
      moveArm(450);
      break;
    
  }
}

void nod(void) {
    int steps = stepsPerLoop;
    if (nodDownwards) steps = -steps;
    nodStepper.step(steps); // TODO: Change this blocking function to do multiple steps over multiple loops instead   
    nodDownwards = !nodDownwards; 
}

void think(void) {
    // Move head down 
    
    // Move arm in
    moveArm(ARM_IN);
}

void moveJaw(void) {
  if (jawPos > 360) jawPos -= 360;
  int servoInput = (jawPos > 180 ? 360 - jawPos : jawPos);
  jawServo.write(servoInput);              // tell servo to go to position in variable 'pos' 
  jawPos++;
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

