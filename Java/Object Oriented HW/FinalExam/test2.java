import java.io.*;

public class test2{
    public static void main(String[] args) throws Exception {
        Cal test = new Cal("","");        
        test.write("","","");       
    }
}
class Cal{
    static String s1;
    static String s2;
    public Cal(String s1,String s2){
        this.s1 = s1;
        this.s2 = s2;
    }
    String Add(){

        char[] c1 = s1.toCharArray();
        char[] c2 = s2.toCharArray();
        String ans = "";
        int index;
        char[] tmpans;
        if(c1.length>c2.length){
            tmpans = new char[c1.length+1];
            index = c1.length+1;
        }else{
            tmpans = new char[c2.length+1];
            index = c2.length+1;
        }
        
        int index1=c1.length-1;
        int index2=c2.length-1;
        //System.out.println(index1);
        int tmp1=0,tmp2=0,tmp;
        
        for(int i=index-1;i>=0;i--){

            if(index1>=0 && index2>=0){
                tmp1 = (int)c1[index1]+(int)c2[index2]-48-48+tmp2;
                //System.out.println(tmp1);
                tmpans[i] = (char)(tmp1%10+48);
                tmp2=tmp1/10;
                index1--;
                index2--;
            }else if(index1<0 && index2<0){
                tmpans[i] = (char)(tmp2+48);
            }else if(index1<0){
                tmp1 = 0+(int)c2[index2]-48+tmp2;
                tmpans[i] = (char)(tmp1%10+48);
                tmp2=tmp1/10;
                index1--;
                index2--;
            }else if(index2<0){
                tmp1 = (int)c1[index1]+0-48+tmp2;
                tmpans[i] = (char)(tmp1%10+48);
                tmp2=tmp1/10;
                index1--;
                index2--;
            }
        }
        for(int i=0;i<tmpans.length;i++){
            tmp = (int)tmpans[i];
            if(tmp==48){
                if(i!=0) ans+="0";
            }else if(tmp==49){
                ans+="1";
            }else if(tmp==50){
                ans+="2";
            }else if(tmp==51){
                ans+="3";
            }else if(tmp==52){
                ans+="4";
            }else if(tmp==53){
                ans+="5";
            }else if(tmp==54){
                ans+="6";
            }else if(tmp==55){
                ans+="7";
            }else if(tmp==56){
                ans+="8";
            }else if(tmp==57){
                ans+="9";
            }
        }




        return ans;
    }

    void write(String s1,String s2,String s){
      
        try {
            File f1 = new File("number.txt");     
            File f2 = new File("result.txt");
            FileInputStream r = new FileInputStream(f1);
            FileOutputStream w = new FileOutputStream(f2);
            int flag = 0,tmp=0;
            while(tmp!=-1){
                tmp = r.read();
                //System.out.println(tmp);
                if(flag==0){
                    if(tmp>=48 && tmp<=57){
                        if(tmp==48){
                            this.s1+="0";
                        }else if(tmp==49){
                            this.s1+="1";
                        }else if(tmp==50){
                            this.s1+="2";
                        }else if(tmp==51){
                            this.s1+="3";
                        }else if(tmp==52){
                            this.s1+="4";
                        }else if(tmp==53){
                            this.s1+="5";
                        }else if(tmp==54){
                            this.s1+="6";
                        }else if(tmp==55){
                            this.s1+="7";
                        }else if(tmp==56){
                            this.s1+="8";
                        }else if(tmp==57){
                            this.s1+="9";
                        }
                    }
    
                }else{
                    if(tmp>=48 && tmp<=57){
                        if(tmp==48){
                            this.s2+="0";
                        }else if(tmp==49){
                            this.s2+="1";
                        }else if(tmp==50){
                            this.s2+="2";
                        }else if(tmp==51){
                            this.s2+="3";
                        }else if(tmp==52){
                            this.s2+="4";
                        }else if(tmp==53){
                            this.s2+="5";
                        }else if(tmp==54){
                            this.s2+="6";
                        }else if(tmp==55){
                            this.s2+="7";
                        }else if(tmp==56){
                            this.s2+="8";
                        }else if(tmp==57){
                            this.s2+="9";
                        }
                    }
                }
                if(tmp==10) flag++;
            }
    
            s = Add();
            System.out.println(this.s1);
            System.out.println(this.s2);
            System.out.println(s);  
            char[] add1 = this.s1.toCharArray();
            char[] add2 = this.s2.toCharArray();
            char[] answer = s.toCharArray();
            for(int i=0;i<add1.length;i++){
                w.write((int)(add1[i]));
            }
            w.write(13);
            w.write(10);
            w.write(13);
            w.write(10);
            for(int i=0;i<add2.length;i++){
                w.write((int)(add2[i]));
            }
            w.write(13);
            w.write(10);
            w.write(13);
            w.write(10);
            for(int i=0;i<answer.length;i++){
                w.write((int)(answer[i]));
            }
        } catch (Exception e) {
            System.out.println("Can not find number.txt");
            System.out.println(e);
        }




    }
}