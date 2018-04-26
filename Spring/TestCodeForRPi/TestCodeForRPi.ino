void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  // Serial.println(sizeof(float)); 
  delay(500);
  Serial.println(120643);
  delay(500);
  Serial.println(1.2);
  delay(500);
  Serial.println(0.000000012,10);
}

//byte sendBytes(auto f) {
//  byte *bytes_p = (byte *) &f;
//  Serial.write(bytes_p, sizeof(f));
//  Serial.write('\n');
//}

