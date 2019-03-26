public class PrimeString41050540252 extends PrimeString{
    public int Count_ans(String[] A){
        char[] str;
        int sum,flag,count=0;
        int[] data={2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,
        101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199};
        for(int i=0;i<A.length;i++){
            sum=0;
            str=A[i].toCharArray();
            for(int j=0;j<str.length;j++){
                sum+=(char)str[j]+48;
            }
            if(sum>=2){
                flag=1;
                for(int j=0;j<data.length && data[j]*data[j]<sum;j++){
                    if(sum%data[j]==0){
                        flag=0;
                        break;
                    }
                }
                for(int j=211;j*j<sum && flag==1;j++){
                    if(sum%j==0){
                        flag=0;
                        break;
                    }
                }
                if(flag==1) count++;  
            }          
        }
        return count;
    }
}