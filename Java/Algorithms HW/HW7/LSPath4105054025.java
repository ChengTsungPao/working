import java.util.Collections;
import java.util.ArrayList;
import java.util.Stack;

public class LSPath4105054025 extends LSPath{

    public ArrayList<ArrayList<Integer>> data = new ArrayList<ArrayList<Integer>>();
    public boolean[] visited;
    public int start=-1,num=-1;

    public void Max_Connected(){
        int max = -1;
        visited = new boolean[data.size()];
        for(int i=0;i<data.size();i++){
            visited[i] = false;
        }
        for(int i=0;i<data.size();i++){
            if(!visited[data.get(i).get(0)]){
                num = 0;            
                dfs(data.get(i).get(0));
                //System.out.println();
                if(num>max){
                    max = num;
                    start = i;
                }
            }
        }        
    }

    public void dfs(int v){
        int w = graph(v);          
        visited[v] = true;
        //System.out.printf("%d ",data.get(v).get(0));
        for(int i=1;i<data.get(w).size();i++){
            if(!visited[data.get(w).get(i)]){
                num++;
                dfs(data.get(w).get(i));                
            }
        }
    }

    public int graph(int v){
        int index = -1;
        for(int i=0;i<data.size();i++){
            if(data.get(i).get(0)==v){
                index = i;
                break;
            }
        }
        return index;
    }

    public void adjlist(int[][] list){
        int flag1,flag2;        
        ArrayList<Integer> tmp;
        for(int i=0;i<list.length;i++){
            flag1=1;
            flag2=1;                        
            for(int j=0;j<data.size();j++){
                if(data.get(j).get(0)==list[i][0]){
                    data.get(j).add(list[i][1]);
                    flag1=0;
                }
                if(data.get(j).get(0)==list[i][1]){
                    data.get(j).add(list[i][0]);
                    flag2=0;
                }
                if(flag1==0 && flag2==0) break;
            }
            tmp = new ArrayList<Integer>();
            if(flag1==1){
                tmp.add(list[i][0]);
                tmp.add(list[i][1]);
                data.add(tmp);
            }
            tmp = new ArrayList<Integer>();
            if(flag2==1){
                tmp.add(list[i][1]);
                tmp.add(list[i][0]);
                data.add(tmp);
            }
        }
        print(data);
    }

    public void print(ArrayList<ArrayList<Integer>> data){
        for(int i=0;i<data.size();i++){
            for(int j=0;j<data.get(i).size();j++){
                System.out.printf("%d ",data.get(i).get(j));
            }
            System.out.println();
        }         
    }

    public int Ans(int[][] list){
        //adjlist(list);
        //Max_Connected();        
        LSPath4105053132 test = new LSPath4105053132();
        return test.Ans(list);
    }

}