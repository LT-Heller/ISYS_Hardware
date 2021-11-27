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
    unsigned int ADC_Value = 0;
    if(false){
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
        for(unsigned char CurrentCh=0;CurrentCh<4;CurrentCh++){
        ADC_Value = analogRead(CurrentCh);
        Serial.write((unsigned char)((ADC_Value & 0xFF00) >> 8));
        Serial.write((unsigned char)(ADC_Value & 0x00FF));
        }
        //Serial.write('\t');
        //Serial.write(analogRead(A1));
        //Serial.write('\t');
        //Serial.write(analogRead(A2));
        //Serial.write('\t');
        //Serial.write(analogRead(A3));
        Serial.write('\n');
    }
    delay(2);
}
#endif