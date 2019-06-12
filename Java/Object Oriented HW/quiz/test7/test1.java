class sum{
    private static int sum = 0;
    public static void add(int n){
        int tmp = sum;
        tmp = tmp +n;
        try{
            Thread.sleep((int)(1000*Math.random()));
        }
        catch (InterruptedException e){}
        sum = tmp;
        System.out.println("sum "+sum);
    }
}
class member extends Thread{
    public void run(){
        for(int i=1;i<=10;i++){
            sum.add(i);
        }
    }
}
public class test1{
    public static void main(String args[]) {
        member m1 = new member();
        member m2 = new member();

        try{
            m1.start();
            m1.join();
            m2.start();
        }catch (InterruptedException e){}

        
    }
}