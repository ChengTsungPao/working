class practice8{
    public static void main(String[] args) {
        practice8_2 member1 = new practice8_2("Megan", "Fox");
        practice8_2 member2 = new practice8_2("Natalie", "Portman");
        practice8_2 member3 = new practice8_2("Taylor", "Swift");
        
        System.out.println();
        System.out.println(member1.getFirst());
        System.out.println(member1.getLast());
        System.out.println(member1.getMembers());
        System.out.println(practice8_2.getMembers()); // Because of the static variable
    }
}