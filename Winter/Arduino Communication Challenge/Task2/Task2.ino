#include <SoftwareSerial.h>

#define ROBOTCMDLEN    6    // "MD +N "

SoftwareSerial mySerial(9, 10); // RX, TX
String my_buffer = "";

typedef enum {
  WAIT_PROMPT, WAIT_ECHO
} States_t;

States_t state = WAIT_PROMPT;

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
        sendMotorCommand(1, motorSpeed1);
        //sendMotorCommand(2, motorSpeed2);
      }
      break;

    case WAIT_ECHO:

      break;
  }

}

bool checkPrompt(String buf) {
  if (mySerial.available()) {
    char recv = mySerial.read();
    Serial.print(recv);
    if (recv == '?') return true;
    buf += String(recv);
  }
  return false;
}

int getMotorSpeed(int motorNumber) {
  int rawForward = analogRead(0);
  int rawTurn = analogRead(1);
  return mapInputToMotor(motorNumber, rawForward, rawTurn);
}

int mapInputToMotor(int motorNumber, int rawForward, int rawTurn) {
  // TODO: implement mapping from raw input to motor speed.
  return (motorNumber == 1 ? 5 : -5);
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

