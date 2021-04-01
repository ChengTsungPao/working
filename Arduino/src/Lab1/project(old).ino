
boolean status = 0;
boolean running = 0;
const byte Button = 10;
const byte LED_Y = 11;
const byte LED_R = 12;
const byte LED_G = 13;

boolean press = 0;
boolean oldPress = 0;

void setup() {
  Serial.begin(9600);
  pinMode(Button, INPUT);
  pinMode(LED_Y, OUTPUT);
  pinMode(LED_R, OUTPUT);
  pinMode(LED_G, OUTPUT);
  Serial.println("Welcome to RGB light project !!!");
  Serial.println("--------------------------------");

}

boolean buttunHandler(){
  oldPress = press;
  press = digitalRead(Button);
  if(press && oldPress == 0){
    Serial.print("Change status ");
    Serial.print(status, BIN);
    Serial.print(" to status ");
    Serial.println(!status, BIN);
    status = !status;
    return 1;
  }else{
    return 0;
  }

}

void Delay(unsigned long ms){
  unsigned long count = 0;
  if(!running){
    for(; count < ms; count++){
      if(buttunHandler()){
        running = 1;
        break;
      }else{
        delay(1);
      }
    }
  }
  delay(ms - count);
}

void reset(){
  digitalWrite(LED_Y, LOW);
  digitalWrite(LED_R, LOW);
  digitalWrite(LED_G, LOW);
  running = 0;
  
}

void loop() {

  reset();

  if(!status){
    digitalWrite(LED_Y, HIGH);
    Delay(500);
    digitalWrite(LED_Y, LOW);
    Delay(500);

  }else{
    digitalWrite(LED_R, LOW);
    digitalWrite(LED_G, HIGH);
    Delay(2000);

    digitalWrite(LED_G, LOW);
    digitalWrite(LED_Y, HIGH);
    Delay(1000);

    digitalWrite(LED_Y, LOW);
    digitalWrite(LED_R, HIGH);
    Delay(5000);
    
  }

}


