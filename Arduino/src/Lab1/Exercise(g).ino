// PushbuttonControlOfTwoLeds.ino
// Blink P13 LED if P11 pushbutton is pressed, and blink P12 LED if P10 pushbutton is pressed.
// 4105054025、鄭琮寶

const byte SW1 = 11; // 宣告SW1變數
const byte SW2 = 10; // 宣告SW2變數

const byte LED1 = 13; // 宣告LED1變數
const byte LED2 = 12; // 宣告LED2變數

void setup() {
  Serial.begin(9600);     // 設定鮑率
  pinMode(SW1, INPUT);    // 將SW1腳位輸入
  pinMode(SW2, INPUT);    // 將SW2腳位輸入
  pinMode(LED1, OUTPUT);  // 將LED1腳位輸出
  pinMode(LED2, OUTPUT);  // 將LED2腳位輸出

}

void loop() {
  boolean val1 = digitalRead(SW1); // 讀取SW1腳位的電壓(判斷開啟或關閉)
  boolean val2 = digitalRead(SW2); // 讀取SW2腳位的電壓(判斷開啟或關閉)

  if(val1){ // 若val1值為1的時候執行if條件，若val2值為1的時候執行else if條件，否則執行else條件
    Serial.println("SW1 = 1"); // 在Terminal顯示文字
    digitalWrite(LED1, HIGH); // 打開LED1腳位，也就是將其電壓變成"HIGH"
    delay(50);

  }else if(val2){
    Serial.println("SW2 = 1"); // 在Terminal顯示文字
    digitalWrite(LED2, HIGH); // 打開LED2腳位，也就是將其電壓變成"HIGH"
    delay(50); // delay 50ms

  }else{
    delay(50); // delay 50ms

  }

  digitalWrite(LED1, LOW); // 關閉LED1腳位，也就是將其電壓變成"LOW"
  digitalWrite(LED2, LOW); // 關閉LED2腳位，也就是將其電壓變成"LOW"
  delay(50); // delay 50ms

}


