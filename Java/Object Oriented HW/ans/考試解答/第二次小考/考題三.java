

import java.util.Scanner;
import java.lang.*;

public class test02 
{
	public static void reverse() 
	{
        String str1, del_char;
        Scanner scanner = new Scanner(System.in);   
        boolean flage_del;
        System.out.printf("Please input a paragraph of text: \n");
        str1 = scanner.nextLine();    // 輸入一段文字
        System.out.print("Input deleted characters: \n");
        del_char = scanner.nextLine(); // 輸入要刪除的字元
        scanner.close();
        System.out.printf("result: \n");
        for (int i=str1.length()-1; i>=0; i--)  // 從一段文字最後讀回來
        {
        	flage_del = true;  //是否要顯示
        	for (int j=del_char.length()-1; j>=0; j--)  //讀取要刪除的字元
        	{
                //判斷刪除的字元與文章的字元是否一樣
        		if (del_char.charAt(j) == str1.charAt(i) || low(del_char.charAt(j)) == low(str1.charAt(i))) 
        			flage_del = false;
        	}// End if
        	if (flage_del)  // 如果true則顯示，否則不顯示
        	{
        		System.out.printf("%c",str1.charAt(i));
        	}// End if
        		
        }
	}// End reverse()
	
	public static char low(char chr)  //如果是大寫字母，就轉成小寫
	{
		
		if((int)chr>=65 && (int)chr<=90)
		{
			return (char) ((int)chr+32);
		}// End if
		else
			return chr;
			
	} // End low()
	
	public static void main(String[] args)
	{
		reverse();

	} //End main()
	
} //End class main



