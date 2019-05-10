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
        super("The title");
        setLayout(new GridBagLayout());      
        
        String tmp="可使用參數:\n\n"
        		 + "NO (一氧化氮)                 NO2 (二氧化氮)\nNOx (氮氧化物)               SO2 (二氧化硫)\n"
        		 + "CO (一氧化碳)                 CH4 (甲烷)\nTHC (總碳氫化合物)        NMHC (非甲烷碳氫化合物)\n"
        		 + "O3 (臭氧)                          PM10 (懸浮微粒PM10)\nPM2.5 (懸浮微粒PM2.5)  AT (大氣溫度)\n"
        		 + "RH (相對溼度)                  WD (風向)";
        JTextArea text = new JTextArea(tmp);
        text.setBackground(SystemColor.control);
        GridBagConstraints textlayout = new GridBagConstraints();
        textlayout.gridx = 100;
        textlayout.gridy = 0;
        textlayout.gridwidth = 20;
        textlayout.gridheight = 20;
        textlayout.weightx = 0;
        textlayout.weighty = 0;
        //textlayout.fill = GridBagConstraints.NONE;
        //textlayout.anchor = GridBagConstraints.NORTH;               
        add(text, textlayout); 
        
        daytextfield = new JTextField("This is a sentece", 20);
        daytextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints daytextfieldlayout = new GridBagConstraints();
        daytextfieldlayout.gridx = 50;
        daytextfieldlayout.gridy = 0;
        daytextfieldlayout.gridwidth = 50;
        daytextfieldlayout.gridheight = 50;
        daytextfieldlayout.weightx = 0;
        daytextfieldlayout.weighty = 0;
        //daytextfieldlayout.fill = GridBagConstraints.NONE;
        //daytextfieldlayout.anchor = GridBagConstraints.WEST;
        add(daytextfield, daytextfieldlayout); 
        
        labeltextfield = new JTextField("parameter", 20);
        labeltextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints labeltextfieldlayout = new GridBagConstraints();
        labeltextfieldlayout.gridx = 50;
        labeltextfieldlayout.gridy = 100;
        labeltextfieldlayout.gridwidth = 50;
        labeltextfieldlayout.gridheight = 50;
        labeltextfieldlayout.weightx = 0;
        labeltextfieldlayout.weighty = 0;
        //labeltextfieldlayout.fill = GridBagConstraints.NONE;
        //labeltextfieldlayout.anchor = GridBagConstraints.WEST;
        add(labeltextfield, labeltextfieldlayout); 
        
        historybutton = new JButton("History data");
        GridBagConstraints historybuttonlayout = new GridBagConstraints();
        historybuttonlayout.gridx = 50;
        historybuttonlayout.gridy = -200;
        historybuttonlayout.gridwidth = 20;
        historybuttonlayout.gridheight = 20;
        historybuttonlayout.weightx = 0;
        historybuttonlayout.weighty = 0;
        //historybuttonlayout.fill = GridBagConstraints.NONE;
        //historybuttonlayout.anchor = GridBagConstraints.WEST;
        add(historybutton, historybuttonlayout);
        
        instantbutton = new JButton("Instant data");
        GridBagConstraints instantbuttonlayout = new GridBagConstraints();
        instantbuttonlayout.gridx = 100;
        instantbuttonlayout.gridy = -300;
        instantbuttonlayout.gridwidth = 20;
        instantbuttonlayout.gridheight = 20;
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
        	
            if(event.getActionCommand()=="Instant data"){
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

