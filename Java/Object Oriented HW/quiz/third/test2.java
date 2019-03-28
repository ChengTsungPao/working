import java.util.Scanner;
class test2
{
    public static void main(String[] args) {
        Scanner key1 = new Scanner(System.in);
        Scanner key2 = new Scanner(System.in);
        test2 test = new test2(Integer.valueOf(key1.nextLine()),Integer.valueOf(key2.nextLine()));    
        test.draw();
        
    }
    public int a;
    public int b;
    public test2(int N, int M){
        a=N;
        b=M;
    }
    public void draw(){
        for(int i=0;i<a;i++){
            for(int j=1;j<=b;j++){
                if(i%2==0){
                    System.out.printf("%2d ",i*b+j);
                }
                else{
                    System.out.printf("%2d ",i*b+(b-j+1));
                }
                
            }
            System.out.println();
        }


    }
}

