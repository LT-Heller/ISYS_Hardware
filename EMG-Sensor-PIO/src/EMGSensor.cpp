#include <Arduino.h>
#include <FlexiTimer2.h>

#define FREQ  1000.0
#define SAMPLING_DELAY 1.0/FREQ // [ms]

void sample_data()
{
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
        Serial.write(0xAA);
        Serial.write(0xAA);
        for(unsigned char CurrentCh=0;CurrentCh<4;CurrentCh++){
        ADC_Value = analogRead(CurrentCh);
        Serial.write((unsigned char)((ADC_Value & 0xFF00) >> 8));
        Serial.write((unsigned char)(ADC_Value & 0x00FF));
        }
    }
}

void setup(){
    noInterrupts();

    Serial.begin(2000000);

    pinMode(A0, INPUT);
    pinMode(A1, INPUT);
    pinMode(A2, INPUT);
    pinMode(A3, INPUT);

    FlexiTimer2::set(1, SAMPLING_DELAY, sample_data);
    FlexiTimer2::start();

    interrupts();
}

void loop()
{
    __asm__ __volatile__ ("sleep");
}