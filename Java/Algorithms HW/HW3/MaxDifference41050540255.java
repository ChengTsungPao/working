public class MaxDifference41050540255 extends MaxDifference{public int max_d(int[] A){int B[]={A[0],A[0]};for(int i=1;i<A.length;i++){if(A[i]<B[0])B[0]=A[i];if(A[i]>B[1])B[1]=A[i];}return B[1]-B[0];}}