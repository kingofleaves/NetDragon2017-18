#define PIN_LED 2

String my_buffer;
String currMessage; 
String previousMessage; 

long nextEvent, shortIntv, longIntv; // Time between blinks

bool waitForBuffer;

bool newMessage; // new message sent
bool isLit; // LED on or off
int blinksLeft; // No. of blinks left

void setup() {
  Serial.begin(9600);
  pinMode(PIN_LED, OUTPUT);
  my_buffer = "";
  currMessage = "";
  previousMessage = "";
  nextEvent = millis();
  shortIntv = 250;
  longIntv = 1000;
  waitForBuffer = true;
  newMessage = true;
  bool isLit = false;
  blinksLeft = 0; 
}

void loop() {
  if(Serial.available()) {
    my_buffer = Serial.readString();
    Serial.println(my_buffer);
  }
  processMessage();
}

void processMessage() { 

  if (waitForBuffer) {
    if(isBufferValid()) {
      currMessage = my_buffer;
      previousMessage = String(my_buffer + "");
      newMessage = true;
      waitForBuffer = false;
      Serial.print("Message Valid!: ");
      Serial.println(my_buffer);      
    }
    my_buffer = "";
    return;
  }

  if (nextEvent > millis()) return; // Timer for our actions

  if (blinksLeft > 0) { 
    // If still blinking
    Serial.println("blinking...");
    if(isLit) {
      // Done with one blink. Reduce blink counter. 
      lightLED(false);
      blinksLeft -= 1;        
      if (blinksLeft == 0) {
        // All blinks of a digit end, send long pause between sequences.
        nextEvent = millis() + longIntv; 
      } else {
        // While handling blinks, send small pause between digits.
        nextEvent = millis() + shortIntv;
      } 
    } else {
      // Keep LED blinking
      lightLED(true);
      nextEvent = millis() + shortIntv;
    }
    return;
  }

  // Decide whether we are at the start of a message or the start of a digit when LED is off.
  
  if(!isLit) {
    if(newMessage) {
      // LED is off and we have a new message. Run start sequence and turn off newMessage flag.
      Serial.println((newMessage ? "new message!" : "" ));
      lightLED(true);
      nextEvent = millis() + longIntv;
      newMessage = false;
    } else {
      // LED is off and we are in the middle of a message. Send the next digit.
      if (currMessage =="") {
        // No more digits left to send.
        waitForBuffer = true;
        if(!isBufferValid()) {
        // If no new message, repeat previous message.
          Serial.print("Repeating old message: ");
          Serial.println(previousMessage);
          my_buffer = previousMessage;
        }
        return;
      }
      // If still have digits left to send, send the next digit.
      blinksLeft = nextDigit();
    }
  } else {
    // Keep LED off and send long pause.
    lightLED(false);
    nextEvent = millis() + longIntv;
  }

}

void lightLED(bool state) { // LED on or off
  digitalWrite(PIN_LED, (state ? HIGH : LOW));
  isLit = state;
}

bool isBufferValid() { // Checks if the message contains only numbers
  if (my_buffer == "") return false;
  for(char i=0;i<my_buffer.length();i++)
   {
      if(!isDigit(my_buffer.charAt(i))) return false;
   }
   return true;
}

int nextDigit() {
  Serial.println("getting next digit...");
  Serial.print("next digit is: ");
  int temp = currMessage[0]-'0';  
  currMessage.remove(0, 1);
  Serial.println(temp);
  Serial.println("remaining string:");
  Serial.println(currMessage);
  return temp;
}

