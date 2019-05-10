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

public class childGui extends JFrame{

    public childGui(String data){
        super("The title");
        setLayout(new GridBagLayout());    
        JTextArea text = new JTextArea(data);
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
        
    }

}
