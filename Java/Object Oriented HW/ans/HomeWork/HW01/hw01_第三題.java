
import java.util.Scanner;
import java.lang.*;

public class hw01 
{
	
	public static void main(String[] args)
	{
		int int1, int2;
        Scanner scanner = new Scanner(System.in);
        System.out.printf("Please input the shape of the game and the number of mines. \n");
        int1 = scanner.nextInt();
        int2 = scanner.nextInt();
//        System.out.printf("input:%d,%d\n", int1, int2);
        

        for (int i=0; i<int1; i++)
        {
        	for (int j=0; j<int1; j++)
	        {
        		System.out.printf("* ");
	        }
        	System.out.printf("\n");
        }
        int[][] checkerboard = mines(int1, int2);
        int[][] showboard = new int[int1+2][int1+2];
        for (int i=0; i<=int1+1; i++)
        	for (int j=0; j<=int1+1; j++)
        		if(i==0||i==int1+1 || j==0||j==int1+1)
        			showboard[i][j] = 1;
        
        while(true)
        {
    	System.out.printf("Input coordinate:\n");
        int _x = scanner.nextInt();
        int _y = scanner.nextInt();
    	int re = demolish(checkerboard, showboard, _x, _y, int1);
    	int bombs = 0;
    	
//        for (int i=0; i<=int1+1; i++)
//        {
//        	for (int j=0; j<=int1+1; j++)
//        		System.out.printf("%d ",checkerboard[i][j]);
//        	System.out.printf("\n");
//        }
//        System.out.printf("\n");
//        for (int i=0; i<=int1+1; i++)
//        {
//        	for (int j=0; j<=int1+1; j++)
//        		System.out.printf("%d ",showboard[i][j]);
//        	System.out.printf("\n");
//        }
//        System.out.printf("\n");
    	
    	
    	if(re == 0) // GameOver!!
    	{
	        for (int i=1; i<=int1; i++)
	        {
	        	for (int j=1; j<=int1; j++)
	        		if(showboard[i][j]==1)
	        			System.out.printf("%d ",checkerboard[i][j]);
	        		else if(checkerboard[i][j]==9)
	        			System.out.printf("X ");
	        		else
	        		{
	        			System.out.printf("* ");
	        			bombs++;
	        		}
	        	System.out.printf("\n");
	        }
            System.out.printf("Game Over!\n");
    		break;
    	}
    	else
    	{
	        for (int i=1; i<=int1; i++)
	        {
	        	for (int j=1; j<=int1; j++)
	        		if(showboard[i][j]==1)
	        			System.out.printf("%d ",checkerboard[i][j]);
	        		else
	        		{
	        			System.out.printf("* ");
	        			bombs++;
	        		}
	        	System.out.printf("\n");
	        }
	        if(bombs==int2)
	        {
	        	System.out.printf("Winner!!");
	        	break;
	        }
    	}
        }
//        scanner.close();
	} //End main()
	
	public static int demolish(int[][] board, int[][] showboard, int _x, int _y, int int1)
	{
		if(board[_x][_y] == 9)
		{
			return 0;
		}
		else if(board[_x][_y] == 0)
		{
			showboard[_x][_y] = 1;
			diffusion(board, showboard, _x, _y);
		}
		else
			showboard[_x][_y] = 1;
		return 1;
	}
	public static void diffusion(int[][] board, int[][] showboard, int _x, int _y)
	{
		// not edge
		for(int i=_x-1; i<=_x+1; i++)
			for(int j=_y-1; j<=_y+1; j++)
				if(showboard[i][j]==0 && board[i][j]==0)
				{
					showboard[i][j] = 1;
//					System.out.printf("%d, %d\n", i,j);
					diffusion(board, showboard, i, j);
				}
				else
					showboard[i][j] = 1;
	}
	
	public static int[][] mines(int shape,int _mines)
	{
        int[] mines_rand = new int[shape*shape];
        int[] mines = new int[_mines];
        int[][] checkerboard = new int[shape+2][shape+2];
        int n = 0;
        for (int i=0; i<shape*shape; i++)
        	mines_rand[i] = i;
        
        for (int i=0; i<_mines; i++)
        {
        	n = (int)(Math.random()*(shape*shape-i));
//        	System.out.printf("%d, %d\n", n,mines_rand[n]);
        	int _x = mines_rand[n]/shape+1;
        	int _y = mines_rand[n]%shape+1;
//        	System.out.printf("%d, %d\n", _x,_y);
        	checkerboard[_x][_y] = 9;
        	for (int j =n; j<mines_rand.length-(i+1);j++)
        		mines_rand[j]=mines_rand[j+1];
        }
        
        for(int i=1; i<=shape ;i++)
        {
        	for(int j=1; j<=shape ;j++)
            {
        		if(checkerboard[i][j]==0)
        		{
        			for (int ii=i-1; ii<=i+1; ii++)
        				for (int jj=j-1; jj<=j+1; jj++)
        					if (checkerboard[ii][jj] == 9)
        						checkerboard[i][j] ++;  
        		}
            }
        }
        

		return checkerboard;
	}
	
} //End class main



