class Solution {
    public int[][] reconstructQueue(int[][] people) {
        int[][] ans = {{7,0}, {4,4}, {7,1}, {5,0}, {6,1}, {5,2}};



        return ans;        
    }
}
class problem406{
    public static void main(String[] args) {
        int[][] arr = {{7,0}, {4,4}, {7,1}, {5,0}, {6,1}, {5,2}};
        Solution s = new Solution();
        int[][] ans = s.reconstructQueue(arr);
        for(int i=0;i<ans.length;i++){
            System.out.printf("{%d,%d}\n",ans[i][0],ans[i][1]); 
        }               
    }

}