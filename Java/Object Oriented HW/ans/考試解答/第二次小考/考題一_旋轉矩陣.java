
import java.util.*;


public class ratation_matrix {
	
	public static void main(String[] args) {
		int N, M;
		int count=1;
		Scanner scn = new Scanner(System.in);
		System.out.printf("輸入矩陣大小");
		N = scn.nextInt();
		System.out.printf("輸入方向，0:順時針；1:逆時針");
		M = scn.nextInt();
		int[][] array = new int[N][N];
		
		if (M == 0) {
			
			for (int row=0; row < N/2 ; row++) {		/*控制繞圈次數*/
				for(int col=row; col< N-row-1; col++)	/*向右*/
					array[row][col] = count++;
				
				for (int col=row; col < N-row-1;col++)	/*向下*/
					array[col][N-row-1]=count++;
				
				for(int col=N-row-1; col>row; col--)	/*向左*/
					array[N-row-1][col]=count++;
				for (int col=N-row-1; col>row; col--)	/*向上*/
					array[col][row]=count++;
			}
		}
		else {
			for (int row=0; row <N/2; row++) {
				for (int col=row; col< N-row-1; col++)
					array[col][row]=count++;
				
				for (int col=row; col< N-row-1;col++)
					array[N-row-1][col]=count++;
				
				for(int col=N-row-1; col>row; col--)
					array[col][N-row-1]=count++;
				for (int col=N-row-1; col>row; col--)
					array[row][col]=count++;
			}
		
		}
		if (N%2 != 0)			/*矩陣大小為奇數，必須補上中心點*/
			array[N/2][N/2] = count;
		
		for(int row=0; row<N; row++) { 		/*印出矩陣*/
			for(int col=0; col<N;col++) {
				System.out.printf("%2d",array[row][col]);
				System.out.printf(" ");
				
			}
			System.out.println();
				
		
		}
		
	}			
}
