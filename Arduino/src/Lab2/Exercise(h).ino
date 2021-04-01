// ControlServoWithUsingConstants.ino
// Read potentiometer in RC-time circuit using RCTIME command. Scale time by 100 / 112 and offset by 20 for the servo.
// 4105054025、鄭琮寶

#include <Servo.h>

#define sensorPin 5
#define ServoPin 9
#define BaudRate 9600
#define toHigh 100
#define fromHigh 112
#define offset 20

Servo myServo;
int timeCounter;
unsigned int Time, Time1;
unsigned int Angle = 0;

void setup() {
  Serial.begin(9600);
  myServo.attach(9);
  Serial.println(sensorPin, DEC);

}

void loop() {
  Serial.println("Program Running");
  Time = RCtime(sensorPin); // 計算RCtime
  Serial.println(timeCounter, DEC);
  if(max(Time, Time1) - min(Time, Time1) < 6){ // 若變動幅度太小，不變化
    Time = Time1;
  }
  Time1 = Time;
  Time = Time * toHigh / fromHigh; // 比例縮放
  Angle = Time + offset; // 將數值範圍平移
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
