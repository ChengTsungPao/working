class Sort{

    private int array[];

    public Sort(int array[]){
        this.array=array;
    }

    public void sort(){
        
        int tmp;
        for(int i=0;i<array.length;i++){
            for(int j=0;j<array.length-i-1;j++){

                if(array[j]>array[j+1]){
                    tmp=array[j];
                    array[j]=array[j+1];
                    array[j+1]=tmp;
                }

            }
        }
        for(int i=0;i<array.length;i++){

            System.out.printf("%d ",array[i]);

        }       
        

    }

    public void max(){

        int max=array[0];
        for(int i=1;i<array.length;i++){
            if(max<array[i]){
                max=array[i];
            }
        }
        System.out.println(max);

    }

    public void min(){

        int min=array[0];
        for(int i=1;i<array.length;i++){
            if(min>array[i]){
                min=array[i];
            }
        }
        System.out.println(min);
    }

}

public class homework2_1{
    public static void main(String[] args) {

        int[] array = {2,5,7,4,8,10,5};
        Sort s = new Sort(array);

        s.max();
        s.min();
        s.sort();
        
    }

}