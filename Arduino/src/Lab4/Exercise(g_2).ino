// SelectCaseWithCharacters.ino
// Program that can identify some characters: case, digit, punctuation, Special character.
// 4105054025、鄭琮寶

byte character;

void setup() {
	Serial.begin(9600);

}

void loop() {
	Serial.print("Enter a character: ");
	character = 0;
	while(Serial.available() == 0){}
	character = Serial.read();
	Serial.print("character = ");
	Serial.println(character);
	switch(character){
		case 'A'...'Z':
			Serial.println("Upper case");
			break;
		case 'a'...'z':
			Serial.println("Lower case");
			break;
		case '0'...'9':
			Serial.println("Digit");
			break;
		case '!':
		case '?':
		case '.':
		case ',':
			Serial.println("Punctuation");
			break;
		case '@':
		case '#':
		case '$':
		case '%':
		case '^':
		case '&':
		case '(':
		case ')':
		case '-':
		case '+':
			Serial.println("Special character");
			break;		
		default:
			Serial.println("character not know.");
			Serial.println("Try a different one.");
			break;
	}

}
