import java.util.Scanner;

public class test2{
    public static void main(String[] args) {
        Scanner key1 = new Scanner(System.in);
        Scanner key2 = new Scanner(System.in);
        int a=key1.nextInt();
        int b=key2.nextInt();
        int g[]=new int[2];
        g[0]=a;
        g[1]=b;

        if(a!=0 && b!=0){
            gcdname w=new gcdname();
            /*
            System.out.println(w.gcd(g)[0]);
            System.out.println(w.gcd(g)[1]);
            
            while(a!=1 && b!=1 && a!=0 && b!=0){
                if(a>=b){
                    a=a%b;
                }
                else{
                    b=b%a;
                }
            }
            */
            a=w.gcd(g)[0];
            b=w.gcd(g)[1];
            if(a==0)
            {
                System.out.println(b);
            }
            else if(b==0)
            {
                System.out.println(a);
            }
            else{
                System.out.println(1);
            }
        }
        else{
            System.out.println("Error");
        }

       
    }
   

}