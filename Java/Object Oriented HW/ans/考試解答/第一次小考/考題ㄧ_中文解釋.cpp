#include<stdio.h>
#include<stdlib.h>
#include<time.h>

// 'a' - 'z' : 97 -122    'A' - 'Z' : 65-90
int main(){
	
	char c[1000];
	int flag,ans=0;   // flag 判斷該英文字母先前是否有出現過 
	
	/* 給予初始化，避免陣列內會有在 a-z & A-Z 的字元 */
	for(int i=0;i<1000;i++) 	
	c[i]='0';
	
	printf("Enter:");
	gets(c);   // 可接受所有輸入包括空白 
	
	for(int i=0;i<1000;i++){
		
		flag=1;   // flag=1 先前字母沒出現過累加否則等於 0  
		
		if( (65<=(int)c[i]&&(int)c[i]<=90) || (97<=(int)c[i]&&(int)c[i]<=122) ){    // 當 c[i] 介於 97-122 & 65-90  假受目前 c[i] 的值為 'a':97 下ㄧ個值為 'A':65 
			
			for(int j=0;j<i;j++) // 檢查 c[0]-c[i-1] 先前是否有出現過 
				if( (int)c[i]==(int)c[j]+32 || (int)c[i]==(int)c[j] || (int)c[i]==(int)c[j]-32 ){    //  now 'a':97 => 所以要判斷先前是否出現過 'a' & 'A'。  'a':(int)c[i]==(int)c[j] 以及   'A':(int)c[i]==(int)c[j]-32
																									 //  now 'A':65 => 所以要判斷先前是否出現過 'A' & 'a'。  'A':(int)c[i]==(int)c[j] 以及   'a':(int)c[i]==(int)c[j]+32  
																									 //  所以需要  (int)c[i]==(int)c[j]  ||  (int)c[i]==(int)c[j]-32 ||  (int)c[i]==(int)c[j]+32   這些判斷式  
					flag=0;
					break;	
				}
			
			if(flag) ans++;
		}
	}
	
	printf("%d\n",ans);	
		
}
