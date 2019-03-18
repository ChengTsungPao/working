import java.util.Arrays;

public class ThreeSum4104056046 extends ThreeSum
{
	public int T_sum(int[] nums)
	{
		int result = 0;
		Arrays.sort(nums);
	
		for(int i = 0; i < nums.length && nums[i] <= 0; i++) 
		{
		    if(i != 0 && nums[i] == nums[i - 1]) 
		    	continue;
	
		            
		    int j = i + 1, k = nums.length - 1;
		    
		    while(j < k) 
		    {
		        int sum = nums[i] + nums[j] + nums[k];
	
		        if(sum == 0) 
		        	++result;
		            
		        if(sum <= 0) do j++; while (j < k && nums[j] == nums[j - 1]);
	
		        if(sum >= 0) do k--; while (j < k && nums[k] == nums[k + 1]);
		     }
		 }
		
		 return result; 
	}	
	
}