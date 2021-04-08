// SimpleMap.ino
// 4105054025、鄭琮寶

byte value;
int number;
int keyin;

void setup() {
  Serial.begin(9600);
}

void loop() {
  number = 0;
  Serial.println("Please enter the number:");
  while (Serial.available() == 0){ }; // 當接收到數據的時候 Serial.available() > 0
  keyin = Serial.read(); // 讀取輸入的值
  while (keyin != '\n') { // 若按下enter退出迴圈
    if(keyin >= '0' && keyin <= '9'){ // 處理0~9的符號
      number = number * 10 + (keyin - '0'); 
    }                                     
    keyin = Serial.read(); // 讀取輸入的值
  }

  // 把value的範圍由120對映到0-9之間
  // 注意只有在number=120的時候才會對應到9
  // 當輸入值超出範圍時，會等比例放大
  value = map(number, 0, 120, 0, 9); 
  Serial.print("number: ");
  Serial.print(number, DEC); 
  Serial.print(" value: ");
  Serial.println(value, DEC);
}

