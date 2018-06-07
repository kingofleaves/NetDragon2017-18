#define BUFFER_SIZE 100
#define MIC_BIAS 0
#define MIC_THRESHOLD 10

int memAudio[BUFFER_SIZE];
long lastPoll = 0;
long lastMsg = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  memset(memAudio, 0, sizeof(int) * BUFFER_SIZE);
}

void loop() {

  // if(millis() - lastPoll > 100) {

    int magVal = 0; // Stores magnitude of the next normalized reading

    while(millis() - lastPoll < 500) { // detects speech for 0.5s. 
      // Read raw value from Analog Pin to Mic
      int rawVal = analogRead(0);
      
      // Serial.println(rawVal);
      // Normalize DC Bias
      int normVal = rawVal - MIC_BIAS;
      // get Magnitude and store it if it's bigger than previous iteration.
      magVal = max(magVal, abs(normVal));
      // Print for Debugging
      // Serial.print("Normalized Mic Value: ");
      // Serial.println(normVal);
    }
    // Move all data in buffer back by one unit 
    memmove(memAudio, memAudio + 1, sizeof(int) * (BUFFER_SIZE - 1));
    // Store new value in buffer
    memAudio[BUFFER_SIZE - 1] = (abs(magVal) > MIC_THRESHOLD ? 1 : 0);
  
    // Send average speaking time to RPi
    int speakTime = 0;
    for (int i = BUFFER_SIZE - 1; i < BUFFER_SIZE; i++) {
      speakTime += memAudio[i];
    }
    
    //Serial.print("speaking time; ");
    // TRY PRINTING THIS LESS?
    Serial.println(speakTime); 

    lastPoll = millis();
  //}
  
}


