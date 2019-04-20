
package test03;

import java.util.Scanner;

class test03
{
	public static void main(String arg[])
	{
		int N = 0;
		String plaintext = null;
		//--To Do Start--
		Scanner scn = new Scanner(System.in);
		Scanner scn_int = new Scanner(System.in);
		System.out.printf("Please input a shift number:\n");
		N = scn_int.nextInt();
		System.out.printf("Please input the plaintext:\n");
		plaintext = scn.nextLine();
		System.out.printf("Plaintext:  %s\n",plaintext);
		//--To Do End--
		Caesar sar = new Caesar(plaintext, N);
		sar.cipher();
	}
}
class Caesar
{
	private String this_plaintext;
	private int this_shift;
	public Caesar(String plaintext, int shift) // constructor
	{
		this_plaintext = plaintext;
		this_shift = shift;
	}
	public void cipher()
	{
		System.out.printf("Ciphertext: ");
		for(int i=0; i<this_plaintext.length(); i++)
		{
			int plaintext_num = (int)this_plaintext.charAt(i);
			int ciphertext_num = plaintext_num + this_shift;
			if(plaintext_num>=(int)'A' && plaintext_num<=(int)'Z')
			{
				if(ciphertext_num > (int)'Z')
					ciphertext_num = ciphertext_num-26*((ciphertext_num-(int)'Z'-1)/26+1);
				System.out.printf("%c", (char)ciphertext_num);
			}
			else if(plaintext_num>=(int)'a' && plaintext_num<=(int)'z')
			{
				if(ciphertext_num > (int)'z')
					ciphertext_num = ciphertext_num-26*((ciphertext_num-(int)'z'-1)/26+1);
				System.out.printf("%c", (char)ciphertext_num);
			}
			else
				System.out.printf("%c", (char)plaintext_num);
		}
	}
}