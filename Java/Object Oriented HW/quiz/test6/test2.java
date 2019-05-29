public class test2{
    public static void main(String[] args) {
        CMember<String,Integer> a = new CMember<String,Integer>();
        CMember<Integer,String> a1 = new CMember<Integer,String>();
        String[] s = {"four","five","three","one","two"};
        Integer[] s1 = {4,5,3,1,2};

        a.set(s,s1);
        a1.set(s1,s);

        a.show();
        System.out.println("\n");
        a1.show();
    }
}
class CMember<a,b>{

    public a[] ans1;
    public b[] ans2;

    public void set(a[] data1,b[] data2){
        ans1 = data1;
        ans2 = data2;
    }
    public void show(){
        for(int i=0;i<ans1.length;i++){
            System.out.println(ans2[i]+":"+ans1[i]);
        }

    }
}