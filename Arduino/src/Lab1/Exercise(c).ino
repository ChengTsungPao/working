// LedOnOffTenTimes.ino
// Turn an LED on and off. Repeat 10 times.
// 4105054025、鄭琮寶

int counter; // 宣告counter變數

void setup() {
  Serial.begin(9600);  // 設定鮑率
  pinMode(13, OUTPUT); // 將13腳位輸出

}

void loop() {
  Serial.println("The LED connected to Pin13 is blinking!"); // 在Terminal顯示文字
  for(counter = 20; counter <= 120; counter += 10){ // 迴圈，並控制counter的初始值、最大上限和間格
    digitalWrite(13, HIGH); // 打開13腳位，也就是將其電壓變成"HIGH"
    delay(500); // delay 500ms
    digitalWrite(13, LOW); // 關閉13腳位，也就是將其電壓變成"LOW"
    delay(500); // delay 500ms
  }
  Serial.println("All done!"); // 在Terminal顯示文字
  for(;;); // 停止(Busy Waiting)

}