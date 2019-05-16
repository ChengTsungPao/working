package finalprojecttest;

import javax.swing.JFrame;
import javax.swing.JTextArea;
import java.awt.SystemColor;
import java.awt.*;

public class childGui extends JFrame{

    public childGui(String data){
        super("Instant Data");
        setLayout(new GridBagLayout()); 
        /*String[] line = data.split("\n");
        
        char[] tmp;
        String temp;
        
        temp="";
        tmp=line[4].toCharArray();
        for(int i=0;i<tmp.length;i++) {
        	if(tmp[i]=='®ð') {
        		for(int j=0;j<30;j++) {
        			temp=temp+" ";
        		}        		
        	}else if(tmp[i]=='Àô') {
        		for(int j=0;j<30;j++) {
        			temp=temp+" ";
        		}  
        	}
        	temp=temp+Character.toString(tmp[i]);
        }
        line[4]=temp;
        
        temp="";
        tmp=line[5].toCharArray();
        for(int i=0;i<tmp.length;i++) {
        	if(tmp[i]=='A') {
        		for(int j=0;j<27;j++) {
        			temp=temp+" ";
        		}        		
        	}else if(tmp[i]=='D') {
        		for(int j=0;j<23;j++) {
        			temp=temp+" ";
        		}  
        	}
        	temp=temp+Character.toString(tmp[i]);
        }
        line[5]=temp;
        
        temp="";
        tmp=line[6].toCharArray();
        for(int i=0;i<tmp.length;i++) {
        	if(tmp[i]=='R') {
        		for(int j=0;j<23;j++) {
        			temp=temp+" ";
        		}        		
        	}
        	temp=temp+Character.toString(tmp[i]);
        }
        line[6]=temp;
        
        temp="";
        tmp=line[7].toCharArray();
        for(int i=0;i<tmp.length;i++) {
        	if(tmp[i]=='W') {
        		for(int j=0;j<23;j++) {
        			temp=temp+" ";
        		}        		
        	}
        	temp=temp+Character.toString(tmp[i]);
        }
        line[7]=temp;
        
        temp="";
        tmp=line[8].toCharArray();
        for(int i=0;i<tmp.length;i++) {
        	if(tmp[i]=='W') {
        		for(int j=0;j<25;j++) {
        			temp=temp+" ";
        		}        		
        	}
        	temp=temp+Character.toString(tmp[i]);
        }
        line[8]=temp;
        
        String ans="";
        for(int i=0;i<line.length;i++) {
        	ans=ans+line[i]+"\n";        	
        }*/
      

        JTextArea text = new JTextArea(data);//ans
        text.setBackground(SystemColor.control);
        GridBagConstraints textlayout = new GridBagConstraints();
        textlayout.gridwidth = 20;
        textlayout.gridheight = 20;             
        add(text, textlayout);           
        
    }

}

