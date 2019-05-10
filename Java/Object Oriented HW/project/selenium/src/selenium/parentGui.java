package selenium;

import java.awt.FlowLayout;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JButton;
import javax.swing.JTextArea;
import java.awt.SystemColor;

import javax.swing.JOptionPane;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class parentGui extends JFrame{

    private JButton historybutton,instantbutton;  
    public JTextField daytextfield,labeltextfield;

    public parentGui(){
        super("The Data of Air Parameter");
        setLayout(new GridBagLayout());      
        
        String tmp="可使用參數:\n\n"
        		 + "NO (一氧化氮)                     NO2 (二氧化氮)\nNOx (氮氧化物)                   SO2 (二氧化硫)\n"
        		 + "CO (一氧化碳)                     CH4 (甲烷)\nTHC (總碳氫化合物)            NMHC (非甲烷碳氫化合物)\n"
        		 + "O3 (臭氧)                              PM10 (懸浮微粒PM10)\nPM2.5 (懸浮微粒PM2.5)      AT (大氣溫度)\n"
        		 + "RH (相對溼度)                      WD (風向)\n\n";
        JTextArea text = new JTextArea(tmp);
        text.setBackground(SystemColor.control);
        GridBagConstraints textlayout = new GridBagConstraints();
        //textlayout.gridx = 1;
        //textlayout.gridy = 1;
        textlayout.gridwidth = 0;
        textlayout.gridheight = 30;
        textlayout.weightx = 0;
        textlayout.weighty = 0;
        //textlayout.fill = GridBagConstraints.NONE;
        //textlayout.anchor = GridBagConstraints.NORTH;               
        add(text, textlayout); 
        
        daytextfield = new JTextField("Input the day before", 20);
        daytextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints daytextfieldlayout = new GridBagConstraints();
        //daytextfieldlayout.gridx = 1;
        //daytextfieldlayout.gridy = 1;
        daytextfieldlayout.gridwidth = 30;
        daytextfieldlayout.gridheight = 30;
        daytextfieldlayout.weightx = 0;
        daytextfieldlayout.weighty = 0;
        //daytextfieldlayout.fill = GridBagConstraints.NONE;
        //daytextfieldlayout.anchor = GridBagConstraints.WEST;
        add(daytextfield, daytextfieldlayout); 
        
        historybutton = new JButton("History data");
        GridBagConstraints historybuttonlayout = new GridBagConstraints();
        //historybuttonlayout.gridx = 1;
        //historybuttonlayout.gridy = 1;
        historybuttonlayout.gridwidth = 0;
        historybuttonlayout.gridheight = 30;
        historybuttonlayout.weightx = 0;
        historybuttonlayout.weighty = 0;
        //historybuttonlayout.fill = GridBagConstraints.NONE;
        //historybuttonlayout.anchor = GridBagConstraints.WEST;
        add(historybutton, historybuttonlayout);
        
        labeltextfield = new JTextField("Input the parameter", 20);
        labeltextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints labeltextfieldlayout = new GridBagConstraints();
        //labeltextfieldlayout.gridx = 1;
        //labeltextfieldlayout.gridy = 1;
        labeltextfieldlayout.gridwidth = 30;
        labeltextfieldlayout.gridheight = 30;
        labeltextfieldlayout.weightx = 0;
        labeltextfieldlayout.weighty = 0;
        //labeltextfieldlayout.fill = GridBagConstraints.NONE;
        //labeltextfieldlayout.anchor = GridBagConstraints.WEST;
        add(labeltextfield, labeltextfieldlayout); 
                
        instantbutton = new JButton("Instant  data");
        GridBagConstraints instantbuttonlayout = new GridBagConstraints();
        //instantbuttonlayout.gridx = 1;
        //instantbuttonlayout.gridy = -30;
        instantbuttonlayout.gridwidth = 0;
        instantbuttonlayout.gridheight = 30;
        instantbuttonlayout.weightx = 0;
        instantbuttonlayout.weighty = 0;
        //instantbuttonlayout.fill = GridBagConstraints.NONE;
        //instantbuttonlayout.anchor = GridBgConstraints.WEST;
        add(instantbutton, instantbuttonlayout);  
        
        HandlerClass handler = new HandlerClass();
        historybutton.addActionListener(handler);
        instantbutton.addActionListener(handler);
        
        
    }

    private class HandlerClass implements ActionListener{

        public void actionPerformed(ActionEvent event){
        	
            if(event.getActionCommand()=="Instant  data"){
                //System.out.println(event.getActionCommand());
                getdatagraph use = new getdatagraph();
                childGui go = new childGui(use.instant_button());
                go.setSize(800,350);
                go.setVisible(true);                                
            }
            if(event.getActionCommand()=="History data") {
            	//System.out.println(daytextfield.getText());
            	//System.out.println(labeltextfield.getText());
            	String[] d = daytextfield.getText().split(" ");
            	//String[] label = {labeltextfield.getText(),"time",labeltextfield.getText(),labeltextfield.getText()};
            	getdatagraph use = new getdatagraph(d,labeltextfield.getText());
            	use.history_button();
            }
            //JOptionPane.showMessageDialog(null, String.format("%s", event.getActionCommand()));
        }

    }

}

