// ServoControlWithPushbuttons.ino 
// Press and hold P12 pushbutton to rotate the servo counterclockwise, llor press the pushbutton connected to P11 to rotate the servo clockwise.
// 4105054025、鄭琮寶

#include <Servo.h>

Servo myServo;
const byte SW1 = 12; // counterclockwise
const byte SW2 = 11; // clockwise
boolean button1;
boolean button2;
byte Angle = 90;

void setup() {
  myServo.attach(9); // 設定伺服機
  Serial.begin(9600);
  pinMode(SW1, INPUT);
  pinMode(SW2, INPUT);

}

void loop() {
  button1 = digitalRead(SW1);
  if(button1){
    if(Angle < 159){ // 最大角度限制
      Angle += 2;
    }
  }
  button2 = digitalRead(SW2);
  if(button2){
    if(Angle > 21){ // 最小角度限制
      Angle -= 2;
    }
  }  
  myServo.write(Angle);
  Serial.print("Angle = ");
  Serial.println(Angle, DEC);
  delay(10);
  
}
