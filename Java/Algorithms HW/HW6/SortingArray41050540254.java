public class SortingArray41050540254 extends SortingArray{
    public int[] sorting(int[] A){
        int tmp;
        for(int i=0;i<A.length-1;i++){
            for(int j=i+1;j>0;j--){
                if(A[j]<A[j-1]){
                    tmp=A[j];
                    A[j]=A[j-1];
                    A[j-1]=tmp;
                }
                else{
                    break;
                }
            }
        }
        return A;
    }
}




