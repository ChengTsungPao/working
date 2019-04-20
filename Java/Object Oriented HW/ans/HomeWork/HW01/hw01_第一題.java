
import java.util.*;


public class hw01 {
	
	public static void main(String[] args) {
		Scanner scn = new Scanner(System.in);
		int r, c, k, a1, a2, a3, a4;
		System.out.printf("輸入r");
		r = scn.nextInt();
		System.out.printf("輸入c");
		c = scn.nextInt();
		System.out.printf("輸入k");
		k = scn.nextInt();
		if (1 > (c-k))
			a1 = 1;
		else
			a1 = c-k;
		
		if ((c+k) > 8)
			a2 = 8;
		else
			a2 = c+k;
		
		if (1 > r-k)
			a3 = 1;
		else
			a3 = r-k;
		
		if(r+k > 8)
			a4 = 8;
		else
			a4 = r+k;
		
		System.out.printf("%d格", (a2-a1+1)*(a4-a3+1));
	
	
	
	
	}
}
