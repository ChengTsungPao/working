#include <Arduino.h>
#include <Servo.h>

#define sensorPin 4
#define ServoPin 9
#define BaudRate 9600

#define toHigh 20
#define fromHigh 73
#define offset 10

#define MaxAngle 165
#define MinAngle 15
#define InitAngle 90

#define Up 3
#define Down 11
#define LED_G 12
#define LED_R 13

Servo myServo;
byte status;
int adjustVal;
int timeCounter;
unsigned int Time, Time1;
unsigned int Angle = InitAngle;

void setup() {
  Serial.begin(9600);
  myServo.attach(9);
  pinMode(Up, INPUT);
  pinMode(Down, INPUT);
  pinMode(LED_G, OUTPUT);
  pinMode(LED_R, OUTPUT);

  adjustVal = adjust();
  status = 0;

}

void loop() {
  if(digitalRead(Up) && status != 1){
    Serial.println("Up");
    Angle = MaxAngle;

    digitalWrite(LED_G, HIGH);
    myServo.write(Angle);
    delay(500);
    digitalWrite(LED_G, LOW);

    Serial.print("Angle = ");
    Serial.println(Angle, DEC);
    status = 1;

  }else if(digitalRead(Down) && status != 2){
    Serial.println("Down");
    Angle = MinAngle;

    digitalWrite(LED_R, HIGH);
    myServo.write(Angle);
    delay(500);
    digitalWrite(LED_R, LOW);

    Serial.print("Angle = ");
    Serial.println(Angle, DEC);
    status = 2;

  }else if(status != 0){
    Angle = MaxAngle * (status == 1) + MinAngle * (status == 2) + adjust();
    myServo.write(Angle);

    Serial.print("Angle = ");
    Serial.println(Angle, DEC);
  }
  delay(100);
   
}

int adjust() {
  int adjustAngle;
  Time = RCtime(sensorPin);
  if(max(Time, Time1) - min(Time, Time1) < 6){
    Time = Time1;
  }
  Time1 = Time;
  Time = Time * toHigh / fromHigh;
  adjustAngle = Time - offset;
  if(adjustAngle > toHigh - offset){
    return toHigh - offset;
  }else if(adjustAngle < 0 - offset){
    return 0 - offset;
  }else{
    return adjustAngle;
  }
  
}

unsigned int RCtime(byte sensPin) {
  timeCounter = 0;
  pinMode(sensPin, OUTPUT);
  digitalWrite(sensPin, HIGH);
  delay(100); // 充電時間100ms
  pinMode(sensPin, INPUT);
  digitalWrite(sensPin, LOW);
  while (digitalRead(sensPin)){
    timeCounter++;
  }
  return timeCounter;

}
