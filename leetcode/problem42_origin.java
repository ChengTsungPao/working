class Solution {
    public int trap(int[] height) {

        int maxpos = 0;
        int max = 0;
        for(int i=0;i<height.length;i++){
            if(height[i]>max){
                max = height[i];
                maxpos = i;
            }
        }
        
        int total_rain = 0;
        int start = 0;
        int end = 1;
        int sum = 0;        
        for(int i=1;i<=maxpos;i++){
            if(height[i]>=height[start]){
                if(height[start]<height[end]){
                    total_rain += (end-start-1)*height[start] - sum;
                }else{
                    total_rain += (end-start-1)*height[end] - sum;
                }
                sum = 0;
                start = i;
                end = i+1;
            }else{
                sum += height[i];
                end++;
            }         
        }

        start = height.length-1;
        end = height.length-2;
        sum = 0;        
        for(int i=height.length-2;i>=maxpos;i--){     
            if(height[i]>=height[start]){
                if(height[start]<height[end]){
                    total_rain += (start-end-1)*height[start] - sum;
                }else{
                    total_rain += (start-end-1)*height[end] - sum;
                }
                sum = 0;
                start = i;
                end = i-1;
            }else{
                sum += height[i];
                end--;
            }         
        }

        return total_rain;        
    }
}
class problem42_origin{
    public static void main(String[] args) {
        int[] arr = {4,2,3};
        Solution s = new Solution();
        System.out.println(s.trap(arr));        
    }

}