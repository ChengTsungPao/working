import java.util.Scanner;

class parent{
    public int height;

    public void show(){
        for(int i=0;i<height;i++){
            System.out.printf("*");
        }
    }
}
class child extends parent{
    
    public child(int a){
        height=a;        
    }
    public void show(){
        int tmp = (height+1)/2;
        for(int i=1;i<=tmp;i++){
            for(int j=1;j<=i;j++){
                System.out.printf("%d",j);
            }
            System.out.println();
        }
        for(int i=1;i<tmp;i++){
            for(int j=1;j<=tmp-i;j++){
                System.out.printf("%d",j);
            }
            System.out.println();
        }

    }
}
public class test1{
    public static void main(String args[]) {
        int N;
        Scanner sc = new Scanner(System.in);
        System.out.printf("please enter the odd number N\n");
        N=Integer.valueOf(sc.nextLine());
        child ch = new child(N);
        ch.show();
        
    }
}
