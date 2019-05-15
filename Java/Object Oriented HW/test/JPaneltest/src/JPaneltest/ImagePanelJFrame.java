package JPaneltest;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JTextArea;
import javax.swing.ImageIcon;
import java.awt.*;

public class ImagePanelJFrame extends JFrame {  

    public ImagePanelJFrame() { 
    	
        init();  
    }  
      
    public void init() {  
        setSize(800,600);  
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);  
        ImagePanel imagePanel = new ImagePanel();  

        imagePanel.setOpaque(true); 
        imagePanel.setBackground(Color.white); 
        System.out.println(this);
        System.out.println(imagePanel); 	


        add(imagePanel);  
        setVisible(true);  
    }  
      
    public static void main(String[] args) {  
        ImagePanelJFrame f = new ImagePanelJFrame();  
    }  
      



} 
class ImagePanel extends JPanel {  
    public ImagePanel() {  
        super(new BorderLayout()); 
    }  
  
    public void paintComponent(Graphics g) {  
        super.paintComponent(g);  
        ImageIcon img = new ImageIcon("D:\\program\\vscode_workspace\\private\\working\\Java\\Object Oriented HW\\test\\JPaneltest\\graph.jpg"); 
        ImageIcon img1 = new ImageIcon("D:\\program\\vscode_workspace\\private\\working\\Java\\Object Oriented HW\\test\\JPaneltest\\graph1.jpg");
        img.paintIcon(this, g, 0, 0);  
        img1.paintIcon(this, g, 0, 0);  

    }  
} 



