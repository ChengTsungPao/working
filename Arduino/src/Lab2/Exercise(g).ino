// ControlServoWithPot.ino
// Read potentiometer in RC-time circuit using RCTIME command.
// 4105054025、鄭琮寶

#include <Servo.h>

Servo myServo;
int sensorPin = 4;
int timeCounter;
unsigned int Time, Time1;
unsigned int Angle = 0;

void setup() {
  Serial.begin(9600);
  myServo.attach(9);

}

void loop() {
  Serial.println("Program Running");
  Time = RCtime(sensorPin);
  Serial.println(timeCounter, DEC);
  if(max(Time, Time1) - min(Time, Time1) < 6){
    Time = Time1;
  }
  Time1 = Time;
  Time = Time * 120 / 112; // 0.1uF RC-time 最大為112s
  Angle = Time + 30;
  Serial.print("Angle = ");
  Serial.println(Angle, DEC);
  myServo.write(Angle);
  
}

unsigned int RCtime(byte sensPin){ // 與前支程式相同，計算RCtime
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
