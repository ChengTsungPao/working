public class TopN4105054025 extends TopN{
    public int[] Ans(int[][] c, int a, int n){
        int max = 0;
        for(int i=0;i<c.length;i++){
            if(c[i][0] > max || c[i][1] > max){
                if(c[i][0] > c[i][1]){
                    max = c[i][0];
                }else{
                    max = c[i][1];
                }
            }
        }
        if(n > max) n = max;
        int[] answer = new int[n];
        int[] ans_status = new int[n];
        int[] status = new int[max];
        for(int i=0;i<max;i++){
            status[i]=0;
        }
        for(int i=0;i<c.length;i++){
            if(c[i][0]==a){
                status[c[i][1]-1]++;
            }else if(c[i][1]==a){
                status[c[i][0]-1]++;
            }            
        }
        for(int i=0;i<n;i++){
            ans_status[i]=0;
            answer[i]=0;
        }
        int tmp,num=0;
        for(int i=0;i<max;i++){
            if(status[i]>ans_status[n-1]){
                ans_status[n-1]=status[i];
                answer[n-1]=i+1;
                for(int j=n-1;j>0;j--){
                    if(ans_status[j]>ans_status[j-1]){
                        tmp=ans_status[j-1];
                        ans_status[j-1]=ans_status[j];
                        ans_status[j]=tmp;

                        tmp=answer[j-1];
                        answer[j-1]=answer[j];
                        answer[j]=tmp;     
                    }else{
                        break;
                    }              
                }
            }
            if(status[i]>0) num++;
        }
        if(answer.length>num){
            int[] ans = new int[num];
            for(int i=0;i<num;i++){
                ans[i]=answer[i];
            }
            return ans;
        }else{
            return answer;
        }                
    }

}