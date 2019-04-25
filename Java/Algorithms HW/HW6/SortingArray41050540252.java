public class SortingArray41050540252 extends SortingArray{
    public int[] sorting(int[] A){
        int a,b,k=0,tmp=0;
        int N = A.length;
        int[] B = new int[N];
        for(int i=1;i<N;i=i*2){
            tmp=i;
        }
        for(int i=1;i<tmp;i=i*2){
            for(int j=0;(j-1)+i*2<N;j=j+i*2){
                a=j;
                b=j+i;     
                for(k=j;k<j+2*i;k++){
                    if(a>=j+i){
                        B[k]=A[b++];
                    }
                    else if(b>=j+i*2){
                        B[k]=A[a++];
                    }
                    else if(A[a]>A[b]){                        
                        B[k]=A[b++];
                    }
                    else{
                        B[k]=A[a++];
                    }                    
                }
            }  
            for(int j=0;j<k;j++){
                A[j]=B[j];   
            }
        }
        for(int i=tmp-1;i<N-1;i++){
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