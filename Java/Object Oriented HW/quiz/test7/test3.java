interface SHOW_FUCN{
    void odd(int N);
    void even(int N);
}
class test3{
    public static void main(String args[]) {
        SHOW show = new SHOW();
        ODD odd = new ODD(show);
        EVEN even = new EVEN(show);
        Thread t_odd = new Thread(odd);
        Thread t_even = new Thread(even);
        t_odd.start();
        t_even.start();        
    }
}

class SHOW implements SHOW_FUCN{
    static int flag=-1;
    public synchronized void odd(int n){
        
        while(flag==1){
            try {                 
                wait();                      
            } catch (InterruptedException e) {}
        }
        System.out.println("odd :"+n); 
        flag = flag*(-1);
        notify();

    }
    public synchronized void even(int n){
        
        while(flag==-1){
            try {                
                wait();            
            } catch (InterruptedException e) {}
        }
        System.out.println("even:"+n);
        flag = flag*(-1);
        notify();

    }
}

class ODD implements Runnable{
    SHOW sh;
    public ODD(SHOW show){
        sh = show;
    }
    public void run(){
        for(int i=1;i<=10;i=i+2){
            sh.odd(i);
        }
    }
}

class EVEN implements Runnable{
    SHOW sh;
    public EVEN(SHOW show){
        sh = show;
    }
    public void run(){
        for(int i=2;i<=10;i=i+2){
            sh.even(i);
        }
    }
}
