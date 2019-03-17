import java.util.ArrayList;
import java.util.Random;

public class homework1_3{
    public static void main(String[] args) {
        int size = 5;
        int mines = 3;
        int choose;
        int map[] = new int[size*size];
        Random rd = new Random();
        ArrayList<Integer> arr = new ArrayList<Integer>(size*size);
        for(int i=0;i<size*size;i++){
            arr.add(i);
        }
        for(int i=0;i<mines;i++){
            choose = rd.nextInt(arr.size());
            map[arr.get(choose)] = -1;
            arr.remove(choose);            
        }        
        /*for(int x:arr){
            System.out.printf("%d ",x);
        }
        System.out.println();
        for(int x:map){
            System.out.printf("%d ",x);
        }
        System.out.println();*/

        int map_2D[][] = new int[size][size];
        for(int i=0;i<map.length;i++){
            map_2D[i/size][i%size] = map[i];
        }
        for(int i=0;i<size;i++){
            for(int j=0;j<size;j++){
                if(map_2D[i][j]==-1){
                    map_2D[i+1][j] = map_2D[i][j] + 1;
                    map_2D[i][j+1] = map_2D[i][j] + 1;
                    map_2D[i-1][j] = map_2D[i][j] + 1;
                    map_2D[i][j-1] = map_2D[i][j] + 1;
                    map_2D[i+1][j-1] = map_2D[i][j] + 1;
                    map_2D[i-1][j+1] = map_2D[i][j] + 1;
                    map_2D[i+1][j+1] = map_2D[i][j] + 1;  
                    map_2D[i-1][j-1] = map_2D[i][j] + 1;                  
                }
            }
        }

        






                        
    }
}