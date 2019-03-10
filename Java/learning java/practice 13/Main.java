class Main{
    public static void main(String[] args) {

        fatty bucky = new fatty();
        food fo = new food();
        food tu = new tuna();
        food po = new potpie();

        bucky.digest(fo);
        bucky.digest(tu);
        bucky.digest(po);
        
    }
}

//abstract:
//if file1 extends file2,file1 need to create all file2's abstract object
