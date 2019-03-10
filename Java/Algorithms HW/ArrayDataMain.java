class ArrayDataMain{
    public static void main(String[] args) {
        int[] A={1,2,3,5,6};
        int[] B={2,3,5,6,7};
        ArrayData4105054025 test = new ArrayData4105054025(A);
        System.out.println(test.max());
        System.out.println(test.dot(B));      
    }
}