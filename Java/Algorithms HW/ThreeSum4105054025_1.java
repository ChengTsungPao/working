import java.util.Arrays;

public class ThreeSum4105054025 extends ThreeSum{

    public int T_sum(int[] A) {
        Arrays.sort(A);
        int N = A.length;
        int cnt = 0;
        for(int i=0;i<N;i++){
            for(int j=i+1;j<N;j++){
                if(Arrays.binarySearch(A,-A[i]-A[j])>j){
                    cnt++;
                }
            }
        }
        return cnt;
        
    }

}