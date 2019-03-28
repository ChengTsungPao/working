class PrimeStringMain{
    public static void main(String[] args) {
        //String[] A={"abc","def","ghi","23","=",""};
        String[] A={"App","DL5","!\""};
        //String[] A={"Doit","Cp","562dax"};          
        PrimeString4105054025 test = new PrimeString4105054025();
        System.out.println(test.Count_ans(A)); 
        /*   
        System.out.println((int)'\"');  
        System.out.println();
        char[] a;
        int tmp;
        for(int j=0;j<A.length;j++){
            a=A[j].toCharArray();
            for(int i=0;i<a.length;i++){
                tmp=(int)a[i];
                System.out.println(tmp);
            }
            System.out.println();
        }
        */
        
    }
}