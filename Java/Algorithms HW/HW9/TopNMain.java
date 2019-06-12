class TopNMain{
    public static void main(String[] args) {
        int[][] c = {{1,2},{3,1},{3,1},{2,3},{1,3},{3,4},{5,1},{1,5}};
        TopN41050540252 test = new TopN41050540252();
        for(int x:test.Ans(c, 3, 10)){
            System.out.printf("%d ",x);
        }
        System.out.println();
    }
}