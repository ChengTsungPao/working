// SegmentTestWithHighLow.ino
// Individually test each segment in a 7-Segment LED display.
// 4105054025、鄭琮寶

byte pinCounter;

void setup() {
  for(byte i = 0; i < 8; i++){ // 依序設定七段顯示器八個腳位
    pinMode(i, OUTPUT);
    digitalWrite(i, HIGH);
  }

}

void loop() {
  for (byte pinCounter = 0; pinCounter < 8; pinCounter++){
    digitalWrite(pinCounter, LOW); // LED燈依序亮起
    delay(1000); // 每1秒亮一次
    // digitalWrite(pinCounter, HIGH);
  }
  for (byte pinCounter = 0; pinCounter < 8; pinCounter++){
    digitalWrite(pinCounter, HIGH); // LED燈依序熄滅
  }
   
}