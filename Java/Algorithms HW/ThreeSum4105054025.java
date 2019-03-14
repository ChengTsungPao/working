import java.util.Arrays;

public class ThreeSum4105054025 extends ThreeSum{

    public int T_sum(int[] A) {
        Arrays.sort(A);
        int N=A.length;
        int i=0,j=0,k=0,index=0,cnt=0,tmp=-1;
        for(i=0;i<N;i++){
            if(A[i]>=0){
                index=i;
                break;
            }
        }        
        for(i=0;i<index;i++){
            for(j=index;j<N;j++){
                tmp=Arrays.binarySearch(A,-A[i]-A[j]);
                if((tmp>i && tmp<index) || (tmp>j && tmp>=index)){
                    for(k=tmp;A[tmp]==A[k] && k!=i && k!=j;k--){
                        cnt++;
                    }                    
                }
            }
        }
        return cnt;
        
    }

}