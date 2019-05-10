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

public class Gui1 extends JFrame{
 
    public JTextField tf;

    public Gui1(){
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

        

        
        
    }

}
