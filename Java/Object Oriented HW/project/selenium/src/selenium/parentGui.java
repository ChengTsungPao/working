package selenium;

import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JTextArea;
import java.awt.SystemColor;
import java.awt.*;
import javax.swing.*;

public class parentGui extends JFrame{

    private JButton historybutton,instantbutton;  
    private JCheckBox historyCheckBox,instantCheckBox,instantCheckBox1; 
    public JTextField daytextfield,labeltextfield;

    public parentGui(){
        super("The Data of Air Parameter");
        setLayout(new GridBagLayout());      
        
        String tmp="�i�ϥΰѼ�:\n\n"
        		 + "NO (�@��ƴ�)                     NO2 (�G��ƴ�)\nNOx (���ƪ�)                   SO2 (�G��Ʋ�)\n"
        		 + "CO (�@��ƺ�)                     CH4 (���J)\nTHC (�`�ҲB�ƦX��)            NMHC (�D���J�ҲB�ƦX��)\n"
        		 + "O3 (���)                              PM10 (�a�B�L��PM10)\nPM2.5 (�a�B�L��PM2.5)      AT (�j��ū�)\n"
        		 + "RH (�۹�ë�)                      WD (���V)\n";
        JTextArea text = new JTextArea(tmp);
        text.setBackground(SystemColor.control);
        GridBagConstraints textlayout = new GridBagConstraints();
        textlayout.gridwidth = 0;
        textlayout.gridheight = 30;
        textlayout.weightx = 0;
        textlayout.weighty = 0;           
        add(text, textlayout);         
        
        historyCheckBox = new JCheckBox("�x�s���v�ƾ�");
        historyCheckBox.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints historyCheckBoxlayout = new GridBagConstraints();
        historyCheckBoxlayout.gridwidth = 15;
        historyCheckBoxlayout.gridheight = 30;
        historyCheckBoxlayout.weightx = 0;
        historyCheckBoxlayout.weighty = 0;
        add(historyCheckBox, historyCheckBoxlayout); 
        
        instantCheckBox = new JCheckBox("�x�s�Y�ɼƾ�");
        instantCheckBox.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints instantCheckBoxlayout = new GridBagConstraints();
        instantCheckBoxlayout.gridwidth = 15;
        instantCheckBoxlayout.gridheight = 30;
        instantCheckBoxlayout.weightx = 0;
        instantCheckBoxlayout.weighty = 0;
        add(instantCheckBox, instantCheckBoxlayout);   
        
        JLabel blank = new JLabel("");
        blank.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints blanklayout = new GridBagConstraints();
        blanklayout.gridwidth = 0;
        blanklayout.gridheight = 30;
        blanklayout.weightx = 0;
        blanklayout.weighty = 0;
        add(blank, blanklayout); 
        
        daytextfield = new JTextField("Input the day before", 20);
        daytextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints daytextfieldlayout = new GridBagConstraints();
        daytextfieldlayout.gridwidth = 30;
        daytextfieldlayout.gridheight = 30;
        daytextfieldlayout.weightx = 0;
        daytextfieldlayout.weighty = 0;
        add(daytextfield, daytextfieldlayout); 
        
        historybutton = new JButton("History data");
        GridBagConstraints historybuttonlayout = new GridBagConstraints();
        historybuttonlayout.gridwidth = 0;
        historybuttonlayout.gridheight = 30;
        historybuttonlayout.weightx = 0;
        historybuttonlayout.weighty = 0;
        add(historybutton, historybuttonlayout);
        
        labeltextfield = new JTextField("Input the parameter", 20);
        labeltextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints labeltextfieldlayout = new GridBagConstraints();
        labeltextfieldlayout.gridwidth = 30;
        labeltextfieldlayout.gridheight = 30;
        labeltextfieldlayout.weightx = 0;
        labeltextfieldlayout.weighty = 0;
        add(labeltextfield, labeltextfieldlayout); 
                
        instantbutton = new JButton("Instant  data");
        GridBagConstraints instantbuttonlayout = new GridBagConstraints();
        instantbuttonlayout.gridwidth = 0;
        instantbuttonlayout.gridheight = 30;
        instantbuttonlayout.weightx = 0;
        instantbuttonlayout.weighty = 0;
        add(instantbutton, instantbuttonlayout);  
        
        HandlerClass handler = new HandlerClass();
        historybutton.addActionListener(handler);
        instantbutton.addActionListener(handler);
        historyCheckBox.addActionListener(handler);
        instantCheckBox.addActionListener(handler);
        
    }

    private class HandlerClass implements ActionListener{

        public void actionPerformed(ActionEvent event){
        	
        	if(event.getActionCommand()=="Instant  data"){
        		int flag = 0;
            	if(instantCheckBox.isSelected()) flag=1;
                //System.out.println(event.getActionCommand());
                getdatagraph use = new getdatagraph();
                childGui go = new childGui(use.instant_button(flag));
                go.setSize(800,350);
                go.setVisible(true);                                
            }
            if(event.getActionCommand()=="History data") {
            	int flag = 0;
            	if(historyCheckBox.isSelected()) flag=1;
            	//System.out.println(daytextfield.getText());
            	//System.out.println(labeltextfield.getText());
            	String[] d = daytextfield.getText().split(" ");
            	//String[] label = {labeltextfield.getText(),"time",labeltextfield.getText(),labeltextfield.getText()};
            	getdatagraph use = new getdatagraph(d,labeltextfield.getText());
            	use.history_button(flag);
            }
            //JOptionPane.showMessageDialog(null, String.format("%s", event.getActionCommand()));
        }

    }

}

