package jframe;

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

public class Gui extends JFrame{

    private JButton reg,reg1;  
    public JTextField tf;

    public Gui(){
        super("The title");
        setLayout(new GridBagLayout());        

        JTextArea jTextArea1 = new JTextArea("NO (¤@®ñ¤Æ´á): 7.13 ppb");
        jTextArea1.setBackground(SystemColor.control);
        GridBagConstraints bag3 = new GridBagConstraints();
        bag3.gridx = 100;
        bag3.gridy = 0;
        bag3.gridwidth = 20;
        bag3.gridheight = 20;
        bag3.weightx = 0;
        bag3.weighty = 0;
        //bag3.fill = GridBagConstraints.NONE;
        //bag3.anchor = GridBagConstraints.NORTH;               
        add(jTextArea1, bag3); 
        
        tf = new JTextField("This is a sentece", 20);
        tf.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints bag2 = new GridBagConstraints();
        bag2.gridx = 50;
        bag2.gridy = 200;
        bag2.gridwidth = 20;
        bag2.gridheight = 20;
        bag2.weightx = 0;
        bag2.weighty = 0;
        //bag2.fill = GridBagConstraints.NONE;
        //bag2.anchor = GridBagConstraints.WEST;
        add(tf, bag2); 
        
        GridBagConstraints bag1 = new GridBagConstraints();
        reg = new JButton("History data");
        bag1.gridx = 50;
        bag1.gridy = -120;
        bag1.gridwidth = 20;
        bag1.gridheight = 20;
        bag1.weightx = 0;
        bag1.weighty = 0;
        //bag1.fill = GridBagConstraints.NONE;
        //bag1.anchor = GridBagConstraints.WEST;
        add(reg, bag1);
        
        GridBagConstraints bag4 = new GridBagConstraints();
        reg1 = new JButton("Instant data");
        bag4.gridy = -90;
        bag4.gridwidth = 20;
        bag4.gridheight = 20;
        bag4.weightx = 0;
        bag4.weighty = 0;
        //bag4.fill = GridBagConstraints.NONE;
        //bag4.anchor = GridBagConstraints.WEST;
        add(reg1, bag4);  
        
        HandlerClass handler = new HandlerClass();
        reg.addActionListener(handler);
        reg1.addActionListener(handler);
        
        
    }

    private class HandlerClass implements ActionListener{

        public void actionPerformed(ActionEvent event){
        	
            if(event.getActionCommand()=="Instant data"){
                System.out.println(event.getActionCommand());
                
                Gui1 go = new Gui1();
                //go.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                go.setSize(600,400);
                go.setVisible(true);
                
            }
            if(event.getActionCommand()=="History data") {
            	System.out.println(tf.getText());
            }
            JOptionPane.showMessageDialog(null, String.format("%s", event.getActionCommand()));
        }

    }

}
