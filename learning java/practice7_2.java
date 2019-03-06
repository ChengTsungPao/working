public enum practice7_2{
    bucky("nice", "22"),
    kelsey("cute", "10"),
    julia("bigmistake", "12"),
    nicole("italian", "13"),
    candy("different", "14"),
    erin("iwish", "16");

    private final String desc;
    private final String year;

    practice7_2(String description, String birthday){
        desc = description;
        year = birthday;
    }

    public String getDesc(){
        return desc;
    }

    public String getYear(){
        return year;
    }
}