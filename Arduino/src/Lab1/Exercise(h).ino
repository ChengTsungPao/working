// ReactionTimer.ino
// Test reaction time with a pushbutton and a bi-color LED
// 4105054025、鄭琮寶

String time; // 宣告time變數
int randValue; // 宣告randValue變數
boolean val = 0; // 宣告val變數
const byte Button = 11; // 宣告Button變數
const byte LED_R = 12; // 宣告LED_R變數
const byte LED_G = 13; // 宣告LED_G變數
extern volatile unsigned long timer0_millis; // arduino的Timer值


void setup() {
  Serial.begin(9600);     // 設定鮑率
  pinMode(Button, INPUT); // 將Button腳位輸入
  pinMode(LED_R, OUTPUT); // 將LED_R腳位輸出
  pinMode(LED_G, OUTPUT); // 將LED_G腳位輸出
  Serial.println("Press and hold pushbutton.");  // 在Terminal顯示文字
  Serial.println("to make light turn red.");
  Serial.println("When light turns green, let");
  Serial.println("go as fast as you can.");
  Serial.println("----------------------------");

}

void setMillis(unsigned long new_millis){ // 重置arduino的Timer
  uint8_t oldSREG = SREG;
  cli(); // disable interupt
  timer0_millis = new_millis; // 歸零
  SREG = oldSREG;
}

void loop() {
  while(!val){ // val = 0繼續執行
    val = digitalRead(Button); // 讀取Button腳位的電壓(判斷開啟或關閉)
  }

  randValue = random(100); // 從0~99隨機選取一個數字
  Serial.print("Delay time = ");  // 在Terminal顯示文字
  Serial.println(1000 + randValue, DEC);  // 在Terminal顯示文字
  
  digitalWrite(LED_R, HIGH); // 打開LED_R腳位，也就是將其電壓變成"HIGH"
  digitalWrite(LED_G, LOW);  // 關閉LED_G腳位，也就是將其電壓變成"LOW"
  delay(1000 + randValue); // delay (1000 + randValue) ms

  val = digitalRead(Button); // 讀取Button腳位的電壓(判斷開啟或關閉)

  digitalWrite(LED_R, LOW);  // 關閉LED_R腳位，也就是將其電壓變成"LOW"
  digitalWrite(LED_G, HIGH); // 打開LED_G腳位，也就是將其電壓變成"HIGH"

  if(!val){
    Serial.println("You cheating !!!");

  }else{
    setMillis(0); // Timer Reset 
    while(val){   // 若val值為1的時候執行if條件，否則執行else條件
      val = digitalRead(Button); // 讀取Button腳位的電壓(判斷開啟或關閉)
    }
    time = String(millis(), DEC); // 紀錄反應時間

    Serial.print("Your time was ");  // 在Terminal顯示文字
    Serial.print(time);
    Serial.println("ms.\n\n");
    Serial.println("To play again, hold the");
    Serial.println("button down again.");

  }

  digitalWrite(LED_G, LOW);  // 關閉LED_G腳位，也就是將其電壓變成"LOW"
  Serial.println("----------------------------");  // 在Terminal顯示文字

}



