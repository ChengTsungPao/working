public class SortingArray4105054025 extends SortingArray{
    public int[] sorting(int[] A){
        int Judge=0;
        if(Judge==1){
            int a,b,k=0,tmp=0,start=0;
            int N = A.length;
            int[] B = new int[N];
            start+=tmp;
            for(int i=1;i<N;i=i*2){
                tmp=i;
            }        
            for(int i=1;i<tmp;i=i*2){
                for(int j=start;(j-1)+i*2<N;j=j+i*2){
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
            while((start+tmp)!=N){            
                start+=tmp;
                for(int i=1;i<N-start+1;i=i*2){
                    tmp=i;
                }
                
                for(int i=1;i<tmp;i=i*2){
                    for(int j=start;(j-1)+i*2<N;j=j+i*2){
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
                a=0;
                b=start;
                for(int i=0;i<start+tmp;i++){
                    if(a>=start){
                        B[i]=A[b++];
                    }
                    else if(b>=start+tmp){
                        B[i]=A[a++];
                    }
                    else if(A[a]>A[b]){                        
                        B[i]=A[b++];
                    }
                    else{
                        B[i]=A[a++];
                    }  
                }
                for(int i=0;i<start+tmp;i++){
                    A[i]=B[i];   
                }
            }
        }        
        SortingArray4105021032 ans = new SortingArray4105021032();        
        return ans.sorting(A);
    }

}