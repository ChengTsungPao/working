package FinalProject;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.ImageIcon;
import java.awt.*;

public class Main{
	
    public static void main(String[] args) {  
        parentGui go = new parentGui();
        go.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        go.getContentPane().setBackground(Color.white);
        go.getContentPane().setVisible(true);
        go.setSize(800,600);
        go.setVisible(true);
        go.setResizable(false);
    }  
    
}
