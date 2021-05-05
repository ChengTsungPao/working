// ActionTones.ino
// Send a tone to the piezo speaker using the tone() command.
// 4105054025、鄭琮寶

const byte SP_PIN = 9;
int duration;
int frequency;

void setup() {
	pinMode(SP_PIN, OUTPUT);
	Serial.begin(9600);

}

void loop() {
	Serial.println("Alarm...");
	delay(500);
	tone(SP_PIN, 1500, 500);
	delay(500);
	tone(SP_PIN, 1500, 500);
	delay(500); 
	tone(SP_PIN, 1500, 500); 
	delay(500);
	tone(SP_PIN, 1500, 500); 
	delay(500);

	Serial.println("Robot replay...");
	delay(100);
	tone(SP_PIN, 2800);
	delay(100);
	noTone(SP_PIN);
	tone(SP_PIN, 2400);
	delay(200);
	noTone(SP_PIN);
	tone(SP_PIN, 4200);
	delay(140);
	noTone(SP_PIN);
	tone(SP_PIN, 2000);
	delay(30);
	noTone(SP_PIN);
	delay(500);

	Serial.println("Hyperspace...");
	delay(100);
	for(duration = 15; duration >= 1; duration--){
		for(frequency = 2000; frequency <= 2500; frequency += 20){
			tone(SP_PIN, frequency);
			delay(duration);
			noTone(SP_PIN);
		}
	}

	Serial.println("Hyperspace jump..."); // 題目要求的修正
	for(duration = 15; duration >= 1; duration -= 3){
		for(frequency = 2000; frequency <= 2500; frequency += 15){
			tone(SP_PIN, frequency);
			delay(duration);
			noTone(SP_PIN);
		}
	}
	for(duration = 1; duration <= 36; duration += 3){
		for(frequency = 2500; frequency >= 2000; frequency -= 15){
			tone(SP_PIN, frequency);
			delay(duration);
			noTone(SP_PIN);
		}
	}

	Serial.println("Done");
	for(;;);

}
