import java.util.Scanner;

abstract class parent{
    public abstract void show();
}

class child extends parent{
    protected int a;
    child(int n){
        a=n;
    }
    public void show(){
        for(int i=0;i<a;i++){
            for(int j=0;j<a-i+1;j++){
                System.out.printf(" ");
            }
            for(int j=0;j<2*i+1;j++){
                System.out.printf("*");
            }
            System.out.println();
            for(int j=0;j<a-i-1;j++){
                System.out.printf(" ");
            }
            for(int j=0;j<2*(i+2)+1;j++){
                System.out.printf("*");
            }
            System.out.println();
            
        }
        for(int i=0;i<a+1;i++){
            System.out.printf(" ");
        }
        System.out.printf("*\n");
        for(int i=0;i<a+1;i++){
            System.out.printf(" ");
        }
        System.out.printf("*\n");

    }   


}

public class test1{
    public static void main(String args[]) {
        Scanner sc = new Scanner(System.in);
        System.out.printf("input\n");
        int A;
        A = sc.nextInt();
        child ch = new child(A);
        ch.show();        
    }
}