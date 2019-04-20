#include <stdio.h>

// �i�H�ѦҦ����}  https://www.youtube.com/watch?v=q6RicK1FCUs

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
void hanoi(int n,char A,char B,char C)  // ����i�H�ݦ��N A��W���Ҧ��L�l (�]�N�O n ��) �g�� B��(�]�����j�L�l����b�p�P�l�W���W�w�A�ҥH�ե��o�g�L B��) �~�ಾ�ʨ� C��l�W �A
										// �Q�k�O�N A��W�̤j���L�l��������J C��W�~����L���p�L�l�A�ҥH�̤j�L�l���W���Ҧ��L�l (�]�N�O n-1 ��) ���o���� B��W �C  
										// �A�N�Ѿl�b A �L�W���̤j�L�l���� C��A�]���������ҥH���ƥ[ 1 �C�̫�N n-1 �Ӧb B��l�W���L�l�g�� A�첾�ʨ� C��C 
										// hanoi(n,A,B,C) = hanoi(n-1,A,C,B) + (A->C) + hanoi(n-1,B,A,C); 
{ 
	
	if(n >0)  {  // �� A��W�٦��L�l�N�~��
	 
		hanoi(n-1, A, C, B);  // �N n-1 �ӽL�l���ʨ� B��W (����i�H�ݦ��D�حn�A���� n-1�Ӧb A��W���L�l�n���ʨ� B�� )�An-1 �ӽL�l�������ʨ� B��W��N�u�ѤU�̤j���L�l�b A��W �C
							  // �]�� n-1 �ӽL�l�����j���p�A�ҥH���i�ण�g�L C�쪽���N�L�̲��ʨ� B��W
							  
		printf("Move disk %d from %c to %c\n", n, A, C);  // A ��l�W���̤j�L�l���ʨ� C��l�W 
		++num; // �]�� A -> C �u�����ʣ����A�ҥH���ʦ��� +1 
		
		hanoi(n-1, B, A, C); // �b�N n-1 �Ӧb B��W���L�l�������ʨ� C��l�W�A�����Ҧ��b A��W���L�l���ʨ� C��C (�P�z����i�H�ݦ��D�حn�A���� n-1�Ӧb B��W���L�l�n���ʨ� C��)
		  
	} 
} 
int main() 
{ 
	int n; 
	printf("��J�L�l�ƶq�G"); 
	scanf("%d", &n); 
	printf("\n"); 
	hanoi(n, 'A', 'B', 'C'); 
	printf("\n�ֲ̤��ʦ��ơG %d",num);
} 


