public class PrimeString41050540255 extends PrimeString{
    public int Count_ans(String[] A){
        char[] str;
        int sum,flag,count=0;
        for(int i=0;i<A.length;i++){
            sum=0;
            str=A[i].toCharArray();
            for(int j=0;j<str.length;j++){
                sum+=(int)str[j];
            }
            if(sum>=2){
                flag=1;
                if(sum%2==0 && sum!=2){
                    flag=0;
                }
                else{
                    for(int j=3;j*j<=sum && flag==1;j+=2){
                        if(sum%j==0){
                            flag=0;
                            break;
                        }
                    }
                }
                if(flag==1) count++;  
            }          
        }
        return count;
    }
}