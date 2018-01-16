#include <SoftwareSerial.h>

#define ROBOTCMDLEN    6    // "MD +N "

SoftwareSerial mySerial(10, 9); // RX, TX
String my_buffer = "";
bool secondMotor = false;

typedef enum {
  WAIT_PROMPT, WAIT_ECHO
} States_t;

States_t state = WAIT_PROMPT;

long echoStart;
String prevMessage;

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  Serial.println("Potato Potahto!");

  // set the data rate for the SoftwareSerial port
  mySerial.begin(9600);
}

void loop() {
  switch (state) {
    case WAIT_PROMPT:
      if (checkPrompt(my_buffer)) {
        int motorSpeed1 = getMotorSpeed(1);
        int motorSpeed2 = getMotorSpeed(2);
        // Choose which Motor to send command to
        secondMotor ? sendMotorCommand(2, motorSpeed2) : sendMotorCommand(1, motorSpeed1);
        secondMotor = !secondMotor; // Switch to the other motor for the next cycle
        
        state = WAIT_ECHO;
        echoStart = millis();
      }
      break;

    case WAIT_ECHO:
      if (millis() > echoStart + 100) {
        // Timeout. Resend command and move on worriedly.
        mySerial.write(prevMessage.c_str());
        state = WAIT_PROMPT;
      }
      checkPrompt(my_buffer);
      if(my_buffer[0] != 'M') {
        my_buffer.remove(0,1); // Clear out noise
      } else {
        // First letter is 'M'. Check if the buffer contains the message that we expect to be echoed back
        if (my_buffer.substring(0, 8) == prevMessage) {
          // Yay success! move on happily.
          state = WAIT_PROMPT;
        } else {
          // Oops, this is noise. 
          my_buffer.remove(0,1); // Clear out noise
        }
        
      }
        
      break;
  }

}

bool checkPrompt(String buf) {
  if (mySerial.available()) {
    char recv = mySerial.read();
    if (recv == '?') return true;
    buf += String(recv);
    Serial.println("checking buffer...");
    Serial.println(buf);
    Serial.println("checked buffer...");
  }
  return false;
}

int getMotorSpeed(int motorNumber) {
  int rawForward = analogRead(0);
  int rawTurn = analogRead(1);
  Serial.print("Raw Forward/Backward: ");
  Serial.println(rawForward);
  Serial.print("Raw Turn: ");
  Serial.println(rawTurn);
  return mapInputToMotor(motorNumber, rawForward, rawTurn);
}

int mapInputToMotor(int motorNumber, int rawForward, int rawTurn) {
  // TODO: implement mapping from raw input to motor speed.
  // Subtract Offset:
  rawForward -= 511; // how much backward
  rawTurn -= 511; // how much to the right

  int motorOutput = 0;
  int totalPower = 0;
  if (motorNumber == 1) {
    // Left Motor: 
    totalPower = rawTurn - rawForward;
  } else {
    // Right Motor:
    totalPower = rawTurn - rawForward;
  }
  
  int sign = 1;
  if(totalPower < 0) {
    sign = -1;
    totalPower = -totalPower;
  }
  motorOutput = (totalPower - 26)/51;
  if (motorOutput < 0) motorOutput = 0;
  if (motorOutput > 9) motorOutput = 9;
  return sign * motorOutput;
  // return (motorNumber == 1 ? 9 : -9);
}

void sendMotorCommand(int motorNumber, int motorSpeed) {
  // Error Checking
  if (motorNumber < 1 || motorNumber > 2) return;
  if (motorSpeed <= -10 || motorNumber >= 10) return;

  // Generate Motor Command
  String command = "";
  command += "M";
  command += (motorNumber == 1 ? "1" : "2");
  command += " ";
  command += (motorSpeed < 0 ? "-" : "+");
  command += String(abs(motorSpeed));
  command += " ";

  //Checksum Calculations
  char checksum[2];
  calc_robotcmd_chksum(command.c_str(), ROBOTCMDLEN, checksum);

  // Add Checksum to Motor Command
  command += String(checksum[0]);
  //Serial.println(checksum[0]);
  //Serial.println(checksum[1]);
  command += String(checksum[1]);

  // Send Command Through Serial
  mySerial.write(command.c_str());
  Serial.println(command.c_str());
  prevMessage = command;

}

unsigned char tohex(byte x) // convert nibble value to hex-ascii char
{
  x &= 0x0f;
  if (x < 10) return (x + '0');
  return (x - 10 + 'A');
}

void calc_robotcmd_chksum(unsigned char cbuf[], int cbuflen, unsigned char cksum[] )
{
  // cbuf: array of chars holding the received robot command
  // cbuflen: length of chars with which to calculate checksum
  // cksum: array of chars to hold checksum as hex-ascii

  byte hexsum = 0;                // variable to calc checksum
  for (int i = 0; i < cbuflen; i++) {
    hexsum ^= cbuf[i];
  }

  // save calculated checksum as hex-ascii for comparison and validation
  // NOTE: use of hex-ascii is easier to view and debug via Serial Monitor
  cksum[0] = tohex((hexsum >> 4) & 0x0f);
  cksum[1] = tohex(hexsum & 0x0f);
}

