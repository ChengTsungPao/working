// ServoVelocities.ino
// Rotate the servo counterclockwise slowly, then clockwise rapidly.
// 4105054025、鄭琮寶

#include <Servo.h>

Servo myServo;

void setup() {
  myServo.attach(9); // 設定伺服機
  Serial.begin(9600);

}

void loop() {
  myServo.write(0);
  Serial.println("Counterclockwise!");
  for(int i = 0; i <= 180; i += 10){ // 每50ms增加伺服機角度10度
    myServo.write(i); // 設定伺服機角度
    delay(50);
    Serial.print("i = ");
    Serial.println(i, DEC);
  }
  delay(3000);
  Serial.println("Clockwise!");
  for(int i = 180; i >= 0; i -= 20){ // 若設定為 i -= 50，則無法順利旋轉到角度為 0 (i = 0)
    myServo.write(i);
    delay(50); // 若設定為100，則肉眼可見較不平順
    Serial.print("i = ");
    Serial.println(i, DEC);
  }
  delay(3000);
  
}
