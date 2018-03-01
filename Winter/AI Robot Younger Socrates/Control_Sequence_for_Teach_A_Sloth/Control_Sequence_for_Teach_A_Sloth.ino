/*  Control Sequence for Teach'A Sloth 
 *  Team NetDragon 2017-2018
 *  ME310, Stanford University.
 *  Managed by: Ye Wang
 */

#include <Servo.h>
#include <Stepper.h>

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
static const int jawPin = 3;
Servo jawServo;  //servo for moving jaw for speaking
int jawPos = 0;    // variable to store the servo position for speaking
int jawPosInit = 0;
bool isSpeaking = false; // switch for whether sloth is speaking (servo)

// Arms Control - two servos
bool isFlailing = false;

static const int lArmPin = 8;
Servo lArmServo;
int lArmPos = 0;    // variable to store the servo position for speaking
int lArmPosInit = 0;
bool lArmMoving = false; // switch for whether sloth is speaking (servo)

static const int rArmPin = 9;
Servo rArmServo;
int rArmPos = 0;    // variable to store the servo position for speaking
int rArmPosInit = 0;
bool rArmMoving = false; // switch for whether sloth is speaking (servo)


void setup() {
  Serial.begin(9600);
  nodStepper.setSpeed(nodSpeed);
  jawServo.attach(jawPin);  
  rArmServo.attach(rArmPin);  
  lArmServo.attach(lArmPin);  
}

void loop() {
  if (isNodding) {
    nod();
  }
  if (isSpeaking) {
    moveJaw();
  }
  if (isFlailing) {
    flail();
  }
  
  checkInput();
}

void checkInput(void) {
  if (Serial.available()) {
    char c = Serial.read();
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
      case 'f':
        isFlailing = !isFlailing;
        break; 
      case 't':
        // tilt head;
        break; 
    }
  }
}

void nod(void) {
    int steps = stepsPerLoop;
    if (nodDownwards) steps = -steps;
    nodStepper.step(steps); // TODO: Change this blocking function to do multiple steps over multiple loops instead   
    nodDownwards = !nodDownwards; 
}

void moveJaw(void) {
  if (jawPos > 360) jawPos -= 360;
  int servoInput = (jawPos > 180 ? 360 - jawPos : jawPos);
  jawServo.write(servoInput);              // tell servo to go to position in variable 'pos' 
  jawPos++;
}

void flail(void) {
  Serial.println("Flailing");
  moveRightArm();
  moveLeftArm();
}

void moveRightArm(void) {
  if (rArmPos > 360) rArmPos -= 360;
  int servoInput = (rArmPos > 180 ? 360 - rArmPos : rArmPos);
  rArmServo.write(servoInput);              // tell servo to go to position in variable 'pos' 
  rArmPos++;
}
void moveLeftArm(void) {
  if (lArmPos > 360) lArmPos -= 360;
  int servoInput = (lArmPos > 180 ? 360 - lArmPos : lArmPos);
  lArmServo.write(servoInput);              // tell servo to go to position in variable 'pos' 
  lArmPos++;
}
