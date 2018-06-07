#include<FastLED.h>
#define NUM_LEDS 3

CRGBArray<NUM_LEDS> leds;
long lastEventTime = 0;
int sweepCount = 0;

#define OUR_RED CHSV(0, 128, 200)
#define OUR_BLUE CHSV(100, 128, 150)
#define BREATHE_INTV 750 //(not used)
#define SWEEP_INTV 900
#define METER_INTV 600

CHSV currColor = CHSV(0,0,0); 
int h = 1000;
bool fadeIn = true;


enum LEDstate { STOP, BREATHE_R, SWEEP_R, METER_R, BREATHE_B, SWEEP_B, METER_B};
LEDstate currState;

void setup() { 
  Serial.begin(9600);
  FastLED.addLeds<NEOPIXEL,6>(leds, NUM_LEDS); 
  currState = STOP;
}

void loop(){ 
//  if(Serial.available()) {
//    String c = Serial.readString();
//    h = c.toInt();
//  }
//  CHSV hsv = CHSV(100, 128, 200); 
//  breathe(hsv, h);

  checkSerial();
  switch(currState) {
    case STOP:
      turnOff();
      break;
    case BREATHE_R:
      breathe(OUR_RED, BREATHE_INTV);
      break;
    case SWEEP_R:
      sweep(OUR_RED, SWEEP_INTV);
      break;
    case METER_R:
      meter(OUR_RED, METER_INTV);
      break;  
    case BREATHE_B:
      breathe(OUR_BLUE, BREATHE_INTV);
      break;
    case SWEEP_B:
      sweep(OUR_BLUE, SWEEP_INTV);
      break;
    case METER_B:
      meter(OUR_BLUE, METER_INTV);
      break;       
  }
}

void checkSerial() {
  if(Serial.available()) {
    // Reset Variables
    reset();

    // Respond to Serial
    char c = Serial.read();
    switch(c) {
      case '0':
        currState = STOP;
        break;
      case '1':
        currState = BREATHE_B;
        break;        
      case '2':
        currState = SWEEP_B;
        break;
      case '3':
        currState = METER_B;
        break;
      case '4':
        currState = BREATHE_R;
        break;        
      case '5':
        currState = SWEEP_R;
        break;
      case '6':
        currState = METER_R;
        break;
    }
  }
}

void reset(){
  currColor = CHSV(currColor.hue, currColor.sat, 0);
  fadeIn = true;
  sweepCount = 0;
  for(int i = 0; i < NUM_LEDS; i++) {   
    // fade everything out
    leds[i] = CRGB::Black;
  }
  FastLED.show();
}

void turnOff(){
  for(int i = 0; i < NUM_LEDS; i++) {   
    // fade everything out
    leds.fadeToBlackBy(40);
    FastLED.show();
  }
}

void breathe(CHSV hsvColor, long time_intv) {
  // fade everything out
  //    leds.fadeToBlackBy(20000/time_intv);
  if(fadeIn) {
    currColor = CHSV(hsvColor.hue, hsvColor.sat, currColor.val + 3);
    if (currColor == hsvColor) {
      fadeIn = false;
    }
  }
  else{
    currColor = CHSV(hsvColor.hue, hsvColor.sat, currColor.val - 3);
    if (currColor.val < 30) {
      fadeIn = true;
    }  
  }
  
  for(int i = 0; i < NUM_LEDS; i++) {   
    leds[i] = currColor;
  }
  
  FastLED.show();
  FastLED.delay(30);

//  if (millis() - lastEventTime >= time_intv) {   
//    // let's set an led value
//    for(int i = 0; i < NUM_LEDS; i++) {   
//      leds[i] = currColor;
//    }
//    FastLED.show();
//    delay(time_intv/2);
//    lastEventTime = millis();
//  }
}

void sweep(CHSV hsvColor, long time_intv) {
  for(int i = 0; i < NUM_LEDS; i++) {   
    // fade everything out
    leds.fadeToBlackBy(20000/time_intv);

    FastLED.delay(50);
  }

  if (millis() - lastEventTime >= time_intv/3) {   
    leds[sweepCount++] = hsvColor;
    if(sweepCount >= NUM_LEDS) sweepCount = 0;
    FastLED.show();
    lastEventTime = millis();
  }
}

void meter(CHSV hsvColor, long time_intv) {
    if(sweepCount >= NUM_LEDS) {
      if(currColor.val > 2) {
        currColor = CHSV(currColor.hue, currColor.sat, currColor.val -3);   
      }
      else {
        currColor.val = 0;
      }
      for(int i = 0; i < NUM_LEDS; i++) {   
        leds[i] = currColor;
      }
      FastLED.show();
      delay(20);
      
//      for (int i = 0; i < NUM_LEDS; i++) {
//        leds[i] = CRGB::Black;
//      }
    } else {
      if (millis() - lastEventTime >= time_intv/4) {   
        currColor = hsvColor;
        leds[sweepCount++] = hsvColor;   
        FastLED.show();
        lastEventTime = millis();
      }
    }
}

