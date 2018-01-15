void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}

bool checkPrompt(String buf) {
  if (Serial.available()) {
    char recv = Serial.read();
    if (recv == '?') return true;
    buf.append(recv);
  }
  return false;
}

void sendMotorCommand(int motorNumber, int motorSpeed) {
  // Error Checking
  if (motorNumber < 1 || motorNumber > 2) return;
  if (motorSpeed <= -10 || motorNumber >= 10) return;
  
  //Checksum Calculations
  calc_robotcmd_chksum(unsigned char cbuf[], int cbuflen, unsigned char cksum[] );

  // Generate Motor Command
  String command = "";
  command += "M";
  command += (motorNumber == 1 ? "1" : "2");
  command += " ";
  command += (motorSpeed < 0 ? "-" : "+");
  command += String(motorSpeed);
  command += " ";
  command += String(checksum[0]);
  command += String(checksum[1]);  

  // Send Command Through Serial
  mySerial.write(command);
}

