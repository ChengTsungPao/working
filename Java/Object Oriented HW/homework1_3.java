import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;

public class homework1_3{
    public static void main(String[] args) {
        System.out.println("Please input the shape of the game and the number of mines.");
        Scanner input = new Scanner(System.in);
        String tmp = input.nextLine();
        int size = Integer.valueOf(tmp.split(" ")[0]);
        int mines = Integer.valueOf(tmp.split(" ")[1]);
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
        int map_2D[][] = new int[size][size];
        for(int i=0;i<map.length;i++){
            map_2D[i/size][i%size] = map[i];            
        }
        for(int i=0;i<size;i++){
            for(int j=0;j<size;j++){
                if(map_2D[i][j]==-1){
                    if(i+1<size && map[(i+1)*size+j]!=-1) map_2D[i+1][j] = map_2D[i+1][j] + 1;
                    if(j+1<size && map[i*size+j+1]!=-1) map_2D[i][j+1] = map_2D[i][j+1] + 1;
                    if(i-1>=0 && map[(i-1)*size+j]!=-1) map_2D[i-1][j] = map_2D[i-1][j] + 1;
                    if(j-1>=0 && map[i*size+j-1]!=-1) map_2D[i][j-1] = map_2D[i][j-1] + 1;
                    if(i+1<size && j-1>=0 && map[(i+1)*size+j-1]!=-1) map_2D[i+1][j-1] = map_2D[i+1][j-1] + 1;
                    if(i-1>=0 && j+1<size && map[(i-1)*size+j+1]!=-1) map_2D[i-1][j+1] = map_2D[i-1][j+1] + 1;
                    if(i+1<size && j+1<size && map[(i+1)*size+j+1]!=-1) map_2D[i+1][j+1] = map_2D[i+1][j+1] + 1;  
                    if(i-1>=0 && j-1>=0 && map[(i-1)*size+j-1]!=-1) map_2D[i-1][j-1] = map_2D[i-1][j-1] + 1;                  
                }
            }
        }
        /*
        for(int i=0;i<size;i++){
            for(int j=0;j<size;j++){
                System.out.printf("%2d ",map_2D[i][j]);     
            }
            System.out.println();
        }
        */
        int flag1 = 1,flag2 = 1;
        int pos[] = new int[2];
        char vision[][] = new char[size][size];
        for(int i=0;i<size;i++){
            for(int j=0;j<size;j++){
                vision[i][j] = '*';
            }
        }
        
        while(flag1==1){            
            for(int i=0;i<size;i++){
                for(int j=0;j<size;j++){
                    System.out.printf("%c ",vision[i][j]);
                }
                System.out.println();
            }
            System.out.println("Input coordinate:");
            Scanner key = new Scanner(System.in);
            tmp = key.nextLine();
            pos[0] = Integer.valueOf(tmp.split(" ")[0])-1;
            pos[1] = Integer.valueOf(tmp.split(" ")[1])-1;
            if(map_2D[pos[0]][pos[1]]==-1){
                for(int i=0;i<size;i++){
                    for(int j=0;j<size;j++){
                        if(map_2D[i][j]==-1){
                            System.out.printf("%c ",'X');
                        }
                        else{
                            System.out.printf("%d ",map_2D[i][j]);
                        }
                        
                    }
                    System.out.println();
                }
                System.out.println("Game Over!");
                break;
            }
            else{
                vision[pos[0]][pos[1]] = (char)(map_2D[pos[0]][pos[1]] + 48);
            }
            flag2 = 1;
            while(flag2==1 && vision[pos[0]][pos[1]]=='0'){
                flag2 = 0;
                for(int i=0;i<size;i++){
                    for(int j=0;j<size;j++){
                        if(vision[i][j]=='0'){
                            if(i+1<size){
                                if(vision[i+1][j]=='*' && map_2D[i+1][j]!=-1){
                                    vision[i+1][j] = (char)(map_2D[i+1][j] + 48);
                                    flag2 = 1;
                                }                        
                            }
                            if(j+1<size){
                                if(vision[i][j+1]=='*' && map_2D[i][j+1]!=-1){
                                    vision[i][j+1] = (char)(map_2D[i][j+1] + 48);
                                    flag2 = 1;
                                }                  
                            }
                            if(i-1>=0){
                                if(vision[i-1][j]=='*' && map_2D[i-1][j]!=-1){
                                    vision[i-1][j] = (char)(map_2D[i-1][j] + 48);
                                    flag2 = 1;
                                }                       
                            } 
                            if(j-1>=0){
                                if(vision[i][j-1]=='*' && map_2D[i][j-1]!=-1){
                                    vision[i][j-1] = (char)(map_2D[i][j-1] + 48);
                                    flag2 = 1;
                                }                         
                            } 
                            if(i+1<size && j-1>=0){
                                if(vision[i+1][j-1]=='*' && map_2D[i+1][j-1]!=-1 && (map_2D[i+1][j-1]!=0 || map_2D[i+1][j]==0 || map_2D[i][j-1]==0)){
                                    vision[i+1][j-1] = (char)(map_2D[i+1][j-1] + 48);
                                    flag2 = 1;
                                }                        
                            } 
                            if(i-1>=0 && j+1<size){
                                if(vision[i-1][j+1]=='*' && map_2D[i-1][j+1]!=-1 && (map_2D[i-1][j+1]!=0 || map_2D[i-1][j]==0 || map_2D[i][j+1]==0)){
                                    vision[i-1][j+1] = (char)(map_2D[i-1][j+1] + 48);
                                    flag2 = 1;
                                }                       
                            } 
                            if(i+1<size && j+1<size){
                                if(vision[i+1][j+1]=='*' && map_2D[i+1][j+1]!=-1 && (map_2D[i+1][j+1]!=0 || map_2D[i+1][j]==0 || map_2D[i][j+1]==0)){
                                    vision[i+1][j+1] = (char)(map_2D[i+1][j+1] + 48);
                                    flag2 = 1;
                                }                    
                            } 
                            if(i-1>=0 && j-1>=0){
                                if(vision[i-1][j-1]=='*' && map_2D[i-1][j-1]!=-1 && (map_2D[i-1][j-1]!=0 || map_2D[i-1][j]==0 || map_2D[i][j-1]==0)){
                                    vision[i-1][j-1] = (char)(map_2D[i-1][j-1] + 48);
                                    flag2 = 1;
                                }                  
                            }   
                            
                        }

                    }
                }                
            }
            flag1 = 0;
            for(int i=0;i<size;i++){
                for(int j=0;j<size;j++){
                    if(vision[i][j]=='*' && map_2D[i][j]!=-1){
                        flag1 = 1;
                        break;
                    }
                }
            }
            if(flag1==0){
                for(int i=0;i<size;i++){
                    for(int j=0;j<size;j++){
                        System.out.printf("%c ",vision[i][j]);
                    }
                    System.out.println();
                }
                System.out.println("Winner!!"); 
            } 
        }                        
    }
}