public class Continuous4105054025 extends Continuous{
    public int min_sum(int[] list){
        int sum=0,max=0,min=list[0];for(int x:list) {if(sum>max) max=sum;sum+=x;if(sum-max<min) min=sum-max;}return min;}}