// DisplayDigits.ino
// Display the digits 0 through 9 on a 7-segment LED display.
// 4105054025、鄭琮寶

void setup() {
  DDRD = B11111111; // 將pin0-7接腳全設成輸出模式
}

void loop() {
  // BAFG.CDE
  /*
  PORTD = B00010000; // 0,小數點會亮
  delay(1000);       // 暫停一秒
  PORTD = B01111011; // 1,小數點不會亮
  delay(1000);       // 暫停一秒
  PORTD = B00100100; // 2,小數點會亮
  delay(1000);       // 暫停一秒
  PORTD = B00101001; // 3,小數點不會亮
  delay(1000);       // 暫停一秒
  PORTD = B01000011; // 4,小數點會亮
  delay(1000);       // 暫停一秒
  PORTD = B10001001; // 5,小數點不會亮 
  delay(1000);       // 暫停一秒
  PORTD = B10000000; // 6,小數點會亮 
  delay(1000);       // 暫停一秒
  PORTD = B00011011; // 7,小數點不會亮
  delay(1000);       // 暫停一秒 
  PORTD = B00000000; // 8,小數點會亮
  delay(1000);       // 暫停一秒
  PORTD = B00001001; // 9,小數點不會亮
  delay(1000);       // 暫停一秒
  */
  PORTD = B00000010; // A,小數點會亮
  delay(1000);       // 暫停一秒
  PORTD = B11001000; // b,小數點不會亮
  delay(1000);       // 暫停一秒
  PORTD = B10010100; // C,小數點會亮
  delay(1000);       // 暫停一秒
  PORTD = B01101000; // d,小數點不會亮
  delay(1000);       // 暫停一秒
  PORTD = B10000100; // E,小數點會亮
  delay(1000);       // 暫停一秒
  PORTD = B10001110; // F,小數點不會亮 
  delay(1000);       // 暫停一秒
   
}

