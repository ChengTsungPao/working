package FinalProject;

import javax.swing.JFrame;
import javax.swing.JTextArea;
import java.awt.SystemColor;
import java.awt.*;

public class childGui extends JFrame{

    public childGui(String data){
    	
        super("Instant Data");
        setLayout(new GridBagLayout()); 
        int tmp;
        String[] line = data.split("\n");
        String ans="空氣數據:\n\n";
        String[] blank = {"","\n","  ","\n","","\n","","\n","","\n","","\n"};
        for(int i=0;i<line.length/2;i++) {
        	if(i==4) {
        		tmp=6;
        	}else if(i==5) {
        		tmp=2;        		
        	}else {
        		tmp=0;
        	}        	
        	for(int j=0;j<35-line[2*i].toCharArray().length-tmp;j++) {
        		blank[2*i]+=" ";
        	}
        }
        for(int i=0;i<line.length;i++) {
        	ans+=line[i]+blank[i];
        }
        JTextArea text = new JTextArea(ans);//ans
        text.setBackground(SystemColor.control);
        GridBagConstraints textlayout = new GridBagConstraints();
        textlayout.gridwidth = 20;
        textlayout.gridheight = 20;             
        add(text, textlayout); 
        
    }

}


