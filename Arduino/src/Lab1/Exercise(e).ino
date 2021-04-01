// TestBiColorLed.ino
// Turn bi-color LED red, then green, then off in a loop.
// 4105054025、鄭琮寶

int counter; // 宣告counter變數

void setup() {
  Serial.begin(9600);  // 設定鮑率
  pinMode(12, OUTPUT); // 將12腳位輸出
  pinMode(13, OUTPUT); // 將13腳位輸出

}

void loop() {
  for(counter = 20; counter <= 120; counter += 20){ // 迴圈，並控制counter的初始值、最大上限和間格
    digitalWrite(12, HIGH); // 打開12腳位，也就是將其電壓變成"HIGH"
    digitalWrite(13, LOW);  // 關閉13腳位，也就是將其電壓變成"LOW"
    delay(counter); // delay counter ms
    digitalWrite(12, LOW);  // 關閉12腳位，也就是將其電壓變成"LOW"
    digitalWrite(13, HIGH); // 打開13腳位，也就是將其電壓變成"HIGH"
    delay(counter); // delay counter ms
  }
  Serial.println("All done"); // 在Terminal顯示文字

}