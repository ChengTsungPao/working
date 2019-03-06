public class practice6_3{
    private int month;
    private int day;
    private int year;

    public practice6_3(int m,int d,int y){
        month = m;
        day = d;
        year = y;

        System.out.printf("The contrtuctor for this is %s\n",this);
    }

    public String toString(){
        return String.format("%d/%d/%d",month,day,year); // wrong : return String.format("%s",this);
    }
}