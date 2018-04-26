#define BUFFER_SIZE 100
#define MIC_THRESHOLD 100

int memAudio[BUFFER_SIZE];


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  memset(memAudio, 0, sizeof(int) * BUFFER_SIZE);
}

void loop() {
  // Read raw value from Analog Pin to Mic
  int rawVal = analogRead(0);
  // Normalize DC Bias
  int normVal = rawVal - 526;
  // Print for Debugging
  // Serial.print("Normalized Mic Value: ");
  // Serial.println(normVal);
  // Move all data in buffer back by one unit 
  memmove(memAudio, memAudio + 1, sizeof(int) * (BUFFER_SIZE - 1));
  // Store new value in buffer
  memAudio[BUFFER_SIZE - 1] = (abs(normVal) > MIC_THRESHOLD ? 1 : 0);

  // Send average speaking time to RPi
  int speakTime = 0;
  for (int i = 0; i < BUFFER_SIZE; i++) {
    speakTime += memAudio[i];
  }
  Serial.print("speaking time; ");
  Serial.println(speakTime);
  
}


