// ReadPotWithRcTime.ino
// Read potentiometer in RC-time circuit using RCTIME command.
// 4105054025、鄭琮寶

// 0.01uF -->  11s
// 0.10uF --> 112s

#include <Servo.h>

int sensorPin = 4;
unsigned int timeCounter;

void setup() {
  Serial.begin(9600);

}

void loop() {
  Serial.println("The RC decay time was");
  Serial.println(RCtime(sensorPin), DEC); // 計算RCTime
  delay(1000);
  
}

unsigned int RCtime(byte sensPin){
  timeCounter = 0;
  pinMode(sensPin, OUTPUT);
  digitalWrite(sensPin, HIGH);
  delay(100); // 充電時間100ms
  pinMode(sensPin, INPUT);
  digitalWrite(sensPin, LOW);
  while (digitalRead(sensPin)){
    // delay(0); // 因為放電時間太短，所以0ms
    timeCounter++;
  }
  return timeCounter;

}
