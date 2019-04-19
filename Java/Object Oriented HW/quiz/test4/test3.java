import java.util.Scanner;

public class test3{
    public static void main(String[] args) {
        Scanner N = new Scanner(System.in);
        Student a = new Student(N.nextInt());
        a.show();
        
    }
}
class Teacher{
    char ch;

    private int number;

    public Teacher(int a){
        number = a;        
    }
    public void show(){
        System.out.println();   

    }
}
class Student extends Teacher{  
    Teacher t;  
    public Student(int v){
        super(v);
        t=new Teacher(v); 
        
        hanoi(5,'A','B','C');
    }
    public void hanoi(int n,char a,char b,char c){     
        
        if(n>1){          
            hanoi(n-1,a,c,b);  
            System.out.println("Move disc "+n+" from "+a+" to "+c);              
            hanoi(n-1,b,a,c);                 
        }
        else if(n==1){
            System.out.println("Move disc "+n+" from "+a+" to "+c);      
        }
              
    }
}