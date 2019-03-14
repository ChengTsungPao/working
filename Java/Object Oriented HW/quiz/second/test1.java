public class test1{
    
    public static void main(String[] args) {
        int N=5;
        int M=0;
        int j=0,k=0;
        int data[][]=new int[N][N];
        for(int i=0;i<N;i++){
            for(j=0;j<N;j++){
                data[i][j]=0;
            }
        }   
        j=0; 
        if(M==0){
            for(int i=0;i<N*N;i++){
                if(j>=N){
                    choose();
                }

            } 
            
        }
        else if(M==1){
            for(int i=0;i<N;i++){
                for(j=0;j<N;j++){
                    data[i][j]=0;
                }
            }           
        }
        else{
            System.out.println("input the correct data");
        }
        for(int i=0;i<N;i++){
            for(j=0;j<N;j++){
                System.out.printf("%2d ",data[i][j]);
            }
            System.out.println();
        }        
        public void choose(int num){
            num=num%4;
            switch (key) {
                case 0:
                    k++;
                    break;
                case 1:
                    j++;
                    break;
                case 2:
                    k--;
                    break;
                case 3:
                    j--;
                    break;       
                default:
                    break;
            }
        }
    }

}