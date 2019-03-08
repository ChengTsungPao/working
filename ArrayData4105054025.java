public class ArrayData4105054025 extends ArrayData{

    public ArrayData4105054025(int[] A){
        this.A = A;
    }

    public int max(){
    	if(A.length!=0){
	        int num = A[0];
	        for(int x:A){
	            if(num < x){
	                num=x;
	            }
	        }
	        return num;
    	}
        else{
            return 0;
        }
    }

    public int dot(int[] B){
        if(A.length==B.length && A.length!=0 && B.length!=0){
            int sum = 0;
            for(int i=0;i<A.length;i++){
                sum+=A[i]*B[i];
            }
            return sum;
        }
        else{
            return 0;
        }
    }
}