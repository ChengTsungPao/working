// TestPiezoWithFreqout.ino
// Send a tone to the piezo speaker using the tone() command.
// 4105054025、鄭琮寶

const byte SP_PIN = 9;

void setup() {
	pinMode(SP_PIN, OUTPUT);
	Serial.begin(9600);

}

void loop() {
	Serial.println("Tone sending...");
	tone(SP_PIN, 3000, 1500); // frequence = [1500, 2000, 2500, 3000] 頻率越高聲音聽起來越尖銳
	delay(3000);
	Serial.println("Tone done.");

}
