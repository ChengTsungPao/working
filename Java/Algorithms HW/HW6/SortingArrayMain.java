class SortingArrayMain{
    public static void main(String[] args) {
        int[] A = {1,2,5,7,4,2,1,7,1,2,5,7,4,2,1};
        SortingArray41050540252 test = new SortingArray41050540252();
        show(test.sorting(A));  
    }
    static void show(int[] A) {
        for(int i=0;i<A.length;i++)
            System.out.printf("%d ",A[i]);
        System.out.println();        
    }  
}
