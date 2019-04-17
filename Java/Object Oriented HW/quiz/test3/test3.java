import java.util.Scanner;
class test3{
    public static void main(String[] args) {
        Scanner key = new Scanner(System.in);
        Pascal test = new Pascal(Integer.valueOf(key.nextLine()));
        test.create();        
    }
}

class Pascal{
    public int N;
    public Pascal(int n){
        N=n;
    }
    public void create(){
        int[][] data=new int[N][N];
        data[0][0]=1;
        for(int i=1;i<N;i++){
            data[i][0]=data[i-1][0];
            data[i][i]=data[i-1][0];
            for(int j=1;j<i;j++){
                data[i][j]=data[i-1][j-1]+data[i-1][j];
            }
        }
        for(int i=0;i<N;i++){
            for(int j=0;j<i+1;j++){
                if(j==0){
                    for(int k=0;k<N-1-i;k++){
                        System.out.printf("  ");
                    }
                }
                System.out.printf("%2d  ",data[i][j]);
            }
            System.out.println();
        }
    }

}