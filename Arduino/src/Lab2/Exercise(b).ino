// ServoControlWithMonitor.ino
// Send messages to the UNO to control a servo using 'Serial Monitor'
// 4105054025、鄭琮寶

#include <Servo.h>

Servo myServo;
byte Angle;
byte keyin;

void setup() {
  myServo.attach(9); // 設定伺服機
  Serial.begin(9600);
  
}

void loop() {
  myServo.write(0); // 設定伺服機角度
  Angle = 0; // 設定Angle的初始值
  Serial.println("Please enter the angle:");
  while (Serial.available() == 0){ }; // 當街收到數據的時候 Serial.available() > 0
  keyin = Serial.read(); // 讀取輸入的值
  while (keyin != '\n') { // 若按下enter退出迴圈
    if(keyin >= '0' && keyin <= '9'){
      Angle = Angle * 10 + (keyin - '0'); // 5, Angle = 10 * 0 + 5 = 5 --> 4, Angle = 10 * 0 + 4 = 54 --> .....
    }                                     // keyin - '0' => 因為'0'的ASCII為48
    keyin = Serial.read(); // 讀取輸入的值
  }
  if(Angle > 180){ // 避免值大於180度
    Serial.println("Value of Angle must be below 181.");
  }else{
    myServo.write(Angle); // 控制伺服機角度
    Serial.print("The angles is ");
    Serial.println(Angle, DEC);
  }
  delay(3000);
  
}
