import java.util.EnumSet;

class practice7{
    public static void main(String[] args) {
        for(practice7_2 people: practice7_2.values()){
            System.out.printf("%s\t%s\t%s\n", people, people.getDesc() ,people.getYear());
        }

        System.out.println("\nAnd now for the range of constants!!!\n");

        for(practice7_2 people:EnumSet.range(practice7_2.kelsey, practice7_2.candy)){
            System.out.printf("%s\t%s\t%s\n", people, people.getDesc() ,people.getYear());
        }
    }
}