import java.util.Scanner;
import java.util.Random;

class apples{
    public static void main(String args[]) {
        tuna tunaObject = new tuna();
        Scanner key = new Scanner(System.in);
        String name;
        System.out.print("\nInput your name:");
        name = key.nextLine();
        tunaObject.tunaMessage(name);
    } 
}