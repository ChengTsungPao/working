// 4105054025、鄭琮寶

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
byte status; // 系統狀態
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
  if(digitalRead(Up) && status != 1){ // 角度最大之執行程式
    Serial.println("Up");
    Angle = MaxAngle;

    digitalWrite(LED_G, HIGH); // LED燈亮
    myServo.write(Angle); // 角度轉向
    delay(500);
    digitalWrite(LED_G, LOW); // LED燈暗

    Serial.print("Angle = ");
    Serial.println(Angle, DEC);
    status = 1;

  }else if(digitalRead(Down) && status != 2){ // 角度最小之執行程式
    Serial.println("Down");
    Angle = MinAngle;

    digitalWrite(LED_R, HIGH); // LED燈亮
    myServo.write(Angle); // 角度轉向
    delay(500);
    digitalWrite(LED_R, LOW); // LED燈暗

    Serial.print("Angle = ");
    Serial.println(Angle, DEC);
    status = 2;

  }else if(status != 0){ // 微調
    Angle = MaxAngle * (status == 1) + MinAngle * (status == 2) + adjust(); // 判斷目前之系統狀態來決定要由，MaxAngle或MinAngle調整
    myServo.write(Angle);

    Serial.print("Angle = ");
    Serial.println(Angle, DEC);
  }
  delay(100);
   
}

int adjust() { // 偵測RCtime支變化來控制，微調伺服機角度
  int adjustAngle;
  Time = RCtime(sensorPin);
  if(max(Time, Time1) - min(Time, Time1) < 6){
    Time = Time1;
  }
  Time1 = Time;
  Time = Time * toHigh / fromHigh;
  adjustAngle = Time - offset;
  if(adjustAngle > toHigh - offset){ // 避免誤差，過範圍則以邊界值為輸出值
    return toHigh - offset;
  }else if(adjustAngle < 0 - offset){
    return 0 - offset;
  }else{
    return adjustAngle;
  }
  
}

unsigned int RCtime(byte sensPin) { // 與前支程式相同，計算RCtime
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
