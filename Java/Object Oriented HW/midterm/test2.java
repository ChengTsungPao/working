import java.util.Scanner;

public class test2{
    public static void main(String[] args) {
        String data1 = "abcdefghijklmnopqrstuvwxyz";
        String data2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        String tmp;

        char[] s=data1.toCharArray();
        char[] b=data2.toCharArray();
        Scanner key = new Scanner(System.in);
        System.out.println("Input a paragraph of text:");
        tmp = key.nextLine();
        char[] text=tmp.toCharArray();
        System.out.println("Input deleted characters:");
        tmp = key.nextLine();
        char[] del=tmp.toCharArray();
        int flag;
        for(int i=text.length-1;i>=0;i--){
            flag=1;
            for(int j=0;j<del.length && flag==1;j++){
                if(text[i]==del[j]){
                    flag=0;
                }
                for(int k=0;k<26 && flag==1;k++){
                    if(del[j]==s[k] || del[j]==b[k])
                    {
                        if(text[i]==s[k] || text[i]==b[k]){
                            flag=0;
                        }
                    }
                }

            }
            if(flag==1){
                System.out.printf("%c",text[i]);
            }            
        }
        
    }
}