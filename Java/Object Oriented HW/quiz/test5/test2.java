//package college;
import java.util.Scanner;

public class test2{
    public static void main(String args[]) {
        Compute com1 = new Compute();
        Compute com2 = new Compute();
        com1.mul1();
        com1.show();
        com1.a=7;
        com2.mul1();
        com2.show();        
    }

}

class Math{
    protected final double pi=3.14;
    protected double ans;

    public void show(){
        System.out.println("ans="+ans);
    }
}
class Compute extends Math{
    int pi=5;
    public static int a = 3;
    public static int b = 11; 

    public void mul1(){        
        ans = a*b*super.pi;
    }
    public void mul2(){
        ans = a*b*pi;
    }

}