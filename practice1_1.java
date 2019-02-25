import java.util.Scanner;
import java.util.Random;

class practice1{
    public static void main(String args[]) {
        practice1_2 practiceObject = new practice1_2();
        Scanner key = new Scanner(System.in);
        String name;
        System.out.print("\nInput your name:");
        name = key.nextLine();
        practiceObject.practiceMessage(name);
    } 
}