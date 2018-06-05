#include<FastLED.h>
#define NUM_LEDS 3
#define TIME_INTV 500

CRGBArray<NUM_LEDS> leds;
long lastEventTime = 0;
int sweepCount = 0;

#define OUR_RED CRGB::Red
#define OUR_BLUE CRGB(150, 255, 255)


enum LEDstate { STOP, CALL_R, SWEEP_R, METER_R, CALL_B, SWEEP_B, METER_B};
LEDstate currState;

void setup() { 
  Serial.begin(9600);
  FastLED.addLeds<NEOPIXEL,6>(leds, NUM_LEDS); 
  currState = STOP;
}

void loop(){ 
  checkSerial();

  switch(currState) {
    case STOP:
      turnOff();
      break;
    case CALL_R:
      callTeacher(OUR_RED);
      break;
    case SWEEP_R:
      sweep(OUR_RED);
      break;
    case METER_R:
      meter(OUR_RED);
      break;  
    case CALL_B:
      callTeacher(OUR_BLUE);
      break;
    case SWEEP_B:
      sweep(OUR_BLUE);
      break;
    case METER_B:
      meter(OUR_BLUE);
      break;       
  }
}

void checkSerial() {
  if(Serial.available()) {
    char c = Serial.read();
    switch(c) {
      case '0':
        currState = STOP;
        break;
      case '1':
        currState = CALL_R;
        break;        
      case '2':
        currState = SWEEP_R;
        break;
      case '3':
        currState = METER_R;
        break;
      case '4':
        currState = CALL_B;
        break;        
      case '5':
        currState = SWEEP_B;
        break;
      case '6':
        currState = METER_B;
        break;
    }
  }
}

void turnOff(){
  for(int i = 0; i < NUM_LEDS; i++) {   
    // fade everything out
    leds.fadeToBlackBy(40);
    FastLED.show();
  }
}

void callTeacher(CRGB rgbColor) {
  for(int i = 0; i < NUM_LEDS; i++) {   
    // fade everything out
    leds.fadeToBlackBy(40);

    FastLED.delay(20);
  }

  if (millis() - lastEventTime >= TIME_INTV) {   
    // let's set an led value
    for(int i = 0; i < NUM_LEDS; i++) {   
      leds[i] = rgbColor;
    }
    FastLED.show();
    delay(TIME_INTV/2);
    lastEventTime = millis();
  }
}

void sweep(CRGB rgbColor) {
  for(int i = 0; i < NUM_LEDS; i++) {   
    // fade everything out
    leds.fadeToBlackBy(40);

    FastLED.delay(20);
  }

  if (millis() - lastEventTime >= TIME_INTV/3) {   
    leds[sweepCount++] = rgbColor;
    if(sweepCount >= NUM_LEDS) sweepCount = 0;
    FastLED.show();
    lastEventTime = millis();
  }
}

void meter(CRGB rgbColor) {

  if (millis() - lastEventTime >= TIME_INTV/4) {   
    if(sweepCount >= NUM_LEDS) {
      sweepCount = 0;
      for (int i = 0; i < NUM_LEDS; i++) {
        leds[i] = CRGB::Black;
      }
    } else {
      leds[sweepCount++] = rgbColor;
    }
    FastLED.show();
    lastEventTime = millis();
  }
}

