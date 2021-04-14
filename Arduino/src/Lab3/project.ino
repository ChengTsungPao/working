// 4105054025、鄭琮寶

# define STOP_times 20
# define Delay_Time (50 * (STOP_times + 1))

byte times = STOP_times + 1;
unsigned int time = 0; 
unsigned int STOP_RCTime;
int sensorPin = 12;

const byte LEDs[6] = {
  B01111011, B00101100, B00101001, 
  B01001011, B10001001, B10001000 
};

void setup() {
  // Serial.begin(9600);
  
  Get_Rc_Time();
  STOP_RCTime = time * 1.5;

  DDRD = B11111111; // 將pin0-7接腳全設成輸出模式
  while(time < STOP_RCTime){ // 直到第一次遮住光敏電阻在運作
    Get_Rc_Time();
  }
}

void loop() {
  // Serial.println(time, DEC);

  Get_Rc_Time();    // 得到RC時間
  Delay();          // 以RC時間當延遲時間
  Update_Display(); // 顯示數字
}

void Get_Rc_Time(){ // 之前程式相同，獲得RC-Time
  time = 0;
  pinMode(sensorPin, OUTPUT); 
  digitalWrite(sensorPin, HIGH); 
  delay(50);
  pinMode(sensorPin, INPUT); 
  digitalWrite(sensorPin, LOW); 
  while(digitalRead(sensorPin)){ 
    time++;
  }
}

void Delay(){ // 之前程式類似，控制delay
  PORTD -= 8 * ((times != (STOP_times + 1)) && times != 1); // 當手移開時，LED燈閃爍
  delay(Delay_Time / times);
  PORTD += 8 * ((times != (STOP_times + 1)) && times != 1); // 當手移開時，LED燈閃爍
}

void Update_Display(){ // 之前程式類似，更新七段顯示器

  if(time < STOP_RCTime){ // 當手移開時，進入判斷
    if(times == 1){ // 當手移開且已跳變"STOP_times"次時，不須再跳變，直接return
      return;
    }else{
      times--;
    }
  }else{
    times = STOP_times + 1;
  }

  PORTD = LEDs[random(6)];
}