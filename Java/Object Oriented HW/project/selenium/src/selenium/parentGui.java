package selenium;

import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JTextArea;
import java.awt.SystemColor;
import javax.swing.JOptionPane;
import javax.swing.JTextField;
import java.awt.*;

public class parentGui extends JFrame{

    private JButton historybutton,instantbutton;  
    private JCheckBox historyCheckBox,instantCheckBox,instantCheckBox1; 
    public JTextField daytextfield,labeltextfield;

    public parentGui(){
        super("The Data of Air Parameter");
        setLayout(new GridBagLayout());      
        
        String tmp="可使用參數:\n\n"
        		 + "NO (一氧化氮)                     NO2 (二氧化氮)\nNOx (氮氧化物)                   SO2 (二氧化硫)\n"
        		 + "CO (一氧化碳)                     CH4 (甲烷)\nTHC (總碳氫化合物)            NMHC (非甲烷碳氫化合物)\n"
        		 + "O3 (臭氧)                              PM10 (懸浮微粒PM10)\nPM2.5 (懸浮微粒PM2.5)      AT (大氣溫度)\n"
        		 + "RH (相對溼度)                      WD (風向)\n";
        JTextArea text = new JTextArea(tmp);
        text.setBackground(SystemColor.control);
        GridBagConstraints textlayout = new GridBagConstraints();
        textlayout.gridwidth = 0;
        textlayout.gridheight = 30;
        add(text, textlayout);      
        
        instantCheckBox = new JCheckBox("儲存即時數據");
        instantCheckBox.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints instantCheckBoxlayout = new GridBagConstraints();
        instantCheckBoxlayout.gridwidth = 15;
        instantCheckBoxlayout.gridheight = 30;
        add(instantCheckBox, instantCheckBoxlayout);  
        
        historyCheckBox = new JCheckBox("儲存歷史數據");
        historyCheckBox.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints historyCheckBoxlayout = new GridBagConstraints();
        historyCheckBoxlayout.gridwidth = 15;
        historyCheckBoxlayout.gridheight = 30;
        add(historyCheckBox, historyCheckBoxlayout);  
        
        JLabel blank = new JLabel("");
        blank.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints blanklayout = new GridBagConstraints();
        blanklayout.gridwidth = 0;
        blanklayout.gridheight = 30;
        add(blank, blanklayout); 
        
        daytextfield = new JTextField("Input the date before", 20);
        daytextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints daytextfieldlayout = new GridBagConstraints();
        daytextfieldlayout.gridwidth = 30;
        daytextfieldlayout.gridheight = 30;
        add(daytextfield, daytextfieldlayout); 
        
        instantbutton = new JButton("Instant  data");
        GridBagConstraints instantbuttonlayout = new GridBagConstraints();
        instantbuttonlayout.gridwidth = 0;
        instantbuttonlayout.gridheight = 30;
        add(instantbutton, instantbuttonlayout); 
        
        labeltextfield = new JTextField("Input the parameter", 20);
        labeltextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints labeltextfieldlayout = new GridBagConstraints();
        labeltextfieldlayout.gridwidth = 30;
        labeltextfieldlayout.gridheight = 30;
        add(labeltextfield, labeltextfieldlayout); 
                
        historybutton = new JButton("History data");
        GridBagConstraints historybuttonlayout = new GridBagConstraints();
        historybuttonlayout.gridwidth = 0;
        historybuttonlayout.gridheight = 30;
        add(historybutton, historybuttonlayout);
        
        HandlerClass handler = new HandlerClass();
        historybutton.addActionListener(handler);
        instantbutton.addActionListener(handler);
        historyCheckBox.addActionListener(handler);
        instantCheckBox.addActionListener(handler);
        
    }

    private class HandlerClass implements ActionListener{

        public void actionPerformed(ActionEvent event){
        	
        	if(event.getActionCommand()=="Instant  data"){
                //System.out.println(event.getActionCommand());
                getdatagraph use = new getdatagraph();
                childGui go = new childGui(use.instant_button(instantCheckBox.isSelected()));
                go.setSize(800,350);
                go.setVisible(true);                                
            }
            if(event.getActionCommand()=="History data") {
            	if(daytextfield.getText().equals("Input the date before") || daytextfield.getText().equals("")) {
            		JOptionPane.showMessageDialog(null, String.format("%s", "Please input the date !!!"));
            		
            	}else {
                	//System.out.println(daytextfield.getText());
                	//System.out.println(labeltextfield.getText());
                	String[] d = daytextfield.getText().split(" ");                	
                	getdatagraph use = new getdatagraph(d,labeltextfield.getText());
                	use.history_button(historyCheckBox.isSelected());
            	}
            }
            
        }

    }

}

