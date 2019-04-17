public class gcdname{
    public int[] gcd(int[] g){

        int a=g[0];
        int b=g[1];
        if(a!=1 && b!=1 && a!=0 && b!=0){
            if(a>=b){
                a=a%b;
                g[0]=a;
                g[1]=b;
                return gcd(g);
            }
            else if(a<b){
                b=b%a;
                g[0]=a;
                g[1]=b;
                return gcd(g);
            }
        }
        return g;
    
    
    }
}