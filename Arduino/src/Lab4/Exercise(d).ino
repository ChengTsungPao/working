// TwinkleTwinkle.ino
// Play the first seven notes from Twinkle Twinkle Little Star.
// 4105054025、鄭琮寶

#include "pitches.h"

const byte SP_PIN = 9;
char* Notes[] = {"C7","C7","G7","G7","A7","A7","G7","F7","F7","E7","E7","D7","D7","C7"};
int Frequencies[] = {NOTE_C7, NOTE_C7, NOTE_G7, NOTE_G7, NOTE_A7, NOTE_A7, NOTE_G7, NOTE_F7, NOTE_F7, NOTE_E7, NOTE_E7, NOTE_D7, NOTE_D7, NOTE_C7}; 
int Durations[] = {500, 500, 500, 500, 500, 500, 1000, 500, 500, 500, 500, 500, 500, 1000};

byte index;
int noteFreq;
int noteDuration;

void setup() {
	pinMode(SP_PIN, OUTPUT);
	Serial.begin(9600);

}

void loop() {
	Serial.println("Note Duration Frequency");
	Serial.println("---- ------- ----------");
	for(index = 0; index <= 13; index++){
		Serial.print(Notes[index]);
		noteDuration = Durations[index];
		Serial.print(" noteDuration= "); Serial.print(noteDuration, DEC);
		noteFreq = Frequencies[index];
		Serial.print(" noteFreq= "); Serial.println(noteFreq,DEC);
		tone(SP_PIN, noteFreq);
		delay(noteDuration);
		noTone(SP_PIN);
	}
	for(;;);

}

