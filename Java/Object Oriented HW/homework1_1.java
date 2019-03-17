import java.util.Scanner;

public class homework1_1{
    public static void main(String[] args) {
        int i=0,j=0;
        Scanner key = new Scanner(System.in);
        String[] data = key.nextLine().split(" ");
        int data_int[] = new int[3];
        for(int k=0;k<data_int.length;k++)
            data_int[k]=Integer.valueOf(data[k]);

        if(data_int[0] - data_int[2] < 1){
            i=i+data_int[0];
        }
        else{
            i=i+data_int[2]+1;
        }
        if(data_int[1] - data_int[2] < 1){
            j=j+data_int[1];
        }
        else{
            j=j+data_int[2]+1;
        }    
        if(data_int[0] + data_int[2] > 8){
            i=i+(8-data_int[0]);
        }
        else{
            i=i+data_int[2];
        }
        if(data_int[1] + data_int[2] > 8){
            j=j+(8-data_int[1]);
        }
        else{
            j=j+data_int[2];
        }   
        System.out.println(i*j);    
    }

}