public class practice8_2{
    private String first;
    private String last;
    private static int members = 0;

    public practice8_2(String fn, String ln){
        first = fn;
        last = ln;
        members++;
        System.out.printf("Contrusctor for %s %s, members in the club: %d\n", first, last, members);
    }
    public String getFirst(){
        return first;
    }
    public String getLast(){
        return last;
    }
    public static int getMembers(){
        return members;
    }
}