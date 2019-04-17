public class test{
    public static void main(String[] args) {
        test t=new test();
        System.out.println(t.sum(1, 2));
        System.out.println(t.series(10));  
        System.out.println(((char)97));      
    }

    public int sum(int a,int b) {
        return a+b;        
    }

    public int series(int a){
        if(a==1 || a==2){
            return 1;
        }
        else{
            return series(a-1)+series(a-2);
        }
    }
}