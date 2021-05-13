// MusicWithMoreFeatures.ino
// Play the beginning of For He's a Jolly Good Fellow.
// 4105054025、鄭琮寶

#include "pitches.h"

char* Notes[] = {"C","C","A","G","E","G","D","P","C","C","A","G","E","G","Q"}; // 修改前 {"C","E","E","E","D","E","F","E","E","D","D","D","C","D","E","C","Q"};
byte Octaves[] = {6, 7, 6, 6, 6, 6, 6, 6, 6, 7, 6, 6, 6, 6}; // 修改前 {7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7};
byte Durations[] = {2, 4, 4, 4, 4, 2, 2, 4, 2, 4, 4, 4, 4, 2}; // 修改前 { 4, 2, 4, 4, 4, 4, 2, 2, 4, 2, 4, 4, 4, 4, 2, 2};
byte Dots[] = {0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1}; // 修改前 {0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0};

char* Notes_table[] = {"C", "d", "D", "e", "E", "F", "g", "G", "a", "A", "b", "B", "P", "Q"};
				   // {"C8","d8","D8","e8","ES", "F8","g8","G8","a8","A8","b8","B8","P","Q"}
int Frequencies[] = {4186, 4435, 4699, 4978, 5274, 5588, 5920, 6272, 6645, 7040, 7459, 7902, 0, 0}; //建立音符表頻率陣列,第八個八度音頻率範圍已超出 pitches.h 內容,故不使用

const byte SP_PIN = 9; 
const int BeatsPerMin = 240; // 修改前 320
byte index;
byte offset;
int noteFreq;
int noteDuration;
byte noteOctave; 
byte noteDot;
int WholeNote;

void setup() {
	pinMode(SP_PIN, OUTPUT);
	Serial.begin(9600);

}

void loop() {
	Serial.println("Program Runngin!");
	WholeNote = (60000 / BeatsPerMin) * 4;
	while(Notes[index] != "Q"){ 
		offset = 0;
		while(1){ 
			if(Notes_table[offset] == Notes[index]){
				break;
			}
			offset++;
		}
		noteOctave = Octaves[index];
		noteOctave = 8 - noteOctave;
		noteDuration = Durations[index];
		noteFreq = Frequencies[offset];
		noteFreq = noteFreq / pow(2, noteOctave);
		noteDuration = WholeNote / noteDuration;
		noteDot = Dots[index];
		if(noteDot == 1){
			noteDuration = noteDuration * 3 / (float)2;
		}
		if(noteFreq >= 31){
			tone(SP_PIN, noteFreq);
		}
		delay(noteDuration);
		noTone(SP_PIN);
		index++;
	}
	for(;;);

}



