import java.util.Scanner;

public class test3{
    public static void main(String args[]) {
        Scanner scn1 = new Scanner(System.in);
        System.out.println("Input two numbers");
        int N = scn1.nextInt();
        int M = scn1.nextInt();
        Func func1 = new Func();

        try{
            func1.div1(N,M);
        }catch (Exception e) {
            float result = (float)N/(float)M;
            System.out.printf("result: %f",result);
        } 
        

        scn1.close();
        
    }
}

class Func{
    final void div1(int N,int M) throws Exception{
        float result = N/M/0;
        System.out.printf("result: %f",result);
    }
}