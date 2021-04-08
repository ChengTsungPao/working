// DialDisplay.ino
// Display POT position using 7-segment LED display.
// 4105054025、鄭琮寶

byte index;
int timeCounter;
int time;
int sensorPin = 9;

const byte LEDs[7] = {
  B00011000, // 依題目要求增加D
  B00011010, B00011110, B10011110, 
  B11011110, B11111110, B11111111
};

void setup() {
  DDRD = B11111111; // 將pin0-7接腳全設成輸出模式
}

void loop() {
  time = RCtime(sensorPin);
  index=map(time, 0, 900, 0, 6); // 把RCtime的範圍對映到0-5之間 // RCtime的變化範圍,可根據不同情況斟酌調整
  PORTD = LEDs[index];

}

long RCtime(byte sensPin) { // 與之前程式相同，計算RCtime
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
