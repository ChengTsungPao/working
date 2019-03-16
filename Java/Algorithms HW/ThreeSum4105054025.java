import java.util.Arrays;

public class ThreeSum4105054025 extends ThreeSum{

    public int T_sum(int[] A) {
        Arrays.sort(A);
        int N=A.length;
        int i=0,j=0,k=0,cnt=0,tmp=-1;  
        int start=0,end=N;
        for(i=0;A[i]<0;i++){
            for(j=N-1;A[j]>=0;j--){
                tmp=Arrays.binarySearch(A,start,end,-A[i]-A[j]);
                if(tmp>0){
                    if(((tmp>i && A[tmp]<0) || (tmp<j && A[tmp]>=0))){
                        for(k=tmp;A[tmp]==A[k] && k!=i && k!=j;k++){
                            cnt++;
                        }   
                        start=tmp;
                        for(k=tmp-1;A[tmp]==A[k] && k!=i && k!=j;k--){
                            cnt++;
                        }                   
                    }
                }
                else if(tmp!=-(start+1) && tmp!=-(end+1) && tmp!=0){
                    start=-tmp-1;                  
                }
            }
            start=0;
            end=N;
        }
        return cnt;        
    }

}