public class Continuous4105054025 extends Continuous{

    public  int min_sum(int[] list){
        int min=0,sum=0;
        for(int i=0;i<list.length;i++){
            for(int j=i;j<list.length;j++){
                sum+=list[j];
                if((i==0 && j==0) || sum < min){
                    min = sum;
                }
            }
            sum = 0;
        }
        return min;
    }

}
