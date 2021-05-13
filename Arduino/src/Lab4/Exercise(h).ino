// MicroMusicWithRtttl.ino
// Play Nokia RTTTL format ringtones using array.
// 4105054025、鄭琮寶

#define SP_PIN 9
int Octave[] = {0, 262, 277, 294, 311, 330, 349, 370, 392, 415, 
				440, 466, 494, 523, 554, 587, 622, 659, 698, 740, 784, 831,
				880, 932, 988,1047, 1109, 1175, 1245, 1319, 1397, 1480, 1568, 1661, 
				1760, 1865, 1976, 2093, 2217, 2349, 2489, 2637, 2794, 2960, 3136, 3322, 
				3520, 3729, 3951, 4186, 4435, 4699, 4978, 5274, 5588, 5920, 6272, 6645};
// 音樂陣列(此兩個陣列內沒有空格) 
const char *song1 = "Entertainer:d=4,o=5,b=140:8d,8d#,8e,c6,8e,c6,8e,2c.6,8c6,8d6,8d#6,8e6,8c6,8d6,e6,8b,d6,2c6.p.8d,8d#,8e,c6,8e,c6,8e,2c.6,8p,8a,8g,8f#,8a,8c6,e6,8d6,8c6,8a,2d6";
const char *song2 = "Reveille:d=4,o=7,b=140:8g6,8c,16e,16c,8g6,8e,8c,16e,16c,8g6,8e,8c,16e,16c,8a6,8c,e,8c.8g6,8c,16e,16c,8g6,8e,8c.16e,16c,8g6,8e,8c,16e,16c,8g6,8e,c,p,8e,8e,8e,8e,g.8e,8c,8e,8c,8e,8c,e,8c,8e,8e,8e,8e,8e,g.8e,8c.8e,8c,8g6,8g6.c.";

// 題目要求
const char *song3 = "TwinkleTwinkle:d=4,o=7,b=120:c,c,g,g,a,a,2g,f,f,e,e,d,d,2c,g,g,f,f,e,e,2d,g,g,f,f,e,e,2d,c,c,g,g,a,a,2g,f,f,e,e,d,d,1c";
const char *song4 = "FrereJacques:d=4,o=7,b=125:c,d,e,c,c,d,e,c,e,f,1,2g,e,f,2g,8g,8a,8g,8f,e,c,8g,8a,8g,8f,e,c,c,g6,2c,c,g6,2c";
const char *song5 = "Beethoven5:d=8,o=7,b=125:g,g,g,2d#,p,f,f,f,2d";
const char *song6 = "ForHe'sAJollyGoodFellow:d=4,0=7,b=320:c,2e,e,e,d,e,2f.,2e,e,2d,d,d,c,d,2e.,2c,d,2e,e,e,d,e,2f,g,2a,a,g,g,g,2f,d,2c";
const char *song7 = "TakeMeOutToTheBallgame:d=4,o=7,b=225:2c6,c,a6,g6,e6,2g.6,2d6,p,2c6,c,a6,g6,e6,2g.6,g6,p,p,a6,g#6,a6,e6,f6,g6,a6,p,f6,2d6,p,2a6,a6,a6,b6,c,d,b6,a6,g6";

char Notes[] = {'p','a','#','b','c','#','d','#','e','f','#','g','#'};

#define SONGS_NUM 7
const char *songs[SONGS_NUM] = { song1, song2, song3, song4, song5, song6, song7 };

byte default_d = 4; //宣告並設定音符持續時間預設值 
byte default_o = 7; //宣告並設定八度音變數預設值
int default_b = 140; //宣告並設定每分鐘多少拍預設值
int num;
long wholenote; // 宣告全音符的時間變數
long duration; //音符持續時間
byte note; //音高暫存變數
byte scale; //音階暫存變數

