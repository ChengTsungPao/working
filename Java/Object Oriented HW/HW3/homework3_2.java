class homework3_2{
    public static void main(String args[]) {
        BBB b = new BBB(0);
        b.show();
    }
}
abstract class AAA{
    protected int num1 = 10;
    AAA(int x){
        if(x<3)
            System.out.println("constructor: You cannot print this line");
    }
    void func_1(){
        System.out.println("func_1: You cannot print this line");
    }
    abstract void func_2();
    private void func_3(){
        if(num1>0){
            System.out.println("func_3: You cannot print this line");
        }
    }
    final void show(){
        func_1();
        func_2();
        func_3();
    }
}

class BBB extends AAA{

    public BBB(int n){
        super(3);
    }
    public void func_1(){
        num1 = -1;
    }
    public void func_2(){
        num1 = -1;
    }

}