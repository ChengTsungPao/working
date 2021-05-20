#include <Arduino.h>
// #include "pitches.h"

// ColorChange.ino
// 4105054025、鄭琮寶

// 使用陣列定義顏色對應碼
const byte array_black[3] = {0,0,0};
const byte array_green[3] = {0,255,0};
const byte array_indigo[3] = {75,0,130}; 

// 宣告變數
const byte Red = 7;
const byte Green = 6;
const byte Blue = 5;
const int MaintainTime = 2000; // 維持時間
const int TurnTime = 3000;     // 轉換時間
byte light1[3]; // 定義陣列變數, 作為儲存目前顏色對應碼的變數
byte light2[3]; // 定義陣列變數, 作為儲存漸變顏色對應碼的變數
int counter;
byte index;

void setup() {
	pinMode(Red, OUTPUT);
	pinMode(Green, OUTPUT);
	pinMode(Blue, OUTPUT);

}

void loop() {
	subgreen();
	ChangeColor();
	subindigo();
	ChangeColor();
	subblack();
	ChangeColor();
}

// 設定讀取顏色對應碼的副程式,將指定顏色陣列值存到light陣列變數裡

void subblack(){ // 將light變數setup成指定的顏色的色碼
	for(index=0;index<3;index++){
		light1[index]=light2[index];
		light2[index]=array_black[index];
	}
}

void subgreen(){ // 將light變數setup成指定的顏色的色碼
	for(index=0;index<3;index++){ 
		light1[index]=light2[index];
		light2[index]=array_green[index];
	}
}

void subindigo(){ // 將light變數setup成指定的顏色的色碼
	for(index=0;index<3;index++){ 
		light1[index]=light2[index];
		light2[index]=array_indigo[index];
	}
}

void ChangeColor(){ // 副程式使led動作, 轉變顏色 
	for(counter=1;counter<=(TurnTime/12);counter++){
		// 為了避免因為duty為0%造成亮度轉變時產生的閃爍現象,因此若value=0時,則跳過不予呈現
		if(map(counter,0,TurnTime/12,0,light2[0])!=0){ 
			analogWrite(Red,map(counter,0,TurnTime/12,0,light2[0])); 
			delay(2);
		}
		if(map(TurnTime/12-counter,0,TurnTime/12,0,light1[1])!=0){ 
			analogWrite(Green,map(TurnTime/12-counter,0,TurnTime/12,0,light1[1]));
			delay(2);
		} 
		if(map(counter,0,TurnTime/12,0,light2[2])!=0){ 
			analogWrite(Blue,map(counter,0,TurnTime/12,0,light2[2]));
			delay(2);
		} 
		if(map(TurnTime/12-counter,0,TurnTime/12,0,light1[0])!=0){ 
			analogWrite(Red,map(TurnTime/12-counter,0,TurnTime/12,0,light1[0])); 
			delay(2);
		} 
		if(map(counter,0,TurnTime/12,0,light2[1])!=0){ 
			analogWrite(Green,map(counter,0,TurnTime/12,0,light2[1]));
			delay(2); 
		} 
		if(map(TurnTime/12-counter,0,TurnTime/12,0,light1[2])!=0){ 
			analogWrite(Blue,map(TurnTime/12-counter,0,TurnTime/12,0,light1[2])); 
			delay(2);
		}
	}
	for(counter=1;counter<=MaintainTime/6;counter++){ 
		analogWrite(Red,light2[0]);
		delay(2);
		analogWrite(Green,light2[1]);
		delay(2);
		analogWrite(Blue,light2[2]);
		delay(2);
	}
}