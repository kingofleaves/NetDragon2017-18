#define PIN_EN_L 11
#define PIN_IN1_L 12
#define PIN_IN2_L 13

#define PIN_EN_L 10
#define PIN_IN1_L 9
#define PIN_IN2_L 8



void setup() {
  // put your setup code here, to run once:
  pinMode(PIN_POWER, OUTPUT);
  pinMode(PIN_GND, OUTPUT);  
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(PIN_POWER, HIGH);
  digitalWrite(PIN_GND, LOW);  
}
