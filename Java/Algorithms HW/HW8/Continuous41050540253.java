public class Continuous41050540253 extends Continuous{

    public int min_sum(int[] list){

        int sum = 0, max = 0, min = list[0];
        for (int i=0;i<list.length;i++) {    
            if(sum > max) max = sum;
            sum += list[i];
            if(sum - max < min) min = sum - max;
        }
        return min;
    }

}