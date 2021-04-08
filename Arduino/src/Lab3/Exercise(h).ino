// LightMeter.ino
// Indicate light level using 7-segment display.
// 4105054025、鄭琮寶

// 透過控制Delay副程式，可控制數字跳變之快慢
// 換成1uF電容RC-Time上升，數字跳變會變慢

byte index = 0;
unsigned int time; 
int sensorPin = 12;

const byte LEDs[10]={
  B00010000, B01111011, B00100100, B00101001, B01000011, 
  B10001001, B10000000, B00011011, B00000000, B00001001 
};

void setup() {
  DDRD = B11111111; // 將pin0-7接腳全設成輸出模式
}

void loop() {
  Get_Rc_Time();    // 得到RC時間
  Delay();          // 以RC時間當延遲時間
  Update_Display(); // 顯示數字
}

void Get_Rc_Time(){ 
  time = 0;
  pinMode(sensorPin, OUTPUT); 
  digitalWrite(sensorPin, HIGH); 
  delay(50);
  pinMode(sensorPin, INPUT); 
  digitalWrite(sensorPin, LOW); 
  while(digitalRead(sensorPin)){ 
    time++;
  }
}

void Delay(){ 
  delay(time / 2); // 數字跳變加快2倍 (time * 2 => 放慢2倍)
}

void Update_Display(){ 
  PORTD = LEDs[index];
  index++;
  if(index == 10){ 
    index = 0;
  }
}
