import java.util.ArrayList;

public class test2{
    public static void main(String[] args) {
        A a = new A("a");
        A b = new A("b");
        A c = new A("c");
        A d = new A("d");
        a.start();
        b.start();
        c.start();
        d.start();
        
    }
}

class A extends Thread{
    String name;
    public A(String str){
        name = str;
    }
    public void run(){
        B.lineup(name);
    }
}

class B{
    private static ArrayList<String> people = new ArrayList<String>();
    public synchronized static void lineup(String name){
        people.add(name);
        for(String x:people){
            System.out.printf("%s ",x);
        }
        System.out.println();
    }
}