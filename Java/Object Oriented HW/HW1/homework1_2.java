import java.util.Scanner;

public class homework1_2{
    public static void main(String[] args) {               
        int tmp,index=0;
        String data="ABCDEFGHIJKLMNOPQRSTUVWXYZ";

        System.out.printf("Input the number of A : ");
        Scanner key1 = new Scanner(System.in);
        int A=key1.nextInt();

        System.out.printf("Input the number of N : ");
        Scanner key2 = new Scanner(System.in);        
        int N=key2.nextInt();

        System.out.println();
        for(int i=0;i<2*A-1;i++){
            for(int j=0;j<N;j++){
                for(int k=0;k<2*A-1+3;k++){   
                    if(i>=A){
                        tmp=2*A-2-i;
                    }
                    else{
                        tmp=i;
                    }
                    if(k%(2*A-1+3)==A-1-tmp || k%(2*A-1+3)==2*A-2-(A-tmp-1)){
                        System.out.printf("*");
                    }
                    else if((k%(2*A-1+3)==A-1-tmp+2 || k%(2*A-1+3)==2*A-2-(A-tmp-1)-2) && tmp>=2){
                        System.out.printf("o");
                    }
                    else if(tmp==A-1 && k%(2*A-1+3)>=2*A-1){
                        if(index>=data.toCharArray().length) index=0;
                        System.out.printf("%c",data.toCharArray()[index++]);                       
                    }    
                    else{
                        System.out.printf(" ");
                    }   
                          
                }
            }
            System.out.println();
        }    
    }

}
