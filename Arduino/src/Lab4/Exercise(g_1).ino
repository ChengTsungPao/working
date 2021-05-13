// SelectCaseWithValues.ino
// Enter a value and see the minimum variable size required to hold it.
// 4105054025、鄭琮寶

unsigned int value;
int var;
byte keyin;

void setup() {
	Serial.begin(9600);

}

void loop() {
	Serial.print("Enter a value from ");
	Serial.println("0 to 65535");
	value = 0;
	while(Serial.available() == 0){}
	keyin = Serial.read();
	while(keyin != '\n'){
		if(keyin >= '0' && keyin <= '9'){
			value = value * 10 + (keyin - '0');
		}
		keyin = Serial.read();
	}
	Serial.print("value = ");
	Serial.println(value, DEC);

	var = decide(value);
	switch(var){
		case 0:
			Serial.println("boolean");
			break;
		case 1:
			Serial.println("byte");
			break;
		case 2:
			Serial.println("int");
			break;
		case 3:
			Serial.println("unsigned int");
			break;
		default:
			Serial.println("Error number !");
			break;
	}

}

int decide(unsigned int number){
	if(number <= 1){
		var = 0;
	}else if(value >= 2 && value <= 255){
		var = 1;
	}else if(value >= 256 && value <= 32767){
		var = 2;
	}else if(value >= 32768 && value <= 65535){
		var = 3;
	}else{
		var = 4;
	}
	return var;

}



