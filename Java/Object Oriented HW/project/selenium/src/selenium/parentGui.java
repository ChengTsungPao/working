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

        JTextArea text = new JTextArea("NO (¤@®ñ¤Æ´á): 7.13 ppb");
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
        daytextfieldlayout.gridy = 200;
        daytextfieldlayout.gridwidth = 20;
        daytextfieldlayout.gridheight = 20;
        daytextfieldlayout.weightx = 0;
        daytextfieldlayout.weighty = 0;
        //daytextfieldlayout.fill = GridBagConstraints.NONE;
        //daytextfieldlayout.anchor = GridBagConstraints.WEST;
        add(daytextfield, daytextfieldlayout); 
        
        labeltextfield = new JTextField("kind", 20);
        labeltextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints labeltextfieldlayout = new GridBagConstraints();
        labeltextfieldlayout.gridx = 50;
        labeltextfieldlayout.gridy = 100;
        labeltextfieldlayout.gridwidth = 20;
        labeltextfieldlayout.gridheight = 20;
        labeltextfieldlayout.weightx = 0;
        labeltextfieldlayout.weighty = 0;
        //labeltextfieldlayout.fill = GridBagConstraints.NONE;
        //labeltextfieldlayout.anchor = GridBagConstraints.WEST;
        add(labeltextfield, labeltextfieldlayout); 
        
        historybutton = new JButton("History data");
        GridBagConstraints historybuttonlayout = new GridBagConstraints();
        historybuttonlayout.gridx = 50;
        historybuttonlayout.gridy = -120;
        historybuttonlayout.gridwidth = 20;
        historybuttonlayout.gridheight = 20;
        historybuttonlayout.weightx = 0;
        historybuttonlayout.weighty = 0;
        //historybuttonlayout.fill = GridBagConstraints.NONE;
        //historybuttonlayout.anchor = GridBagConstraints.WEST;
        add(historybutton, historybuttonlayout);
        
        instantbutton = new JButton("Instant data");
        GridBagConstraints instantbuttonlayout = new GridBagConstraints();
        instantbuttonlayout.gridy = -90;
        instantbuttonlayout.gridwidth = -120;
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
                System.out.println(event.getActionCommand());
                getdatagraph use = new getdatagraph();
                childGui go = new childGui(use.instant_button());
                go.setSize(600,400);
                go.setVisible(true);                                
            }
            if(event.getActionCommand()=="History data") {
            	System.out.println(daytextfield.getText());
            	String[] d = daytextfield.getText().split(" ");
            	String[] label = {labeltextfield.getText(),"time",labeltextfield.getText(),labeltextfield.getText()};
            	getdatagraph use = new getdatagraph(d,label);
            	use.history_button();
            }
            //JOptionPane.showMessageDialog(null, String.format("%s", event.getActionCommand()));
        }

    }

}

