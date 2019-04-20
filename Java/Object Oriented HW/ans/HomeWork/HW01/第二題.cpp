#include<stdio.h>
#include<stdlib.h>

int main()
{
	
	int n=4,h=8;
	int k,l=65;
	
	for(int i=0;i<2*h-1;i++)
	{
		
		for(int j=0;j<n*(2*h-1+3);j++)
		{
			
			k=j%(2*h-1+3);	
			if(k<2*h-1)
			{
				if( i+k==h-1 || i+k==3*h-3 || i-k== -(h-1) || i-k==h-1 )printf("*");
				else if( i>1 && i<2*h-1-2 && k>1 && k<2*h-1-2 && (i+k==h-1+2 || i+k==3*h-3-2 || i-k== -(h-1)+2 || i-k==h-1-2)  )printf("o");
				else printf(" ");
			}
			else 
			{
				if(i==h-1)printf("%c",l++);
				else printf(" ");
			}
		}
		printf("\n");
	}
	
	
}





