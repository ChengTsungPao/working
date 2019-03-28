import java.util.Scanner;
class test1{
    public static void main(String[] args) {
        Scanner key1 = new Scanner(System.in);
        Scanner key2 = new Scanner(System.in);
        String b=key1.nextLine();
        String a=key2.nextLine();
        Caeser test = new Caeser(a,Integer.valueOf(b));
        test.cipher();

        
    }
}

class Caeser{
    public String str;
    public int N;
    public Caeser(String plain,int n){
        str=plain;
        N=n;
    }
    public void cipher(){
        char[] tmp = str.toCharArray();
        int asc;
        for(int i=0;i<tmp.length;i++){
            if(((int)tmp[i]>=97 && (int)tmp[i]<97+25) || ((int)tmp[i]>=65 && (int)tmp[i]<65+25)){
                asc=(int)tmp[i]+N;
                if(asc>97+25 && (int)tmp[i]>=97){
                    asc=asc-(97+25)+96;
                }
                else if(asc>65+25 && (int)tmp[i]<=65+25){
                    asc=asc-(65+25)+64;
                }
                tmp[i]=(char)(asc);
            }
        }
        for(int i=0;i<tmp.length;i++){
            System.out.printf("%c",tmp[i]);
        }
        System.out.println();
    }
}