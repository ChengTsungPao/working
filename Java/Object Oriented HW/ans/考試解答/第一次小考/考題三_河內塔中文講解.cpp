#include <stdio.h>

// 可以參考此網址  https://www.youtube.com/watch?v=q6RicK1FCUs

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
void hanoi(int n,char A,char B,char C)  // 此行可以看成將 A桿上的所有盤子 (也就是 n 個) 經由 B桿(因為有大盤子不能在小牌子上的規定，所以勢必得經過 B桿) 才能移動到 C桿子上 ，
										// 想法是將 A桿上最大的盤子必須先放入 C桿上才能放其他的小盤子，所以最大盤子之上的所有盤子 (也就是 n-1 個) 都得先到 B桿上 。  
										// 再將剩餘在 A 盤上的最大盤子移到 C桿，因為移ㄧ次所以次數加 1 。最後將 n-1 個在 B桿子上的盤子經由 A桿移動到 C桿。 
										// hanoi(n,A,B,C) = hanoi(n-1,A,C,B) + (A->C) + hanoi(n-1,B,A,C); 
{ 
	
	if(n >0)  {  // 當 A桿上還有盤子就繼續做
	 
		hanoi(n-1, A, C, B);  // 將 n-1 個盤子移動到 B桿上 (此行可以看成題目要你移動 n-1個在 A桿上的盤子要移動到 B桿 )，n-1 個盤子全部移動到 B桿上後就只剩下最大的盤子在 A桿上 。
							  // 因為 n-1 個盤子中有大有小，所以不可能不經過 C桿直接將他們移動到 B桿上
							  
		printf("Move disk %d from %c to %c\n", n, A, C);  // A 桿子上的最大盤子移動到 C桿子上 
		++num; // 因為 A -> C 只有移動ㄧ次，所以移動次數 +1 
		
		hanoi(n-1, B, A, C); // 在將 n-1 個在 B桿上的盤子全部移動到 C桿子上，完成所有在 A桿上的盤子移動到 C桿。 (同理此行可以看成題目要你移動 n-1個在 B桿上的盤子要移動到 C桿)
		  
	} 
} 
int main() 
{ 
	int n; 
	printf("輸入盤子數量："); 
	scanf("%d", &n); 
	printf("\n"); 
	hanoi(n, 'A', 'B', 'C'); 
	printf("\n最少移動次數： %d",num);
} 


