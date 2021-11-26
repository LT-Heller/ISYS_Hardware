#define LITE
#ifdef LITE
#include <Arduino.h>

void setup(){
    Serial.begin(2000000);
    pinMode(A0, INPUT);
    pinMode(A1, INPUT);
    pinMode(A2, INPUT);
    pinMode(A3, INPUT);
}

void loop(){
    if(true){
        Serial.print(analogRead(A0));
        Serial.print('\t');
        Serial.print(analogRead(A1));
        Serial.print('\t');
        Serial.print(analogRead(A2));
        Serial.print('\t');
        Serial.print(analogRead(A3));
        Serial.print('\n');
    }
    else{
        Serial.write(analogRead(A0));
        Serial.write('\t');
        Serial.write(analogRead(A1));
        Serial.write('\t');
        Serial.write(analogRead(A2));
        Serial.write('\t');
        Serial.write(analogRead(A3));
        Serial.write('\n');
    }
    delay(4);
}
#endif