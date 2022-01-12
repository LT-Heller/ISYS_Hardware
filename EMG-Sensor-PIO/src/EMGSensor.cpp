#include <Arduino.h>
#include <FlexiTimer2.h>

#define FREQ  1000.0 // [Samples pro Sekunde]
#define SAMPLING_DELAY 1.0/FREQ // [ms]

void sample_data()
{
    unsigned int ADC_Value = 0;
    // Startbytes
    Serial.write(0xAA);
    Serial.write(0xAA);
    // Datenbytes
    for(unsigned char CurrentCh=0;CurrentCh<4;CurrentCh++){
        ADC_Value = analogRead(CurrentCh);
        // Highbyte
        Serial.write((unsigned char)((ADC_Value & 0xFF00) >> 8));
        // Lowbyte
        Serial.write((unsigned char)(ADC_Value & 0x00FF));
    }
}

void setup(){
    noInterrupts();

    Serial.begin(2000000); // 2 Mbit/s

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