//播放RTITL函數
void play_rtttl(const char *p){ 
	while(*p != ':') // 指標直接找到第一個冒號':'
		p++; //只有一行指令,可以省略大括弧
	p++; // 跳過:
	// 取得該音樂陣列的音符持續時間值(duration) 
	if(*p == 'd'){//若指標指定字元為'd'
		p = p + 2; // 跳過"d="
		num = 0;

	while(isdigit(*p)){ //判斷 p指標所指的字元是否為數字,是的話更新 num,否的話離開 while 迴圈
		num = (num * 10) + (*p++ - '0');
	} //執行完此行, p指標會移向下一個字元 
	if(num > 0) //只有一行指令,可以省略大括弧
		default_d = num; // 取得該音樂陣列的音符持續時間值
	p++; // 跳過','
	}
	Serial.print("default_d = "); 
	Serial.println(default_d, DEC);
	// 取得該音樂陣列的八度音變數預設值(octave) 
	if(*p == 'o'){ //'o'
		p = p + 2; // 跳過"o="
		num = *p++ - '0'; // 不用考慮兩位數的問題
		if(num >= 3 && num <= 7) 
			default_o = num; // 取得該音樂陣列的八度音變數值
		p++;
	} // 跳過,

	Serial.print("default_o= ");
	Serial.println(default_o, DEC);
	// 取得該音樂陣列的每分鐘多少拍值(BPM, beats per minute),也就是 tempo
	if(*p == 'b') {
		p = p + 2; // 跳過"b="
		num = 0;
		while(isdigit(*p)){
			num= (num * 10) + (*p++-'0');
		} 
		default_b = num; // 取得該音樂陣列的每分鐘多少拍值
		p++; // 跳過:
	} 
	Serial.print("default_b = ");
	Serial.println(default_b, DEC);
	// 取得全音符的時間,其中 L 為限定運算結果以 long 資料形態儲存 
	wholenote = (60 * 1000L / default_b) * 4;
	Serial.print("wholenote = ");
	Serial.println(wholenote, DEC); // 開始播放每個音符,直到陣列結束
	while(*p) { // 首先取得音符的 duration,如果有的話
		num = 0;
		while(isdigit(*p)){ 
			num = (num * 10) + (*p++ - '0');
		}
		if(num) // 如果 num 不為零,duration 就用陣列設定值
			duration =  wholenote / num;
		else //如果 num 為零, duration 就用原訂初始值 
			duration = wholenote / default_d; //休止符附點'.'的狀況放在後面需考慮
		// 取得音符
		note = 0;
		switch(*p){ //利用 case 函數取得 note
			case 'c':
				note = 1; break;	// 省略頁面,把兩行指令放在同一行
			case 'd': 
				note = 3; break;
			case 'e':
				note = 5; break; 
			case 'f':
				note = 6; break;
			case 'g':
				note = 8; break;
			case 'a':
				note= 10; break;
			case 'b':
				note = 12; break;
			case 'p':
			default:
				note = 0;
		}
		p++;
		// 取得'#' sharp 升音符(代示這個音符的音高要比標定的高半音)
		if(*p == '#'){
			note++;
			p++;
		}
		// 取得休止符附點". dotted note
		if(*p == '.'){ // 若有,則音符的音長比其原來的音長增加了一半
			duration += duration/2;
			p++;
		}
		// 取得音階(第幾個八度音)
		if(isdigit(*p)) 
			scale = *p++ - '0';
		else
			scale = default_o;
		if(*p == ',')
			p++; // 跳過',',處理下個音符,或到結尾了
		// 播放音符
		if(note){
			Serial.print("Playing: ");
			Serial.print(scale, DEC);
			Serial.print(' ');
			Serial.print(note, DEC);
			Serial.print(" (");
			Serial.print(Octave[(scale - 4) * 12 + note], DEC);
			Serial.print(") ");
			Serial.println(duration, DEC);
			tone(SP_PIN, Octave[(scale - 4) * 12 + note]);
			delay(duration); noTone(SP_PIN);
		}
		else{
			Serial.print("Pausing: ");
			Serial.println(duration, DEC);
			delay(duration);
		}
	}	
}

// 主程式 setup 與 loop

void setup() {
	Serial.begin(9600);

}

void loop() {
	int i;
	Serial.print("Start.");
	for(i = 0; i < SONGS_NUM; i++){
		play_rtttl(songs[i]);
		delay(1000);
	}
	Serial.print("Done.");
	while(1) {}; // 停止執行程式

}
