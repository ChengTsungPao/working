// ColorCycle.ino
// 4105054025、鄭琮寶

// 使用陣列定義顏色對應碼
const byte array_red[3] = {255,0,0}; 
const byte array_orange[3] = {255,165,0}; 
const byte array_yellow[3] = {255,255,0};
const byte array_green[3] = {0,255,0};
const byte array_blue[3] = {0,0,255}; 
const byte array_indigo[3] = {75,0,130}; 
const byte array_purple[3] = {128,0,128}; 
const byte array_white[3] = {255,255,255};

// 宣告變數
const byte Red = 7;
const byte Green = 6;
const byte Blue = 5;
const int TurnOnTime = 3000;   // 漸亮時間
const int MaintainTime = 1000; // 維持時間
const int TurnOffTime = 3000;  // 漸暗時間
byte light[3]; // 定義陣列變數, 作為儲存顏色對應
int counter;
byte index;

void setup() {
	pinMode(Red, OUTPUT);
	pinMode(Green, OUTPUT);
	pinMode(Blue, OUTPUT);

}

void loop() {
	subred(); // 呼叫subred()副程式將動作顏色指定為亮紅色
	active(); // 呼叫active()副程式開始動作
	suborange(); // 指定亮橙色
	active();
	subyellow(); // 指定亮黃色
	active();
	subgreen(); // 指定亮綠色
	active();
	subblue(); // 指定亮藍色
	active();
	subindigo(); // 指定亮靛藍
	active();
	subpurple(); // 指定亮紫色
	active(); 
	subwhite(); // 指定亮白色 
	active();
}


void subred(){ // 將light變數setup成指定的顏色的色碼
	for(index=0;index<3;index++){
		light[index]=array_red[index];
	}
}

void suborange(){ // 將light變數setup成指定的顏色的色碼
	for(index=0;index<3;index++){ 
		light[index]=array_orange[index];
	}
}

void subyellow(){ // 將light變數setup成指定的顏色的色碼
	for(index=0;index<3;index++){ 
		light[index]=array_yellow[index];
	}
}

void subgreen(){ // 將light變數setup成指定的顏色的色碼
	for(index=0;index<3;index++){ 
		light[index]=array_green[index];
	}
}

void subblue(){ // 將light變數setup成指定的顏色的色碼
	for(index=0;index<3;index++){ 
		light[index]=array_blue[index];
	}
}

void subindigo(){ // 將light變數setup成指定的顏色的色碼
	for(index=0; index<3;index++){ 
		light[index]=array_indigo[index];
	}
}

void subpurple(){ // 將light變數setup成指定的顏色的色碼
	for(index=0;index<3;index++){ 
		light[index]=array_purple[index];
	}
}

void subwhite(){ // 將light變數setup成指定的顏色的色碼
	for(index=0;index<3;index++){
		light[index]=array_white[index];
	}
}

void active(){  // 使led動作
	TurnON();   // 漸漸變亮
	Maintain(); // 維持最亮
	TurnOFF();  // 漸漸變暗
}

void TurnON(){ // 執行由暗轉亮的過程 
	for(counter=1;counter<=(TurnOnTime/6);counter++){ // 因為每個RGB亮2ms,故TurnOnTime要除以6,以下皆同 
		analogWrite(Red,map(counter,0,TurnOnTime/6,0,light[0])); // 將原本counter變動的範圍(0-TurnOnTime/6)改對應至(0-light[0]),以下皆同 
		delay(2);
		analogWrite(Green,map(counter,0,TurnOnTime/6,0,light[1]));
		delay(2);
		analogWrite(Blue,map(counter,0,TurnOnTime/6,0,light[2]));
		delay(2);
	}
}

void Maintain(){ // 維持最亮狀態
	for(counter=1;counter<=MaintainTime/6;counter++){
		analogWrite(Red, light[0]);
		delay(2);
		analogWrite(Green, light[1]);
		delay(2);
		analogWrite(Blue,light[2]);
		delay(2);
	}
}

void TurnOFF(){ // 執行由亮轉暗的過程 
	for(counter=TurnOffTime/6;counter>=1;counter--){
		analogWrite(Red,map(counter, 0,TurnOffTime/6,0,light[0])); 
		delay(2);
		analogWrite(Green,map(counter,0,TurnOffTime/6,0,light[1]));
		delay(2);
		analogWrite(Blue,map(counter, 0, TurnOffTime/6,0,light[2])); 
		delay(2);
	}
}