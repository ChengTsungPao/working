// DoReMiFaSolLaTiDo.ino
// Send an octave of half second tones using a piezoelectric speaker.
// 4105054025、鄭琮寶

const byte SP_PIN = 9;
int duration = 500;

void setup() {
	pinMode(SP_PIN, OUTPUT);
	Serial.begin(9600);

}

void loop() {
	Serial.println("Do...");
	tone(SP_PIN, 1047 * 2); delay(duration); noTone(SP_PIN); delay(duration); // C6
	Serial.println("Do#...");
	tone(SP_PIN, 1109 * 2); delay(duration); noTone(SP_PIN); delay(duration); // C6#

	Serial.println("Re...");
	tone(SP_PIN, 1175 * 2); delay(duration); noTone(SP_PIN); delay(duration); // D6 
	Serial.println("Re#...");
	tone(SP_PIN, 1245 * 2); delay(duration); noTone(SP_PIN); delay(duration); // D6#

	Serial.println("Mi...");
	tone(SP_PIN, 1319 * 2); delay(duration); noTone(SP_PIN); delay(duration); // E6

	Serial.println("Fa...");
	tone(SP_PIN, 1396 * 2); delay(duration); noTone(SP_PIN); delay(duration); // F6 
	Serial.println("Fa...");
	tone(SP_PIN, 1480 * 2); delay(duration); noTone(SP_PIN); delay(duration); // F6#

	Serial.println("Sol...");
	tone(SP_PIN, 1568 * 2); delay(duration); noTone(SP_PIN); delay(duration); // G6
	Serial.println("Sol...");
	tone(SP_PIN, 1661 * 2); delay(duration); noTone(SP_PIN); delay(duration); // G6#

	Serial.println("La...");
	tone(SP_PIN, 1760 * 2); delay(duration); noTone(SP_PIN); delay(duration); // A6 
	Serial.println("La...");
	tone(SP_PIN, 1865 * 2); delay(duration); noTone(SP_PIN); delay(duration); // A6#

	Serial.println("Ti...");
	tone(SP_PIN, 1976 * 2); delay(duration); noTone(SP_PIN); delay(duration); // B6
	Serial.println("Do...");
	tone(SP_PIN, 2093 * 2); delay(duration); noTone(SP_PIN); delay(duration); // C7
	for(;;);

}

