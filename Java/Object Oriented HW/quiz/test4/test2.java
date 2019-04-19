import java.util.Scanner;

class test2{
    public static void main(String args[]) {
        Scanner scn_int = new Scanner(System.in);
        System.out.printf("Please input two values:\n");
        int d1 = scn_int.nextInt();
        int d2 = scn_int.nextInt();
        A a1 = new A();
        A a2 = new A();
        a1.set_B(d1);
        a2.set_B(d2);
        C c = new C();
        int sub = c.substract(a1, a2);
        System.out.printf("%d\n",sub);
        scn_int.close();   

        
    }
}
class A{
    private B b = new B();
    public void set_B(int vv){
        b.set(vv);
    }
    public int get_B(){
        return b.get();
    }
    private class B{
        private int tmp;
        public void set(int vv){
            tmp=vv;
        }
        public int get(){
            return tmp;
        }
    }
}
class C{
    public int substract(A a1,A a2){
        return (a1.get_B()-a2.get_B());
    }
}