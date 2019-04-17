import java.util.Scanner;

public class test3{
    public static void main(String[] args) {
        String data1="abcdefghijklmnopqrstuvwxyz";
        String data2="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        Scanner key1 = new Scanner(System.in);
        Scanner key2 = new Scanner(System.in);
        String a=key1.nextLine();
        String b=key2.nextLine();
        int i,j,flag,c=0;
        char d[]=new char[26];
        for(i=0;i<26;i++)
        {
            d[i]=0;
        }
        for(j=0;j<b.length();j++){
            for(i=0;i<26;i++){
                
                if(data1.toCharArray()[i]==b.toCharArray()[j]){
                    d[c++]=data2.toCharArray()[i];
                 }else if(data2.toCharArray()[i]==b.toCharArray()[j]){
                    d[c++]=data1.toCharArray()[i];
                }
   
            }                
        }
        for(i=a.length()-1;i>=0;i--){
            flag=1;
            for(j=0;j<c;j++){
                if(d[j]==a.toCharArray()[i]){
                    flag=0;
                    break;
                }
            }
            for(j=0;j<b.length();j++){
                if(a.toCharArray()[i]==b.toCharArray()[j]){
                    flag=0;
                    break;
                }
            }
            if(flag==1){
                System.out.printf("%c",a.toCharArray()[i]);
            }
        }

 
        
     





        
    }
}