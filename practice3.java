class practice3{
    public static void main(String args[]) {
        System.out.println("\nIndex\tValue");
        int bucky[]={12,45,32,66,55}; // int bucky[] = new int[5] 
                                      // int bucky[]={{1,2,3},{1,2}}
        for(int count=0;count < bucky.length;count++){
            System.out.println(count+"\t"+bucky[count]);
        }
        sum(bucky);
        System.out.println("The average is "+avg(bucky));
    }
    public static void sum(int arr[]) {
        int total = 0;
        for(int x:arr){
            total+=x;
        }
        System.out.println("Sum of bucky is "+total);       
    }
    public static int avg(int...number) {
        int total = 0;
        for(int x:number){
            total+=x;
        }
        return total/number.length;
        
    }
}