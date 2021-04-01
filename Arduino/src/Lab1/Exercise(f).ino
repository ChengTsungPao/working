// PushbuttonControlled.ino
// Check pushbutton state 10 times per second and blink LED when pressed.
// 4105054025、鄭琮寶

const byte SW = 13; // 宣告SW變數
const byte LED = 12; //宣告LED變數

void setup() {
  Serial.begin(9600);    // 設定鮑率
  pinMode(SW, INPUT);    // 將SW腳位輸入
  pinMode(LED, OUTPUT);  // 將LED腳位輸出

}

void loop() {
  boolean val = digitalRead(SW); // 讀取SW腳位的電壓(判斷開啟或關閉)
  if(val){ // 若val值為1的時候執行if條件，否則執行else條件
    Serial.println("SW = 1");  // 在Terminal顯示文字
    digitalWrite(LED, HIGH); // 打開LED腳位，也就是將其電壓變成"HIGH"
    delay(50); // delay 50ms
    digitalWrite(LED, LOW); // 關閉LED腳位，也就是將其電壓變成"LOW"
    delay(50); // delay 50ms
  }else{
    Serial.println("SW = 0"); // 在Terminal顯示文字
    digitalWrite(LED, HIGH); // 打開LED腳位，也就是將其電壓變成"HIGH"
    delay(100); // delay 100ms
    digitalWrite(LED, LOW); // 關閉LED腳位，也就是將其電壓變成"LOW"
    delay(100); // delay 100ms
  }

}