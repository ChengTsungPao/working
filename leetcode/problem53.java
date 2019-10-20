class Solution {
    public int maxSubArray(int[] nums) {
        int sum = 0, max = 0, min = 0;
        for (int i=0;i<nums.length;i++) {    
            if(sum > max) max = sum;
            sum += -nums[i];
            if(i==0 || sum - max < min) min = sum - max;
        }
        return -min;        
    }
}
class problem53{
    public static void main(String[] args) {
        int[] arr = {-2,1,-3,4,-1,2,1,-5,4};
        Solution s = new Solution();
        System.out.println(s.maxSubArray(arr));        
    }

}