// NestedLoops.ino
// 4105054025、鄭琮寶

byte A;
byte B;

void setup() {
	Serial.begin(9600);

}

void loop() {
	delay(100);
	for(A = 1; A <= 9; A++){
		for(B = 1; B <= 9; B++){
			Serial.print(B, DEC);
			Serial.print("*");
			Serial.print(A, DEC);
			Serial.print("=");
			if(A * B < 10){
				Serial.print(" ");	
			}
			Serial.print(A * B, DEC);
			Serial.print(" ");
		}
		Serial.print("\n");
	}
	for(;;);

}