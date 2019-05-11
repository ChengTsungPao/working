import java.util.Scanner;

class homework3_3{
    public static int a,b;
    public static char[] order;
    public static void main(String[] args) {
        Scanner key = new Scanner(System.in);
        String input = key.nextLine();
        System.out.println();
        homework3_3 method = new homework3_3();
        method.sort(input);
        method.show(order,0);   
        method.show(order,1);
   
    }
    public void sort(String input){
        a = -1;
        b = -1;
        char tmp;
        order = input.toCharArray();
        for(int i=0;i<order.length-1;i++){
            for(int j=i+1;j<order.length;j++){
                if((int)order[j]<(int)order[i]){
                    tmp = order[j];
                    order[j] = order[i];
                    order[i] = tmp;
                }  
            }
            if((int)order[i]>=65 && a==-1){
                a = i;
            }
            if((int)order[i]>=97 && b==-1){
                b = i;
            }
        }
    }
    public void show(char[] input,int mode){
        if(mode==0){
            System.out.print("Form small to large: ");
            for(int i=0;i<input.length;i++){
                System.out.printf("%c",input[i]);
            }
            System.out.println();
        }else{
            System.out.print("From large to small: ");
            if(a!=-1 && b!=-1){
                for(int i=a-1;a-1>=0 && i>=0;i--){
                    System.out.printf("%c",input[i]);
                }
                for(int i=b-1;b-1>=0 && i>=a;i--){
                    System.out.printf("%c",input[i]);
                }
                for(int i=input.length-1;i>=b;i--){
                    System.out.printf("%c",input[i]);
                }
                System.out.println();
            }else if(a!=-1 && b==-1){
                for(int i=a-1;a-1>=0 && i>=0;i--){
                    System.out.printf("%c",input[i]);
                }
                for(int i=input.length-1;i>=a;i--){
                    System.out.printf("%c",input[i]);
                }
                System.out.println();
            }else{
                for(int i=input.length-1;i>=0;i--){
                    System.out.printf("%c",input[i]);
                }
                System.out.println();
            }
        }

    }
}