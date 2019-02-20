import java.util.Scanner;

class div{
    public static void main(String args[]){
        Scanner key = new Scanner(System.in);
        double answer,a,b;
        System.out.print("Input the first  number:");
        a = key.nextDouble();
        System.out.print("Input the second number:");
        b = key.nextDouble();
        answer=a/b;
        System.out.print("a/b = ");
        System.out.println(answer);
    }
}