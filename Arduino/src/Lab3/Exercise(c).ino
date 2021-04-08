// DisplayDigitsWithArray.ino
// Use a Array to store and display digits with a 7-segment LED display.
// 4105054025、鄭琮寶

byte index = 0;
const byte LEDs[16] = {
  B00010000, B01111011, B00100100, B00101001,
  B01000011, B10001001, B10000000, B00011011,
  B00000000, B00001001, B00000010, B11001000,
  B10010100, B01101000, B10000100, B10001110
};

void setup() {
  DDRD = B11111111; // 將pin0-7接腳全設成輸出模式
}

void loop() {
  PORTD = LEDs[index]; // 將pin0-7的輸出 1(HIGH), 0(LOW) 等同於陣列中指標所指定的值
  index++;             // 將指標變數index加1
  if(index == 16){     //為了讓程式循環，當index加到16時，重新設為0
    index = 0;
  }
  delay(1000);
   
}

