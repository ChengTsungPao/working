public class practice6_2{
    private String name;
    private practice6_3 birthday;

    public practice6_2(String theName,practice6_3 theDate){
        name = theName;
        birthday = theDate;
    }

    public String toString(){
        return String.format("My name is %s, my birthday is %s",name,birthday);
    }
}