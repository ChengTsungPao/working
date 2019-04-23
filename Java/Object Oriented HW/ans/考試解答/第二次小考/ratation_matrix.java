
import java.util.*;


public class ratation_matrix {
	
	public static void main(String[] args) {
		int N, M;
		int count=1;
		Scanner scn = new Scanner(System.in);
		System.out.printf("Input the N:");
		N = scn.nextInt();
		System.out.printf("Input the M:");
		M = scn.nextInt();
		int[][] array = new int[N][N];
		
		if (M == 0) {
			
			for (int row=0; row < N/2 ; row++) {		/*����¶�馸��*/
				for(int col=row; col< N-row-1; col++)	/*�V�k*/
					array[row][col] = count++;
				
				for (int col=row; col < N-row-1;col++)	/*�V�U*/
					array[col][N-row-1]=count++;
				
				for(int col=N-row-1; col>row; col--)	/*�V��*/
					array[N-row-1][col]=count++;
				for (int col=N-row-1; col>row; col--)	/*�V�W*/
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
		if (N%2 != 0)			/*�x�}�j�p���_�ơA�����ɤW�����I*/
			array[N/2][N/2] = count;
		
		for(int row=0; row<N; row++) { 		/*�L�X�x�}*/
			for(int col=0; col<N;col++) {
				System.out.printf("%2d",array[row][col]);
				System.out.printf(" ");
				
			}
			System.out.println();
				
		
		}
		
	}			
}
