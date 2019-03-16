import java.util.Arrays;

public class ThreeSum4105054025 extends ThreeSum{

    public int T_sum(int[] A) {
        
        Arrays.sort(A);
        int x1,x2,N=A.length,ans=0;
        for(int find=0;A[find]<0;find++){
            x1=find+1;
            x2=N-1;
            while(x1<x2){
                if(A[find]+A[x1]+A[x2]==0){
                    ans++;
                    x1++;
                    x2--;
                }
                else if(A[find]+A[x1]+A[x2]>0){
                    x2--;                   
                }
                else{
                    x1++;
                }
            }
        }
        return ans;        
    }
}
