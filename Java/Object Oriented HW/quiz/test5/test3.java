public class test3{
    public static void main(String args[]) {
        System.out.println("two different String(data type) variable are same data");
        System.out.println("---------------------");
        System.out.println("two different object are not point to the same menory");
        String a= new String("222");
        String b= new String("222");
        String c= "222";
        String d= "222";
        System.out.println(a.getClass());
        System.out.println(b.getClass());
        System.out.println(a.equals(b));
        System.out.println(c.equals(d));
        
    }
}
//String buffers support mutable strings. Because String objects are immutable they can be shared.
//Initializes a newly created String object so that it represents an empty character sequence.
//Note that use of this constructor is unnecessary since Strings are immutable.