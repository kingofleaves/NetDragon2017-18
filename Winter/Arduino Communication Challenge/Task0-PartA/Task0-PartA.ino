#define PIN_LED 2

String my_buffer;
String currMessage;
String previousMessage; 

long nextEvent, shortIntv, longIntv; // Time between blinks

bool waitForBuffer;

bool newMessage;  
bool isLit; 
int blinksLeft; // No. of blinks left

void setup() {
  // put your setup code here, to run once:
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
  // put your main code here, to run repeatedly:
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

  if (nextEvent > millis()) return; // timer for our actions

  if (blinksLeft > 0) {
    // blinking
    Serial.println("blinking...");
    // 
    if(isLit) {
      lightLED(false);
      blinksLeft -= 1;        
      if (blinksLeft == 0) {
        // All blinks of a digit end
        nextEvent = millis() + longIntv; 
      } else {
        // When still handling blinks
        nextEvent = millis() + shortIntv;
      } 
    } else {
      lightLED(true);
      nextEvent = millis() + shortIntv;
    }
    return;
  }

  // Decide whether we are at the start of a message or the start of a digit
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
        // no more digits left to send.
        waitForBuffer = true;
        if(!isBufferValid()) {
          Serial.print("Repeating old message: ");
          Serial.println(previousMessage);
          my_buffer = previousMessage;
        }
        return;
      }
      blinksLeft = nextDigit();
    }
  } else {
    // LED is on. Turn it off.
    lightLED(false);
    nextEvent = millis() + longIntv;
  }

}

void lightLED(bool state) {
  digitalWrite(PIN_LED, (state ? HIGH : LOW));
  isLit = state;
}

bool isBufferValid() {
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

