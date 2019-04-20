#include<stdlib.h>
#include<stdio.h>

int main(){
	int N,al;
	int i,j,k,l,h,m;
	printf("叫块N\n");
	scanf("%d", &N);
	printf("叫块A\n");
	scanf("%d",&al);
	
	
	for(i=0;i<2*al-1;i++){       //北–row 
		
		if (i < al-1){           //耞琌ぃ琌タà 
			for(l=0; l<N;l++){   // 北璶暗碭タà 
			
				for (j=0; j< al-i-1;j++){ //タàオ娩フ 
				printf(" ");
				}
				for(k=0; k< 2*i+1;k++){   //à 
					printf("*");
				}
				for (j=0; j< 3*al-i-2;j++){ //à娩フ 
					printf(" ");
				}
				
			}
			
			printf("\n");	
		}
		
		else if( i == al -1){      // 猧x禸赣row场常琌琍琍耞琌x禸 
			for(l=0; l<N;l++){     //猧计 
				for (j=0; j<2*(2*al-1);j++) //N猧2琍琍 
					printf("*");           
					
			}
			
			printf("\n");         //传︽ 
		}
		else if (i > al -1 ){    //耞琌ぃ琌à 
			
			for(l=0; l<N;l++){   //北猧计 
				
				for (j=0; j< al+i ;j++){   //à娩フ 
				printf(" ");
				}
			
				for(k=0; k< 4*al-2*i-3;k++){  //à 
					printf("*");       
				}
				for (j=0; j< i-al+1 ;j++){   //à娩フ 
					printf(" ");
				}
				
				
			}
			
			printf("\n");        //传︽ 
			
		}
		
		
		
		
	}
	

	return 0;
}

