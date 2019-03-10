class practice12{
    public static void main(String[] args) {

        practice12_4 bucky[] = new practice12_4[2];
        bucky[0] = new practice12_2();
        bucky[1] = new practice12_3();
        
        for(int x=0;x<2;x++){
            bucky[x].eat();
        }
        
    }
}