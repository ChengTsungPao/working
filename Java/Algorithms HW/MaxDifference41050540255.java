public class MaxDifference41050540255 extends MaxDifference{
    public int max_d(int[] A){
        int m=A[0];
        int M=A[0];
        for(int i=1;i<A.length;i++){
            if(A[i]<m)m=A[i];
            if(A[i]>M)M=A[i];
        }
        return M-m;
    }
}