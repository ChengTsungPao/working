// 4105054025、鄭琮寶

boolean status = 0;     // 宣告status變數 (是否按下按鈕，也就是按鈕之狀態)
const byte Button = 10; // 宣告Button變數
const byte LED_Y = 11;  // 宣告LED_Y變數
const byte LED_R = 12;  // 宣告LED_R變數
const byte LED_G = 13;  // 宣告LED_G變數

void setup() {
  Serial.begin(9600);     // 設定鮑率
  pinMode(Button, INPUT); // 將Button腳位輸入
  pinMode(LED_Y, OUTPUT); // 將LED_Y腳位輸出
  pinMode(LED_R, OUTPUT); // 將LED_R腳位輸出
  pinMode(LED_G, OUTPUT); // 將LED_G腳位輸出
  Serial.println("Welcome to RGB light project !!!");  // 在Terminal顯示文字
  Serial.println("--------------------------------");

}

void Delay(int ms){ // 自訂義delay
  if(!status){ // 若status = 0在執行
    for(; ms > 0; ms--){
      if(digitalRead(Button)){ // 若偵測到Button按下執行下列函數
        Serial.print("Change status !!!"); // 在Terminal顯示文字
        status = 1; // 更換status
        break; // 跳出迴圈
      }else{
        delay(1); // 等待1ms
      }
    }
  }
  delay(ms); // 將剩餘的時間等待完
}


void loop() {

  if(!status){ // 若status = 0在執行
    digitalWrite(LED_Y, HIGH); // 打開LED_Y腳位，也就是將其電壓變成"HIGH"
    Delay(500); // delay 500ms
    digitalWrite(LED_Y, LOW);  // 關閉LED_Y腳位，也就是將其電壓變成"LOW"
    Delay(500); // delay 500ms

  }else{
    digitalWrite(LED_G, HIGH); // 打開LED_G腳位，也就是將其電壓變成"HIGH"
    Delay(2000); // delay 2000ms
    digitalWrite(LED_G, LOW);  // 關閉LED_G腳位，也就是將其電壓變成"LOW"

    digitalWrite(LED_Y, HIGH); // 打開LED_Y腳位，也就是將其電壓變成"HIGH"
    Delay(1000); // delay 1000ms
    digitalWrite(LED_Y, LOW);  // 關閉LED_Y腳位，也就是將其電壓變成"LOW"

    digitalWrite(LED_R, HIGH); // 打開LED_R腳位，也就是將其電壓變成"HIGH"
    Delay(5000); // delay 5000ms
    digitalWrite(LED_R, LOW);  // 關閉LED_R腳位，也就是將其電壓變成"LOW"

    status = 0; // reset 按鈕
    
  }

}


