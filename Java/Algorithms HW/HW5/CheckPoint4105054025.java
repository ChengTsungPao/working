public class CheckPoint4105054025 extends CheckPoint{

    public boolean Ans(int[][] A){
        
        int theta=0;
        for(int i=0;i<A.length && theta!=1;i++){
            for(int j=i+1;j<A.length && theta!=1;j++){
                for(int k=j+1;k<A.length && theta!=1;k++){
                    theta=(A[j][0]-A[i][0])*(A[k][0]-A[i][0])+(A[j][1]-A[i][1])*(A[k][1]-A[i][1]);
                    theta=theta*theta;
                    theta=theta/((A[j][0]-A[i][0])*(A[j][0]-A[i][0])+(A[j][1]-A[i][1])*(A[j][1]-A[i][1]));
                    theta=theta/((A[k][0]-A[i][0])*(A[k][0]-A[i][0])+(A[k][1]-A[i][1])*(A[k][1]-A[i][1]));
                }
            }
        }
        if(theta==1){
            return true;
        }
        else{
            return false;
        }   
        
    }

}