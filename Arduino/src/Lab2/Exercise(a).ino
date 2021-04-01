// ServoTest.ino
// Test the servo at three different position signals
// 4105054025、鄭琮寶

#include <Servo.h>

Servo myServo;

void setup() {
  myServo.attach(9); // 設定伺服機腳位
  
}

void loop() {
  myServo.write(180); // 控制伺服機角度
  delay(3000);
  myServo.write(0);
  delay(3000);
  myServo.write(90);
  delay(3000);
  for(;;); // 停止

}