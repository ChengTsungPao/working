#include<stdio.h>
#include<stdlib.h>
#include<time.h>

// 'a' - 'z' : 97 -122    'A' - 'Z' : 65-90
int main(){
	
	char c[1000];
	int flag,ans=0;   // flag �P�_�ӭ^��r�����e�O�_���X�{�L 
	
	/* ������l�ơA�קK�}�C���|���b a-z & A-Z ���r�� */
	for(int i=0;i<1000;i++) 	
	c[i]='0';
	
	printf("Enter:");
	gets(c);   // �i�����Ҧ���J�]�A�ť� 
	
	for(int i=0;i<1000;i++){
		
		flag=1;   // flag=1 ���e�r���S�X�{�L�֥[�_�h���� 0  
		
		if( (65<=(int)c[i]&&(int)c[i]<=90) || (97<=(int)c[i]&&(int)c[i]<=122) ){    // �� c[i] ���� 97-122 & 65-90  �����ثe c[i] ���Ȭ� 'a':97 �U���ӭȬ� 'A':65 
			
			for(int j=0;j<i;j++) // �ˬd c[0]-c[i-1] ���e�O�_���X�{�L 
				if( (int)c[i]==(int)c[j]+32 || (int)c[i]==(int)c[j] || (int)c[i]==(int)c[j]-32 ){    //  now 'a':97 => �ҥH�n�P�_���e�O�_�X�{�L 'a' & 'A'�C  'a':(int)c[i]==(int)c[j] �H��   'A':(int)c[i]==(int)c[j]-32
																									 //  now 'A':65 => �ҥH�n�P�_���e�O�_�X�{�L 'A' & 'a'�C  'A':(int)c[i]==(int)c[j] �H��   'a':(int)c[i]==(int)c[j]+32  
																									 //  �ҥH�ݭn  (int)c[i]==(int)c[j]  ||  (int)c[i]==(int)c[j]-32 ||  (int)c[i]==(int)c[j]+32   �o�ǧP�_��  
					flag=0;
					break;	
				}
			
			if(flag) ans++;
		}
	}
	
	printf("%d\n",ans);	
		
}
