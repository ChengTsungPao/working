import java.util.Random;

class practice3{
    public static void main(String args[]) {

        Random dice = new Random();
        int num;
        for(int count=1;count<=10;count++){
            num = dice.nextInt(6)+1;
            System.out.printf("Random of %2d number:%d\n",count,num);
        }
    } 
}