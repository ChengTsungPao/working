import java.util.Random;

class MaxDifferenceMain{
    public static void main(String[] args) {
        MaxDifference4105054025 test = new MaxDifference4105054025();
        //int[] arr = {1,2,0,0,-2,-1};  //{-2,-1,-1,1,2,3}
        Random rd = new Random(); // creating Random object
        int[] arr = new int[100000];
        for (int i = 0; i < arr.length; i++) {
           arr[i] = rd.nextInt(200001)-100000; // storing random integers in an array
           //System.out.println(arr[i]); // printing each array element
        }
        
        int ans;
        long t1,t2;
        t1 = System.currentTimeMillis();
        ans = test.max_d(arr);
        t2 = System.currentTimeMillis();
        System.out.println("Answer:"+ans);
        System.out.println("Time:"+(t2-t1)/1000.0);
        
    }
}