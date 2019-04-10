import java.util.Scanner;

class card{

    private static int remain = 100;
    private String number;

    public card(String number){
        this.remain=remain;
        this.number=number;
    }

    public void store(int add){
        if(add>0){
            remain+=add;
        }
        else{
            System.out.println("error");
        }
    }

    public void charge(int sub){
        if(sub>0 && remain-sub>=0){
            remain-=sub;
        }
        else{
            System.out.println("error");
        }

    }

    public static void getRemain(){
        System.out.println(remain);
    }
    
}

public class homework2_2{
    public static void main(String[] args) {
        Scanner sca = new Scanner(System.in);
        System.out.print("Input user id : ");
        card aa = new card(sca.next());
        System.out.print("Input stored value : ");        
        aa.store(sca.nextInt());
        System.out.print("Input charged value : ");
        aa.charge(sca.nextInt());
        card.getRemain();
        
    }
}
