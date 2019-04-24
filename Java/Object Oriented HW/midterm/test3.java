import java.util.Scanner;

public class test3{
    public static void main(String[] args) {
        Scanner N = new Scanner(System.in);
        Student a = new Student(N.nextInt());
        a.show();
        
    }
}

class Teacher{
    protected char ch;
    private int number;
    public Teacher(int a){
        number = a;
    }
    public void show(){
        System.out.printf("The destination of the %dth move is %c-rod.",number,ch);

    }

}
class Student extends Teacher{
    public int count=0,k;
    public Student(int v){
        super(v);
        k=v;
        hanoi(5,'A','B','C');
    }
    public void hanoi(int n,char a,char b,char c){
        if(n!=1){
            hanoi(n-1,a,c,b);
            //System.out.printf("%d %c %c\n",n,a,c);
            count++;
            if(k==count){
                //System.out.println("here");
                ch=c;
            }
            hanoi(n-1,b,a,c);
        }
        else{
            //System.out.printf("%d %c %c\n",n,a,c);
            count++;
            if(k==count){
                //System.out.println("here");
                ch=c;
            }            
        }
    }
}