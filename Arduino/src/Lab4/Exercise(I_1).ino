// ThreeColorTest.ino
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
	digitalWrite(Blue, HIGH);  // 亮 Blue
	delay(500);
	digitalWrite(Blue, LOW);   // 暗 Blue
	delay(500);
	digitalWrite(Green, HIGH); // 亮 Green
	delay(500);
	digitalWrite(Green, LOW);  // 暗 Green
	delay(500);
	digitalWrite(Red, HIGH);   // 亮 Red
	delay(500);
	digitalWrite(Red, LOW);    // 暗 Red
	delay(5000);

}
