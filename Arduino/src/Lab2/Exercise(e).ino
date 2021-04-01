// PolledRcTimer.ino
// Reaction timer program modified to track as RC-time voltage decay.
// 4105054025、鄭琮寶

//   1000uF        3300uF
// 470 -->  2s   470 -->   6s
//  1k -->  6s    1k -->  20s
//  2k --> 14s    2k -->  50s
// 10k --> 80s   10k --> 286s

#include <Servo.h>

int sensorPin = 4;
unsigned int timeCounter;

void setup() {
  Serial.begin(9600);

}

void loop() {
  timeCounter = 0;
  pinMode(sensorPin, OUTPUT);
  Serial.println("Capacitor Charging...");
  digitalWrite(sensorPin, HIGH);
  for (int counter = 5; counter >= 0; counter--){ // 充電倒數計時
    delay(1000);
    Serial.println(counter, DEC);
  }
  pinMode(sensorPin, INPUT);
  digitalWrite(sensorPin, LOW);
  Serial.println("Measure decay time now!");
  while (digitalRead(sensorPin)){ // 開始計時 "RC decay time"
    delay(100);
    timeCounter++;
  }
  Serial.println("The RC decay time was");
  Serial.println(timeCounter);
  delay(1000);
  
}
