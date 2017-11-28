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

void setup() {
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
  analogWrite(PIN_EN_L, 200);
  digitalWrite(PIN_IN1_L, HIGH);
  digitalWrite(PIN_IN2_L, LOW);
  analogWrite(PIN_EN_R, 200);
  digitalWrite(PIN_IN1_R, HIGH);
  digitalWrite(PIN_IN2_R, LOW);
}

/***********************************
 * Function: handleMotors
 * arguments: currState (STATE_FORWARD, STATE_REVERSE, STATE_LEFT, STATE_RIGHT, STATE_PIVOT_L, STATE_PIVOT_R, STATE_STOP), 
 *            pulseInterval (0-255 or 256 to stop), 
 *            pulseDur (0 or longer)
 * Description: this function takes 3 arguments: 
 * currState, a MotionState which defines the motion of the robot, i.e. which way it moves (outlined below in the table), 
 * pulseInterval, the number of inactive pulses (no motor motion) between consecutive active pulses, and
 * pulseDur, the duration (in ms) of each pulse sent to the motor.
 * ----------------------------------------------------------
 * MotionState | Right Motor | Left Motor | Described Motion 
 * ----------------------------------------------------------
 * FORWARD     | FORWARD     | FORWARD    | Straight Forward 
 * REVERSE     | REVERSE     | REVERSE    | Straight Backward
 * LEFT        | FORWARD     | STOPPED    | Left Forward
 * RIGHT       | STOPPED     | FORWARD    | Right Forward
 * PIVOT_L     | FORWARD     | REVERSE    | Pivot left on the spot
 * PIVOT_R     | REVERSE     | FORWARD    | Pivot right on the spot
 * STOP        | STOPPED     | STOPPED    | Stop moving
 * ---------------------------------------
 * 
 ***********************************/
/** Tested and working **/
void handleMotors(MotionStates_t currState) {
    if (currState == STATE_STOP) {
      analogWrite(PIN_MOTOR_LEFT, 0);
      analogWrite(PIN_MOTOR_RIGHT, 0);
    } else {
      if (currState == STATE_FORWARD || currState == STATE_RIGHT || currState == STATE_PIVOT_R) {
        digitalWrite(PIN_MOTOR_LEFT_DIR, FORWARD_OUTPUT);
      } else {
        digitalWrite(PIN_MOTOR_LEFT_DIR, REVERSE_OUTPUT);
      }
      if (currState == STATE_FORWARD || currState == STATE_LEFT || currState == STATE_PIVOT_L) {
        digitalWrite(PIN_MOTOR_RIGHT_DIR, FORWARD_OUTPUT);
      } else {
        digitalWrite(PIN_MOTOR_RIGHT_DIR, REVERSE_OUTPUT);
      }
      if (currState == STATE_LEFT) {
        analogWrite(PIN_MOTOR_LEFT, 0);
      } else {
        analogWrite(PIN_MOTOR_LEFT, BASE_MOTOR_SPEED + leftDifferential);
      }
      if (currState == STATE_RIGHT) {
        analogWrite(PIN_MOTOR_RIGHT, 0);
      } else {
        analogWrite(PIN_MOTOR_RIGHT, BASE_MOTOR_SPEED + rightDifferential);
      }
      if (currState == STATE_STOP) {
        analogWrite(PIN_MOTOR_RIGHT, 0);
        analogWrite(PIN_MOTOR_LEFT, 0);
      }
}
