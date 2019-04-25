public class SortingArray41050540252 extends SortingArray{
    public int[] sorting(int[] A){
        int a,b,k=0,tmp=-1,d=1;
        int N = A.length;
        int[] ans = new int[N];
        for(int i=1;i*2<N;i=i*2){
            for(int j=0;(j-1)+i*2<N;j=j+i*2){
                a=j;
                b=j+i;     
                for(k=j;k<j+2*i;k++){
                    if(a>=j+i){
                        ans[k]=A[b++];
                    }
                    else if(b>=j+i*2){
                        ans[k]=A[a++];
                    }
                    else if(A[a]>A[b]){                        
                        ans[k]=A[b++];
                    }
                    else{
                        ans[k]=A[a++];
                    }                    
                }
            }  
            for(int j=0;j<k;j++){
                A[j]=ans[j];                
            }
            for(int j=0;j<N;j++){
                System.out.printf("%d ",ans[j]);
            }
            System.out.println();

            if(k!=N){
                if(tmp==k || i==1){
                    d=d*2;
                }
                a=k-d;
                if(i*2*2>=N){
                    a=0;
                    d=k;
                } 
                b=k;
                System.out.println("---------------------1 "+i);
                for(int j=k-d;j<N;j++){
                    //System.out.println("j:"+j+" a:"+a+" b:"+b);
                    
                    for(int t=0;t<N;t++){
                        System.out.printf("%d ",ans[t]);
                    }
                    System.out.println();
                    if(a>=k){                    
                        ans[j]=A[b++];
                    }
                    else if(b>=N){
                        ans[j]=A[a++];
                    }
                    else if(A[a]>A[b]){                        
                        ans[j]=A[b++];
                    }
                    else{
                        ans[j]=A[a++];
                    } 
                } 
                tmp=k;
                System.out.println("---------------------2");    
                        
                for(int j=k-d;j<N;j++){
                    A[j]=ans[j];                
                }
                for(int j=0;j<N;j++){
                    System.out.printf("%d ",ans[j]);
                }
                System.out.println();
            }

        }

        return ans;
    }

}