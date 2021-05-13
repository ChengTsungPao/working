// NotesAndDurations.ino
// Play the first few notes from Frere Jacques.
// 4105054025、鄭琮寶

#include "pitches.h"

const byte SP_PIN = 9;
char* Notes[] = {"C7","D7","E7","C7","C7","D7","E7","C7","E7","F7","G7","E7","F7","G7","Q"};
char* Notes_table[] = {"A6","b6","B6","C7","d7","D7","e7","E7","F7","g7","G7","a7","P","Q"};
int Frequencies[] = {NOTE_A6, NOTE_AS6, NOTE_B6, NOTE_C7, NOTE_CS7, NOTE_D7, NOTE_DS7, NOTE_E7, NOTE_F7, NOTE_FS7, NOTE_G7, NOTE_GS7, 0, 0};
byte Durations[] = {4,4,4,4,4,4,4,4,4,4,2,4,4,2};

const int WholeNote = 1750; // 改成 1500 1750 2000 2250
byte index = 0;
byte offset;
int noteFreq;
int noteDuration;

void setup() {
	pinMode(SP_PIN, OUTPUT);
	Serial.begin(9600);

}

void loop() {
	Serial.println("Program Runngin!");
	while(Notes[index] != "Q"){ 
		offset = 0;
		while(1){ 
			if(Notes_table[offset] == Notes[index]){
				break;
			}
			offset++;
		}
		noteDuration = Durations[index];
		noteFreq = Frequencies[offset];
		noteDuration = WholeNote / noteDuration;
		Serial.println(offset, DEC);
		Serial.println(noteFreq, DEC);
		if(noteFreq >= 3){
			tone(SP_PIN, noteFreq);
		}
		Serial.println(noteDuration, DEC);
		delay(noteDuration);
		noTone(SP_PIN);
		index++;
	}
	for(;;);

}



