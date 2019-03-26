import java.util.Arrays;

public class ThreeSum_1 extends ThreeSum{

    public int T_sum(int[] A) {
        
        Arrays.sort(A);
        int start,end,N=A.length,cnt=0;;
        for(int i=0;i<N-1;i++){
            start=i+1;
            end=N-1;
            while(start < end){
                if(A[i]+A[start]+A[end]==0){
                    cnt++;
                    start++;
                    end--;
                }
                else if(A[i]+A[start]+A[end] > 0){
                    end--;
                }
                else{
                    start++;
                }
            }
        }
        return cnt;
        
    }

}

