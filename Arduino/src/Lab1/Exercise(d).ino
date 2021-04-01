// FlashBothLeds.ino
// Turn LEDs connected to P11、P12 and P13 on and off.
// 4105054025、鄭琮寶

void setup() {
  Serial.begin(9600);  // 設定鮑率
  pinMode(13, OUTPUT); // 將13腳位輸出
  pinMode(12, OUTPUT); // 將12腳位輸出
  pinMode(11, OUTPUT); // 將11腳位輸出

}

void loop() {
  digitalWrite(11, LOW);  // 關閉11腳位，也就是將其電壓變成"LOW"
  digitalWrite(13, HIGH); // 打開13腳位，也就是將其電壓變成"HIGH"
  delay(500); // delay 500ms
  digitalWrite(13, LOW);  // 關閉13腳位，也就是將其電壓變成"LOW"
  digitalWrite(12, HIGH); // 打開12腳位，也就是將其電壓變成"HIGH"
  delay(500); // delay 500ms
  digitalWrite(12, LOW);  // 關閉12腳位，也就是將其電壓變成"LOW"
  digitalWrite(11, HIGH); // 打開11腳位，也就是將其電壓變成"HIGH"
  delay(500); // delay 500ms

}