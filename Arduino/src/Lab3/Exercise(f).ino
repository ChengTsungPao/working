// TestPhotoresistor.ino
// Read photoresistor in RC-time circuit using RCTIME command.
// 4105054025、鄭琮寶

// 0.01uF -> 138
// 0.10uF -> 1350
// RCTime大約相差10倍

// 觀察: 當越暗時，所測得之RCTime越大 (光敏電阻阻值上升)

// 測試環境: 509A 2021/4/8 18:18

int timeCounter;
int sensorPin = 12;

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println(RCtime(sensorPin));
  delay(1000);
}

long RCtime(byte sensPin) { // 與之前程式相同，計算RCtime
  timeCounter = 0;
  pinMode(sensPin, OUTPUT);
  digitalWrite(sensPin, HIGH);
  delay(100); // 充電時間100ms
  pinMode(sensPin, INPUT);
  digitalWrite(sensPin, LOW);
  while (digitalRead(sensPin)){
    timeCounter++;
  }
  return timeCounter;

}
