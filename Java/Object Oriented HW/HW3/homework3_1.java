import java.util.Scanner;

abstract class parent{

    protected int n;

    public parent(int a){
        n = a;
    }

    public abstract int[][] method();

    public void show(int a [][]){
        for(int i=0;i<n;i++){
            for(int j=0;j<n;j++)
                System.out.printf("%4d",a[i][j]);            
            System.out.println();
            }
    }
}

class hw03_1 extends parent{

    public hw03_1(int N){
        super(N);
    }

    public int[][] method(){
        int count=1;  
        int[][] data = new int[n][n];        
        for(int row=0;row<n/2;row++){
            for(int col=row;col<n-row-1;col++){
                data[row][col]=count++;
            }
            for(int col=row;col<n-row-1;col++){
                data[col][n-row-1]=count++;
            }                
            for(int col=n-row-1;col>row;col--){
                data[n-row-1][col]=count++;
            }
            for(int col=n-row-1;col>row;col--){
                data[col][row]=count++;
            } 
        }
        data[n/2][n/2]=count++;
        return data;
    }

}

class hw03_2 extends parent{

    public hw03_2(int N){
        super(N);
    }

    public int[][] method(){
        int count=n*n;  
        int[][] data = new int[n][n];        
        for(int row=0;row<n/2;row++){
            for(int col=n-row-1;col>row;col--){
                data[row][col]=count--;
            } 
            for(int col=row;col<n-row-1;col++){
                data[col][row]=count--;
            }
            for(int col=row;col<n-row-1;col++){
                data[n-row-1][col]=count--;
            }                
            for(int col=n-row-1;col>row;col--){
                data[col][n-row-1]=count--;
            }

        }
        data[n/2][n/2]=count--;
        return data;
    }
    
}

public class homework3_1{
    public static void main(String args[]) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Input N value");
        int N = sc.nextInt();//N is an odd number
        hw03_1 matrix = new hw03_1(N);
        int [][] b = matrix.method();
        matrix.show(b);
        System.out.println();

        hw03_2 m = new hw03_2(N);
        int [][]c = m.method();
        m.show(c);        
    }
}