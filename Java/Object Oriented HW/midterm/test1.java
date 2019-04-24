import java.util.Scanner;

public class test1{
    public static void main(String[] args) {
        int N,M;
        Scanner key = new Scanner(System.in);
        System.out.printf("Input the N:");
        N=key.nextInt();
        System.out.printf("Input the M:");
        M=key.nextInt();

        int count=1;
        int[][] data = new int[N][N];
        int row=0,col=0;
        if(M==0){
            for(row=0;row<N/2;row++){
                for(col=row;col<N-row-1;col++){
                    data[row][col]=count++;
                }
                for(col=row;col<N-row-1;col++){
                    data[col][N-row-1]=count++;
                }                
                for(col=N-row-1;col>row;col--){
                    data[N-row-1][col]=count++;
                }
                for(col=N-row-1;col>row;col--){
                    data[col][row]=count++;
                } 
            }
        }
        else{
            for(row=0;row<N/2;row++){
                for(col=row;col<N-row-1;col++){
                    data[col][row]=count++;
                }
                for(col=row;col<N-row-1;col++){
                    data[N-row-1][col]=count++;
                }                
                for(col=N-row-1;col>row;col--){
                    data[col][N-row-1]=count++;
                }
                for(col=N-row-1;col>row;col--){
                    data[row][col]=count++;
                } 
            }
        }

        if(N%2!=0){
            data[N/2][N/2]=count++;
        }
        for(row=0;row<N;row++){
            for(col=0;col<N;col++){
                System.out.printf("%2d ",data[row][col]);
            }
            System.out.println();
        }
        
    }
}