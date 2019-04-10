import java.util.Scanner;

class MultiFunction{

    public void show(int x1,int x2,int x3){

        int gcd=0;
        int lcm=0;        
        for(int i=x1;i>0;i--){
            if(x1%i==0 && x2%i==0 && x3%i==0){
                gcd=i;
                break;
            }
        }
        for(int i=x1;i<x1*x2*x3;i++){
            if(i%x1==0 && i%x2==0 && i%x3==0){
                lcm=i;
                break;
            }
        }
        System.out.printf("gcd=%d ,lcm=%d",gcd,lcm);

    }

    public void show(int x1,int x2,int x3,int x4){

        int[] x = {x1,x2,x3,x4};
        int[] ans = {x[0],x[1],x[2],x[3]};
        double max = -2*x[0]*x[0]-4*x[1]+5*x[2]+Math.sqrt(x[3]*x[3]*x[3]);
        for(int i=0;i<x.length;i++){
            for(int j=0;j<x.length;j++){
                if(j!=i){
                    for(int k=0;k<x.length;k++){
                        if(k!=j && k!=i){
                            for(int m=0;m<x.length;m++){                                
                                if(m!=k && m!=j && m!=i){
                                    //System.out.printf("%d %d %d %d sum=%f\n",i,j,k,m,-2*x[i]*x[i]-4*x[j]+5*x[k]+Math.sqrt(x[m]*x[m]*x[m]));
                                    if(max<(-2*x[i]*x[i]-4*x[j]+5*x[k]+Math.sqrt(x[m]*x[m]*x[m]))){
                                        max = -2*x[i]*x[i]-4*x[j]+5*x[k]+Math.sqrt(x[m]*x[m]*x[m]);
                                        ans[0] = x[i];
                                        ans[1] = x[j];
                                        ans[2] = x[k];
                                        ans[3] = x[m];                                        
                                    }
                                }    
                            }
                        }    
                    }
                }
            }
        } 
        System.out.printf("x1=%d, x2=%d, x3=%d, x4=%d\n",ans[0],ans[1],ans[2],ans[3]);
        System.out.println(max);

    }

    public void show(int x1,int x2,int x3,int x4,int x5){

        double mean = (x1+x2+x3+x4+x5)/5.0;
        double sum = 0;
        double[] x = {x1,x2,x3,x4,x5};
        for(int i=0;i<5;i++){
            sum+=(x[i]-mean)*(x[i]-mean);
        }
        System.out.println("SD="+Math.sqrt(sum/5.0));        

    }

}

class homework2_3{
    public static void main(String[] args) {
        System.out.println("input data (For example : 1,2,3,4,5)");
        Scanner key = new Scanner(System.in);
        String[] x = key.nextLine().split(",");
        MultiFunction mf = new MultiFunction();
        if(x.length==3){
            mf.show(Integer.valueOf(x[0]),Integer.valueOf(x[1]),Integer.valueOf(x[2]));
        }
        else if(x.length==4){
            mf.show(Integer.valueOf(x[0]),Integer.valueOf(x[1]),Integer.valueOf(x[2]),Integer.valueOf(x[3]));
        }
        else if(x.length==5){
            mf.show(Integer.valueOf(x[0]),Integer.valueOf(x[1]),Integer.valueOf(x[2]),Integer.valueOf(x[3]),Integer.valueOf(x[4]));
        }
        else{
            System.out.println("error");
        }        
    }
}
