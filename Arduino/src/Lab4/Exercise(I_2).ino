// PWMTest.ino
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
	analogWrite(Green, 255); // 100% 亮為 255 = 255 * 1
	delay(500);
	analogWrite(Green, 191); //  75% 亮為 191 = 255 * 0.75
	delay(500);
	analogWrite(Green, 128); //  50% 亮為 128 = 255 * 0.50
	delay(500);
	analogWrite(Green, 64);  //  25% 亮為  64 = 255 * 0.25
	delay(500);
	analogWrite(Green, 0);   //   0% 亮為   0 = 255 * 0
	delay(500);
}
