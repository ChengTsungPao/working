#include<stdlib.h>
#include<stdio.h>

int main(){
	int N,al;
	int i,j,k,l,h,m;
	printf("�п�JN\n");
	scanf("%d", &N);
	printf("�п�JA\n");
	scanf("%d",&al);
	
	
	for(i=0;i<2*al-1;i++){       //����C�@row 
		
		if (i < al-1){           //�P�_�O���O�L�����T���� 
			for(l=0; l<N;l++){   // ����n���X�ӥ����T���� 
			
				for (j=0; j< al-i-1;j++){ //���T���Υ��䪺�ť� 
				printf(" ");
				}
				for(k=0; k< 2*i+1;k++){   //�L�X�T���� 
					printf("*");
				}
				for (j=0; j< 3*al-i-2;j++){ //�T���Υk�䪺�ť� 
					printf(" ");
				}
				
			}
			
			printf("\n");	
		}
		
		else if( i == al -1){      // �b�i��x�b�W�A��row�������O�P�P�A�P�_�O�_��x�b 
			for(l=0; l<N;l++){     //�i�� 
				for (j=0; j<2*(2*al-1);j++) //N�Ӫi�A�L2���P�P 
					printf("*");           
					
			}
			
			printf("\n");         //���� 
		}
		else if (i > al -1 ){    //�P�_�O���O�˪��T���� 
			
			for(l=0; l<N;l++){   //����i�� 
				
				for (j=0; j< al+i ;j++){   //�ˤT���Υk�䪺�ť� 
				printf(" ");
				}
			
				for(k=0; k< 4*al-2*i-3;k++){  //�L�X�ˤT���� 
					printf("*");       
				}
				for (j=0; j< i-al+1 ;j++){   //�ˤT���Υk��ť� 
					printf(" ");
				}
				
				
			}
			
			printf("\n");        //���� 
			
		}
		
		
		
		
	}
	

	return 0;
}

