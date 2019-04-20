#include <stdio.h>

// Reference:  https://www.youtube.com/watch?v=q6RicK1FCUs

/*
 fibonacci : 1,1,2,3,5,8,13,21,34,55......
 
 f(1)=f(2)=1
 f(3)= 2 = 1 + 1 
 f(4)= 3 = 1 + 2
 => f(n) = f(n-1) + f(n-2) 
 
int f(int n)
{
	if(n<=2) return 1;
	else return f(n-1)+f(n-2);
}
*/

int num=0;
void hanoi(int n,char A,char B,char C)  // This line can be seen as moving all the discs from the A-rod (that is, n) via the B-rod (because the larger disc can't place on top of the smaller) to the C-rod.¡A
										// The method is to put the largest disc from the A-rod to the C-rod, so that we can place others to C-rod. So all the discs on the largest disc (that is, n-1) must move to B-rod first.  
										// Then move the largest disc remaining on the A-rod to the C-rod, so increase one of the number of movement. 
										// Finally the n-1 discs on the B-rod are moved to the C-rod via the A-rod. 
										// hanoi(n,A,B,C) = hanoi(n-1,A,C,B) + (A->C) + hanoi(n-1,B,A,C); 
{ 
	
	if(n >0)  {  // Continue to do when there is a disc on the A-rod.
	 
		hanoi(n-1, A, C, B);  // Move n-1 discs to the B-rod (this line can be seen similar as the question that we want you to move n-1 discs from the A-rod to the B-rod),
							  // after n-1 discs are all moved to the B-rod. There is only the largest disc on the A-rod.
							  // Because n-1 discs contains large and small, it is impossible to move them directly to the B-rod without going through the C-rod.
							  
		printf("Move disk %d from %c to %c\n", n, A, C);  // The largest disc on the A-rod moves to the C-rod 
		++num; // Since A -> C only moves once, the number of moves plus 1 .
		
		hanoi(n-1, B, A, C); // Move the other n-1 discs from the B-rod to the C-rod will complete moving all discs from A-rod to C-rod. 
							//  This line can be seen similar as the question that we want you to move n-1 discs from the B-rod to the C-rod
		  
	} 
} 

int main() 
{ 
	int n; 
	printf("Enter the number of discs¡G"); 
	scanf("%d", &n); 
	printf("\n"); 
	hanoi(n, 'A', 'B', 'C'); 
	printf("\nThe minimum number of movement¡G %d",num); 
	 
} 



