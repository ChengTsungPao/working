#include<stdio.h>
#include<stdlib.h>
#include<time.h>

// printf(%d %d %d %d ,'a','z','A','Z'); 'a' - 'z' : 97 -122    'A' - 'Z' : 65-90
int main(){
	
	char c[1000];
	int flag,ans=0;   // flag: determine whether the English alphabets have appeared before 
	
	/* Give the initialization to avoid characters will appear a-z & A-Z in the array */
	for(int i=0;i<1000;i++) 	
	c[i]='0';
	
	printf("Enter:");
	gets(c);   // Accept all inputs including blank
	
	for(int i=0;i<1000;i++){
		
		flag=1;   // flag=1 The previous alphabets didn't appear, or flag would equal to 0  
		
		if( (65<=(int)c[i]&&(int)c[i]<=90) || (97<=(int)c[i]&&(int)c[i]<=122) ){    // when c[i] is between 97 and 122 or between 65 and 90 ¡C 
																					// Suppose the current value of c[i] is 'a': 97 
																					// Suppose the current value of c[i] is 'A': 65  
			
			for(int j=0;j<i;j++)  // Examine whether c[0]-c[i-1] has appeared before
				if( (int)c[i]==(int)c[j]+32 || (int)c[i]==(int)c[j] || (int)c[i]==(int)c[j]-32 ){    //  now 'a':97 => Judge whether it has appeared before 'a' & 'A'¡C  'a':(int)c[i]==(int)c[j] and 'A':(int)c[i]==(int)c[j]-32
																									 //  now 'A':65 => Judge whether it has appeared before 'A' & 'a'¡C  'A':(int)c[i]==(int)c[j] and 'a':(int)c[i]==(int)c[j]+32  
																									 //  So these judgments   (int)c[i]==(int)c[j]  ||  (int)c[i]==(int)c[j]-32 ||  (int)c[i]==(int)c[j]+32   are needed  
					flag=0;
					break;	
				}
			
			if(flag) ans++;
		}
	}
	
	printf("%d\n",ans);	
		
}
