import java.util.Scanner;

public class homework1_1{
    public static void main(String[] args) {
        int i=0,j=0;
        Scanner key = new Scanner(System.in);
        String[] data = key.nextLine().split(" ");
        if(Integer.valueOf(data[0]) - Integer.valueOf(data[2]) < 1){
            i=i+Integer.valueOf(data[0]);
        }
        else{
            i=i+Integer.valueOf(data[2])+1;
        }
        if(Integer.valueOf(data[1]) - Integer.valueOf(data[2]) < 1){
            j=j+Integer.valueOf(data[1]);
        }
        else{
            j=j+Integer.valueOf(data[2])+1;
        }    
        if(Integer.valueOf(data[0]) + Integer.valueOf(data[2]) > 8){
            i=i+(8-Integer.valueOf(data[0]));
        }
        else{
            i=i+Integer.valueOf(data[2]);
        }
        if(Integer.valueOf(data[1]) + Integer.valueOf(data[2]) > 8){
            j=j+(8-Integer.valueOf(data[1]));
        }
        else{
            j=j+Integer.valueOf(data[2]);
        }   
        System.out.println(i*j);    
    }

}