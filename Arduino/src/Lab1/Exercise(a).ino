// LedOnOff.ino
// Turn an LED on and off. Repeat 1 time per second in definitely.
// 4105054025、鄭琮寶

void setup() {
  Serial.begin(9600);  // 設定鮑率
  pinMode(13, OUTPUT); // 將13腳位輸出

}

void loop() {
  Serial.println("The LED connected to Pin13 is blinking!"); // 在Terminal顯示文字
  digitalWrite(13, HIGH); // 打開13腳位，也就是將其電壓變成"HIGH"
  delay(500); // delay 500ms
  digitalWrite(13, LOW); // 關閉13腳位，也就是將其電壓變成"LOW"
  delay(1500); // delay 1500ms

}