class SortingArrayMain{
    public static void main(String[] args) {
        int[] A = {1,2,5,7,4,2,1,7,1,2,5,7,4,2,1,5,4,8,10,11,6,47,7,0,5,7,9,100,5,8,9,1,12,11,7,8-1,-5};
        SortingArray41050540253 test = new SortingArray41050540253();
        show(test.sorting(A));  
        System.out.println(A.length);
    }
    static void show(int[] A) {
        for(int i=0;i<A.length;i++)
            System.out.printf("%d ",A[i]);
        System.out.println();        
    }  
}
