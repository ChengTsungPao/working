// SimpleSubprogram.ino
// Demonstrate how Subprogram work.
// 4105054025、鄭琮寶

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println("Start main program" ); 
  delay(2000);
  First_Subprogram(); // 呼叫 First_Subprogram 副程式
  Serial.println("Back in main."); 
  delay(2000);
  Second_Subprogram(); // 呼叫 Second_Subprogram 副程式
  Serial.println("Back in main."); 
  delay(2000);
  Third_Subprogram(); // 呼叫 Third_Subprogram 副程式 
  Serial.println("Repeat main..." );
  delay(2000);
}

void First_Subprogram(){ // First_Subprogram 副程式
  Serial.print("Executing first" ); 
  Serial.println(" subprogram." ); 
  delay(3000);
}

void Second_Subprogram(){ // Second_Subprogram 副程式
  Serial.print("Executing second" ); 
  Serial.println(" subprogram." ); 
  delay(3000);
}

void Third_Subprogram(){ // 依題目要求新增 Third_Subprogram 副程式
  Serial.print("Executing third" ); 
  Serial.println(" subprogram." ); 
  delay(3000);
}
