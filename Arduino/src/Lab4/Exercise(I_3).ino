// SevenColor.ino
// 4105054025、鄭琮寶

const byte Red = 7;
const byte Green = 6;
const byte Blue = 5;

void setup() {
	pinMode(Red, OUTPUT);
	pinMode(Green, OUTPUT);
	pinMode(Blue, OUTPUT);

}

void loop() {
	for(int counter = 0; counter < 400; counter++){ // White
		analogWrite(Red, 255);
		delay(1);
		analogWrite(Green, 255);
		delay(1);
		analogWrite(Blue, 255);
		delay(1);
	}
	for(int counter = 0; counter < 400; counter++){ // Black
		analogWrite(Red, 0);
		delay(1);
		analogWrite(Green, 0);
		delay(1);
		analogWrite(Blue, 0);
		delay(1);
	}
	for(int counter = 0; counter < 400; counter++){ // Red
		analogWrite(Red, 255);
		delay(1);
		analogWrite(Green, 0);
		delay(1);
		analogWrite(Blue, 0);
		delay(1);
	}
	for(int counter = 0; counter < 400; counter++){ // Orange
		analogWrite(Red, 255);
		delay(1);
		analogWrite(Green, 165);
		delay(1);
		analogWrite(Blue, 0);
		delay(1);
	}
	for(int counter = 0; counter < 400; counter++){ // Yellow
		analogWrite(Red, 255);
		delay(1);
		analogWrite(Green, 255);
		delay(1);
		analogWrite(Blue, 0);
		delay(1);
	}
	for(int counter = 0; counter < 400; counter++){ // Green
		analogWrite(Red, 0);
		delay(1);
		analogWrite(Green, 255);
		delay(1);
		analogWrite(Blue, 0);
		delay(1);
	}
	for(int counter = 0; counter < 400; counter++){ // Blue
		analogWrite(Red, 0);
		delay(1);
		analogWrite(Green, 0);
		delay(1);
		analogWrite(Blue, 255);
		delay(1);
	}
	for(int counter = 0; counter < 400; counter++){ // Indigo
		analogWrite(Red, 75);
		delay(1);
		analogWrite(Green, 0);
		delay(1);
		analogWrite(Blue, 130);
		delay(1);
	}
	for(int counter = 0; counter < 400; counter++){ // Purple
		analogWrite(Red, 128);
		delay(1);
		analogWrite(Green, 0);
		delay(1);
		analogWrite(Blue, 128);
		delay(1);
	}

}
