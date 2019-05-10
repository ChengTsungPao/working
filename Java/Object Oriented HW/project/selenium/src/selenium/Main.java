package selenium;

import javax.swing.JFrame;

public class Main{
    public static void main(String[] args) {

        parentGui go = new parentGui();
        go.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        go.setSize(600,400);
        go.setVisible(true);
        
    }
}
